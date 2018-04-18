# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
__all__ = [
    'register_otc_extensions',
]

import importlib
import os
import types
import warnings

from openstack import _log
from openstack import connection
from openstack import proxy
from openstack import service_description
from openstack import utils

from oslo_utils import importutils

_logger = _log.setup_logging('openstack')

_DOC_TEMPLATE = (
    ":class:`{class_name}` for {service_type} aka project")
_PROXY_TEMPLATE = """Proxy for {service_type} aka project

This proxy object could be an instance of
{class_doc_strings}
depending on client configuration and which version of the service is
found on remotely on the cloud.
"""


# List OTC services here
#   Generally it is possible to iterate over known endpoints, but some
#   services requires injection of AK/SK
OTC_SERVICES = {
    'rds': {
        'service_type': 'rds',
        'endpoint_service_type': 'database',
        'additional_headers': {'content-type': 'application/json'},
        'strip_endpoint': True,
    },
    'obs': {
        'service_type': 'obs',
        'require_ak': True,
        'endpoint_service_type': 'object',
    },
    'auto_scaling': {
        'service_type': 'auto_scaling',
        'endpoint_service_type': 'as',
        'append_project_id': True,
    },
    'kms': {
        'service_type': 'kms',
        'append_project_id': True,
    },
    'cce': {
        'service_type': 'cce',
        'append_project_id': False,
    },
}


def _get_descriptor(service_name):
    service = OTC_SERVICES.get(service_name, None)
    if service:
        service_type = service['service_type']
        desc_class = service_description.OpenStackServiceDescription
        service_filter_class = _find_service_filter_class(service_name)
        descriptor_args = {'service_type': service_type}
        if service_filter_class:
            _logger.debug(
                'preparing to register service %s' %
                service_filter_class)
            desc_class = service_description.OpenStackServiceDescription
            descriptor_args['service_filter_class'] = service_filter_class
            class_names = service_filter_class._get_proxy_class_names()
            if len(class_names) == 1:
                _logger.debug('proxy_class_names: %s' % class_names[0])
                doc = _DOC_TEMPLATE.format(
                    class_name="{service_type} Proxy <{name}>".format(
                        service_type=service_type, name=class_names[0]),
                    **service)
                proxy_module = importutils.import_class(class_names[0])
                descriptor_args['proxy_class'] = proxy_module
            else:
                class_doc_strings = "\n".join([
                    ":class:`{class_name}`".format(class_name=class_name)
                    for class_name in class_names])
                doc = _PROXY_TEMPLATE.format(
                    class_doc_strings=class_doc_strings, **service)

        else:
            descriptor_args['proxy_class'] = proxy.Proxy
            descriptor_args['version'] = 'v1.0'
            doc = _DOC_TEMPLATE.format(
                class_name='~openstack.proxy.Proxy', **service)
        descriptor = desc_class(**descriptor_args)
        descriptor.__doc__ = doc
        _logger.debug('proxy is %s' % descriptor.proxy_class)

        return descriptor
    else:
        return None


def patch_connection(target):
    # descriptors are not working out of box for runtime attributes
    # So we need to inject them
    def __getattribute__(self, name):
        # print('getattr invoked on %s with %s' % (self, name))
        value = object.__getattribute__(self, name)
        if hasattr(value, '__get__'):
            value = value.__get__(self, self.__class__)
        return value

    def __setattr__(self, name, value):
        try:
            obj = object.__getattribute__(self, name)
        except AttributeError:
            pass
        else:
            if hasattr(obj, '__set__'):
                return obj.__set__(self, value)
        return object.__setattr__(self, name, value)
    connection.Connection.__getattribute__ = types.MethodType(
        __getattribute__, target)
    connection.Connection.__setattr__ = types.MethodType(
        __setattr__, target)


def add_service_to_sdk(connection, service_name, service_descriptor):
    # descriptors are not working out of box for runtime attributes
    connection.add_service(service_descriptor)
    # Unless connection is patched real proxy can be obtained only so
    proxy = service_descriptor.__get__(connection, service_descriptor)
    setattr(connection, service_name, proxy)
    return proxy


def register_otc_extensions(connection, **kwargs):

    for (service_name, service) in OTC_SERVICES.items():
        _logger.debug('trying to register service %s' % service_name)
        descriptor = _get_descriptor(service_name)
        if not descriptor:
            _logger.error('descriptor for service %s is missing' %
                          service_name)
            _logger.debug('keys %s' % service.keys())
            continue
        proxy = add_service_to_sdk(connection, service_name, descriptor)

        endpoint_service_type = service.get('endpoint_service_type', None)
        # endpoint_service_name = service.get('endpoint_service_name', None)
        if endpoint_service_type and \
                endpoint_service_type != service.get('service_type'):
            proxy.service_type = endpoint_service_type

        if 'additional_headers' in service:
            proxy.additional_headers = service.get('additional_headers')

        if service.get('require_ak', False):
            _logger.debug('during registration found that ak is required')
            config = connection.config.config

            ak = config.get('ak', None)
            sk = config.get('sk', None)

            if not ak:
                ak = os.getenv('S3_ACCESS_KEY_ID', None)
            if not sk:
                sk = os.getenv('S3_SECRET_ACCESS_KEY', None)

            if ak and sk:
                proxy._set_ak(ak=ak, sk=sk)
            else:
                _logger.error('AK/SK pair is not available')
                continue

        endpoint_override = service.get('endpoint_override', None)
        if endpoint_override:
            _logger.debug('Setting endpoint_override into the %s.Proxy' %
                          service_name)
            proxy.endpoint_override = endpoint_override

        append_project_id = service.get('append_project_id', False)
        if append_project_id:
            ep = proxy.get_endpoint_data().catalog_url
            if ep and not ep.rstrip('/').endswith('\%(project_id)s'):
                proxy.endpoint_override = utils.urljoin(ep, '%(project_id)s')

        # Can be done only that late
        # patch_connection(connection)
        # setattr(connection, service_name, proxy)
    return None


def _find_service_filter_class(service_type):
    package_name = 'otcextensions.sdk.{service_type}'.format(
        service_type=service_type).replace('-', '_')
    module_name = service_type.replace('-', '_') + '_service'
    class_name = ''.join(
        [part.capitalize() for part in module_name.split('_')])
    try:
        import_name = '.'.join([package_name, module_name])
        service_filter_module = importlib.import_module(import_name)
    except ImportError as e:
        # ImportWarning is ignored by default. This warning is here
        # as an opt-in for people trying to figure out why something
        # didn't work.
        warnings.warn(
            "Could not import {service_type} service filter: {e}".format(
                service_type=service_type, e=str(e)),
            ImportWarning)
        return None
    # There are no cases in which we should have a module but not the class
    # inside it.
    service_filter_class = getattr(service_filter_module, class_name)
    return service_filter_class
