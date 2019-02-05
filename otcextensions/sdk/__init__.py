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
import importlib
import os
import types
import warnings

from openstack import _log
from openstack import connection
from openstack import service_description
from openstack import utils


_logger = _log.setup_logging('openstack')

__all__ = [
    'register_otc_extensions',
]

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
    'anti_ddos': {
        'service_type': 'anti_ddos',
        'append_project_id': True,
        'endpoint_service_type': 'antiddos',
    },
    'auto_scaling': {
        'service_type': 'auto_scaling',
        'endpoint_service_type': 'as',
        'append_project_id': True,
    },
    'cce': {
        'service_type': 'cce',
        'append_project_id': False,
    },
    'cts': {
        'service_type': 'cts',
        # 'append_project_id': True,
    },
    'dcs': {
        'service_type': 'dcs',
        # 'endpoint_service_type': 'dms',
        'append_project_id': True,
    },
    'deh': {
        'service_type': 'deh',
        'append_project_id': True,
    },
    'dms': {
        'service_type': 'dms',
        'endpoint_service_type': 'dms',
        'append_project_id': True,
    },
    'dns': {
        'service_type': 'dns',
        'replace_system': True,
        # 'append_project_id': True,
    },
    'kms': {
        'service_type': 'kms',
        'append_project_id': True,
    },
    'obs': {
        'service_type': 'obs',
        'require_ak': True,
        'endpoint_service_type': 'object',
    },
    'rds': {
        'service_type': 'rds',
        # 'additional_headers': {'content-type': 'application/json'},
        'append_project_id': True,
    },
    'volume_backup': {
        'service_type': 'vbs',
        'append_project_id': True,
    },
    'mrs': {
        'service_type': 'mrs',
        'endpoint_service_type': 'mrs',
        'additional_headers': {'content-type': 'application/json'},
        'append_project_id': True,
    },
}


def _get_descriptor(service_name):
    """Find ServiceDescriptor class by the service name
    and instanciate it
    """
    service = OTC_SERVICES.get(service_name, None)
    if service:
        service_type = service['service_type']

        desc_class = _find_service_description_class(service_type)
        # _logger.debug('descriptor class %s' % desc_class)
        descriptor_args = {
            'service_type': service.get('endpoint_service_type', service_type)
            # 'service_type': service_type
        }

        if not desc_class.supported_versions:
            doc = _DOC_TEMPLATE.format(
                class_name="{service_type} Proxy".format(
                    service_type=service_type),
                **service)
        elif len(desc_class.supported_versions) == 1:
            supported_version = list(
                desc_class.supported_versions.keys())[0]
            doc = _DOC_TEMPLATE.format(
                class_name="{service_type} Proxy <{name}>".format(
                    service_type=service_type, name=supported_version),
                **service)
        else:
            class_doc_strings = "\n".join([
                ":class:`{class_name}`".format(
                    class_name=proxy_class.__name__)
                for proxy_class in desc_class.supported_versions.values()])
            doc = _PROXY_TEMPLATE.format(
                class_doc_strings=class_doc_strings, **service)
        descriptor = desc_class(**descriptor_args)
        descriptor.__doc__ = doc

        # _logger.debug('proxy is %s' % descriptor.proxy_class)

        return descriptor
    else:
        _logger.warn('unknown service %s was requested' % service_name)
        return None


def _find_service_description_class(service_type):
    package_name = 'otcextensions.sdk.{service_type}'.format(
        service_type=service_type).replace('-', '_')
    module_name = service_type.replace('-', '_') + '_service'
    class_name = ''.join(
        [part.capitalize() for part in module_name.split('_')])
    try:
        import_name = '.'.join([package_name, module_name])
        service_description_module = importlib.import_module(import_name)
    except ImportError as e:
        # ImportWarning is ignored by default. This warning is here
        # as an opt-in for people trying to figure out why something
        # didn't work.
        warnings.warn(
            "Could not import {service_type} service description: {e}".format(
                service_type=service_type, e=str(e)),
            ImportWarning)
        return service_description.ServiceDescription
    # There are no cases in which we should have a module but not the class
    # inside it.
    service_description_class = getattr(service_description_module, class_name)
    return service_description_class


def patch_connection(target):
    # descriptors are not working out of box for runtime attributes
    # So we need to inject them. Additionally we need to override some
    # properties of the proxy

    def get_otc_proxy(self, service_name=None, service=None):
        _logger.debug('get_otc_proxy is %s, %s, %s' %
                      (self, service_name, service))

        if service['service_type'] not in self._proxies:
            # Initialize proxy and inject required properties
            descriptor = _get_descriptor(service_name)
            if not descriptor:
                _logger.error('descriptor for service %s is missing' %
                              service_name)
                return

            proxy = descriptor.__get__(self, descriptor)

            # Set additional_headers into the proxy
            if 'additional_headers' in service:
                proxy.additional_headers = service.get('additional_headers')

            # If service requires AK/SK - inject them
            if service.get('require_ak', False):
                _logger.debug('during registration found that ak is required')
                config = self.config.config

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
                    return

            # Set endpoint_override
            endpoint_override = service.get('endpoint_override', None)
            if endpoint_override:
                _logger.debug('Setting endpoint_override into the %s.Proxy' %
                              service_name)
                proxy.endpoint_override = endpoint_override

            # Ensure EP contain %project_id
            append_project_id = service.get('append_project_id', False)
            if append_project_id:
                ep = proxy.get_endpoint_data().catalog_url
                project_id = proxy.get_project_id()
                if ep and not ep.rstrip('/').endswith('\\%(project_id)s') \
                        and not ep.rstrip('/').endswith('$(tenant_id)s') \
                        and not ep.rstrip('/').endswith(project_id):
                    proxy.endpoint_override = \
                        utils.urljoin(ep, '%(project_id)s')
        else:
            proxy = self._proxies[service['service_type']]

        return proxy

    connection.Connection.get_otc_proxy = types.MethodType(
        get_otc_proxy, target)


def inject_service_to_sdk(conn, service_name, service):
    """Inject service into the SDK space

    For some reason it should be a separate function
    """
    setattr(
        conn.__class__,
        service_name,
        property(
            fget=lambda self: self.get_otc_proxy(service_name, service)
        )
    )


def register_otc_extensions(conn, **kwargs):
    """Register supported OTC services and make them known to the OpenStackSDK

    :param conn: An established OpenStack cloud connection

    :returns: none
    """
    patch_connection(conn)

    for (service_name, service) in OTC_SERVICES.items():
        _logger.debug('trying to register service %s' % service_name)

        if service.get('replace_system', False):
            conn._proxies.pop(service_name, None)

        inject_service_to_sdk(conn, service_name, service)

    return None
