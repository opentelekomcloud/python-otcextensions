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
import warnings
# import openstack

# import os_service_types

from oslo_utils import importutils

from openstack import service_description

from openstack import _log
from openstack import proxy
from openstack import utils

# from otcextensions.sdk import proxy as sdk_proxy


_logger = _log.setup_logging('openstack')
# _service_type_manager = os_service_types.ServiceTypes()

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
        # 'endpoint_override': 'https://rds.%(region_name)s.otc.t-systems.com'
    },
    'obs': {
        'service_type': 'obs',
        'require_ak': True,
        'endpoint_service_name': 'objectstorage',
        # 'endpoint_override': 'https://obs.%(region_name)s.otc.t-systems.com'
    },
    'auto_scaling': {
        'service_type': 'auto_scaling',
        'endpoint_service_type': 'as',
        'append_project_id': True,
    },
}


def _prepare_services(**kwargs):
    # services = []
    for (service_name, service) in OTC_SERVICES.items():
        # service = OTC_SERVICES
        service_type = service['service_type']
        desc_class = service_description.OpenStackServiceDescription
        service_filter_class = _find_service_filter_class(service_name)
        # print(service_filter_class.service_type.__get__())
        descriptor_args = {'service_type': service_type}
        # descriptor_args = {}
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
            doc = _DOC_TEMPLATE.format(
                class_name='~openstack.proxy.Proxy', **service)
        descriptor = desc_class(**descriptor_args)
        descriptor.__doc__ = doc
        _logger.debug('proxy is %s' % descriptor.proxy_class())

        service['descriptor'] = descriptor
        # services.append(descriptor)

    return None


def register_otc_extensions(connection, **kwargs):
    _prepare_services()
    for (service_name, service) in OTC_SERVICES.items():
        _logger.debug('trying to register service %s' % service_name)
        descriptor = service.get('descriptor', None)
        if not descriptor:
            _logger.error('descriptor for service %s is missing' %
                          service_name)
            _logger.debug('keys %s' % service.keys())
            continue
        proxy = descriptor.__get__(connection, descriptor)

        endpoint_service_type = service.get('endpoint_service_type', None)
        # endpoint_service_name = service.get('endpoint_service_name', None)
        if endpoint_service_type and \
                endpoint_service_type != service.get('service_type'):
            proxy.service_type = endpoint_service_type

        if 'additional_headers' in service:
            proxy.additional_headers = service.get('additional_headers')

        connection.add_service(descriptor)

        if service.get('require_ak', False):
            _logger.debug('during registration found that ak is required')
            config = connection.config.config

            ak = config.get('ak', None)
            sk = config.get('sk', None)

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
            ep = proxy.get_endpoint()
            if ep and not ep.rstrip('/').endswith('\%(project_id)s'):
                proxy.endpoint_override = utils.urljoin(ep, '%(project_id)s')

        # recover conn.service.__get__ descriptor, since it is lost
        setattr(
            connection,
            service['service_type'],
            proxy)


# def _get_aliases(service_type, aliases=None):
#     # We make connection attributes for all official real type names
#     # and aliases. Three services have names they were called by in
#     # openstacksdk that are not covered by Service Types Authority aliases.
#     # Include them here - but take heed, no additional values should ever
#     # be added to this list.
#     # that were only used in openstacksdk resource naming.
#     LOCAL_ALIASES = {
#         'rds': 'rds',
#     }
#     all_types = set(_service_type_manager.get_aliases(service_type))
#     if aliases:
#         all_types.update(aliases)
#     if service_type in LOCAL_ALIASES:
#         all_types.add(LOCAL_ALIASES[service_type])
#     return all_types


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
