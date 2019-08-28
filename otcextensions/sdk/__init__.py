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

from openstack import _log
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
        'endpoint_service_type': 'ccev2.0',
        # 'append_project_id': False,
    },
    'cts': {
        'service_type': 'cts',
        # 'append_project_id': True,
    },
    'css': {
        'service_type': 'css',
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
    },
    'kms': {
        'service_type': 'kms',
        'append_project_id': True,
    },
    'obs': {
        'service_type': 'obs',
        'require_ak': True,
        'endpoint_service_type': 'object',
        'set_endpoint_override': True
    },
    'rds': {
        'service_type': 'rds',
        # 'additional_headers': {'content-type': 'application/json'},
        'append_project_id': True,
    },
    'volume_backup': {
        'service_type': 'volume_backup',
        'append_project_id': True,
        'endpoint_service_type': 'vbs',
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
            'service_type': service.get('endpoint_service_type', service_type),
            'aliases': [service.get('service_type', service_type)]
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
    # try:
    import_name = '.'.join([package_name, module_name])
    service_description_module = importlib.import_module(import_name)
    # except ImportError as e:
    #     # ImportWarning is ignored by default. This warning is here
    #     # as an opt-in for people trying to figure out why something
    #     # didn't work.
    #     _logger.warn("Could not import {service_type} "
    #                  "service description: {e}".format(
    #                     service_type=service_type, e=str(e)),
    #                  ImportWarning)
    #     return service_description.ServiceDescription
    # There are no cases in which we should have a module but not the class
    # inside it.
    service_description_class = getattr(service_description_module, class_name)
    return service_description_class


def get_ak_sk(conn):
    """Fetch AK/SK from the cloud configuration or ENV

      This method might be called by the proxy.
    """
    config = conn.config.config

    ak = config.get('access_key', config.get('ak'))
    sk = config.get('secret_key', config.get('sk'))

    if not ak:
        ak = os.getenv('OS_ACCESS_KEY', os.getenv('S3_ACCESS_KEY_ID'))
    if not sk:
        sk = os.getenv('OS_SECRET_KEY', os.getenv('S3_SECRET_ACCESS_KEY'))

    if not (ak and sk):
        _logger.error('AK/SK pair is not configured in the connection, '
                      'but is requested by the service.')
        return (None, None)

    else:
        return(ak, sk)


def load(conn, **kwargs):
    """Register supported OTC services and make them known to the OpenStackSDK

    :param conn: An established OpenStack cloud connection

    :returns: none
    """
    conn.authorize()
    project_id = conn._get_project_info().id

    for (service_name, service) in OTC_SERVICES.items():
        _logger.debug('trying to register service %s' % service_name)

        if service.get('replace_system', False):
            # system_proxy = getattr(conn, service['service_type'])
            # for service_type in system_proxy.all_types:
            if service['service_type'] in conn._proxies:
                del conn._proxies[service['service_type']]
            # attr = getattr(conn, service_name)
            # print(hasattr(conn, service_name))
            # delattr(conn, service['service_type'])

        sd = _get_descriptor(service_name)

        conn.add_service(sd)

        if service.get('append_project_id', False):
            # If service requires project_id, but it is not present in the
            # service catalog - set endpoint_override
            ep = conn.endpoint_for(sd.service_type)
            if ep and not ep.rstrip('/').endswith('\\%(project_id)s') \
                    and not ep.rstrip('/').endswith('$(tenant_id)s') \
                    and not ep.rstrip('/').endswith(project_id):
                conn.config.config[
                    '_'.join([
                        sd.service_type.lower().replace('-', '_'),
                        'endpoint_override'
                    ])
                ] = utils.urljoin(ep, '%(project_id)s')
        elif service.get('set_endpoint_override', False):
            # We need to set endpoint_override for OBS, since otherwise it
            # fails dramatically
            ep = conn.endpoint_for(sd.service_type)
            conn.config.config[
                '_'.join([
                    sd.service_type.lower().replace('-', '_'),
                    'endpoint_override'
                ])
            ] = utils.urljoin(ep)

        # Inject get_ak_sk into the connection to give possibility
        # for some proxies to use them
        setattr(conn, 'get_ak_sk', get_ak_sk)

    return None


register_otc_extensions = load
