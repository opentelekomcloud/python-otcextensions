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
import time

import openstack
from openstack import _log
from openstack import utils

from otcextensions.common import exc
from otcextensions.sdk import proxy
from otcextensions.sdk.cloud import cce as _cce
from otcextensions.sdk.cloud import dds as _dds
from otcextensions.sdk.cloud import rds as _rds
from otcextensions.sdk.compute.v2 import server
from otcextensions.sdk.network.v2 import service_provider


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
    'apig': {
        'service_type': 'apig',
        'append_project_id': True,
        'endpoint_service_type': 'apigv2'
    },
    'aomv1': {
        'service_type': 'aomv1',
        'endpoint_service_type': 'aomv1'
    },
    'aomv2': {
        'service_type': 'aomv2',
        'endpoint_service_type': 'aomv2'
    },
    'auto_scaling': {
        'service_type': 'auto_scaling',
        'endpoint_service_type': 'as',
        'append_project_id': True,
    },
    'bms': {
        'service_type': 'bms'
    },
    'cbr': {
        'service_type': 'cbr',
        'append_project_id': True,
    },
    'cce': {
        'service_type': 'cce',
        'endpoint_service_type': 'ccev2.0',
    },
    'ces': {
        'service_type': 'ces',
        'append_project_id': True,
    },
    'cfwv1': {
        'service_type': 'cfwv1',
        'append_project_id': True,
        'endpoint_service_type': 'cfwv1'
    },
    'cfwv2': {
        'service_type': 'cfwv2',
        'append_project_id': True,
        'endpoint_service_type': 'cfwv2'
    },
    'cfwv3': {
        'service_type': 'cfwv3',
        'append_project_id': True,
        'endpoint_service_type': 'cfwv3'
    },
    'cts': {
        'service_type': 'cts',
        'endpoint_service_type': 'cts'
    },
    'ctsv2': {
        'service_type': 'ctsv2',
        'endpoint_service_type': 'ctsv2'
    },
    'ctsv3': {
        'service_type': 'ctsv3',
        'endpoint_service_type': 'ctsv3'
    },
    'css': {
        'service_type': 'css',
    },
    'csbs': {
        'service_type': 'csbs',
        'endpoint_service_type': 'data-protect'
    },
    'dataarts': {
        'service_type': 'dataarts',
    },
    'dcaas': {
        'service_type': 'dcaas',
        'append_project_id': False,
    },
    'dcs': {
        'service_type': 'dcs',
        'append_project_id': True,
    },
    'dds': {
        'service_type': 'dds',
        'endpoint_service_type': 'ddsv3',
        'append_project_id': True
    },
    'deh': {
        'service_type': 'deh',
        'append_project_id': True,
    },
    'ddmv1': {
        'service_type': 'ddmv1',
        'endpoint_service_type': 'ddmv1',
        'append_project_id': True
    },
    'ddmv2': {
        'service_type': 'ddmv2',
        'endpoint_service_type': 'ddmv2',
        'append_project_id': True
    },
    'ddmv3': {
        'service_type': 'ddmv3',
        'endpoint_service_type': 'ddmv3',
        'append_project_id': True
    },
    'dis': {
        'service_type': 'dis',
        'endpoint_service_type': 'disv2'
    },
    'dms': {
        'service_type': 'dms',
        'endpoint_service_type': 'dms',
        'append_project_id': True,
    },
    'dmsv2': {
        'service_type': 'dmsv2',
        'endpoint_service_type': 'dmsv2',
    },
    'dns': {
        'service_type': 'dns',
        'replace_system': True,
    },
    'dli': {
        'service_type': 'dli',
    },
    'drs': {
        'service_type': 'drs',
    },
    'dws': {
        'service_type': 'dws',
        'endpoint_service_type': 'dwsv1'
    },
    'ecs': {
        'service_type': 'ecs',
    },
    'elb': {
        'service_type': 'elb',
        # 'replace_system': True
    },
    'enterprise_dashboard': {
        'service_type': 'enterprise-dashboard',
        'endpoint_service_type': 'enterprise-dashboard'
    },
    'enterprise_dashboard_v1': {
        'service_type': 'enterprise-dashboard-v1',
        'endpoint_service_type': 'enterprise-dashboard-v1'
    },
    'er': {
        'service_type': 'er',
        'append_project_id': True,
        'endpoint_service_type': 'erv3'
    },
    'evpn': {
        'service_type': 'evpn',
        'append_project_id': True,
        'endpoint_service_type': 'evpn'
    },
    'function_graph': {
        'service_type': 'function_graph',
        'append_project_id': True,
        'endpoint_service_type': 'functiongraph'
    },
    'gaussdb': {
        'service_type': 'gaussdb',
        'append_project_id': True,
        'endpoint_service_type': 'gaussdb-mysql'
    },
    'geminidb': {
        'service_type': 'geminidb',
        'append_project_id': True,
        'endpoint_service_type': 'geminidb'
    },
    'hss': {
        'service_type': 'hss',
        'append_project_id': True,
        'endpoint_service_type': 'hss'
    },
    'identity': {
        'service_type': 'identity',
        'replace_system': True
    },
    'imsv1': {
        'service_type': 'imsv1',
    },
    'imsv2': {
        'service_type': 'imsv2',
    },
    'kms': {
        'service_type': 'kms',
        'append_project_id': True,
    },
    'lts': {
        'service_type': 'lts',
        'endpoint_service_type': 'ltsv2',
        'append_project_id': True,
    },
    'mrs': {
        'service_type': 'mrs',
        'append_project_id': True,
    },
    'modelartsv1': {
        'service_type': 'modelartsv1',
        'endpoint_service_type': 'modelartsv1'
    },
    'modelartsv2': {
        'service_type': 'modelartsv2',
        'endpoint_service_type': 'modelartsv2'
    },
    'rts': {
        'service_type': 'rts',
        'endpoint_service_type': 'orchestration'
    },
    'rms': {
        'service_type': 'rms'
    },
    'nat': {
        'service_type': 'nat',
    },
    'natv3': {
        'service_type': 'natv3',
        'endpoint_service_type': 'natv3'
    },
    'obs': {
        'service_type': 'obs',
        'require_ak': True,
        'endpoint_service_type': 'object',
        'set_endpoint_override': True
    },
    'ocr': {
        'service_type': 'ocr',
    },
    'plas': {
        'service_type': 'plas'
    },
    'rds': {
        'service_type': 'rds',
        'endpoint_service_type': 'rdsv3',
        'append_project_id': True
    },
    'sdrs': {
        'service_type': 'sdrs',
        'append_project_id': True
    },
    'sfsturbo': {
        'service_type': 'sfsturbo',
        'endpoint_service_type': 'sfsturbo',
        # 'append_project_id': True,
    },
    'smn': {
        'service_type': 'smn',
        'append_project_id': True
    },
    'swr': {
        'service_type': 'swr',
        'endpoint_service_type': 'swrv2'
    },
    'tms': {
        'service_type': 'tms'
    },
    'vlb': {
        'service_type': 'vlb',
        'endpoint_service_type': 'elbv3',
    },
    'volume_backup': {
        'service_type': 'volume_backup',
        'append_project_id': True,
        'endpoint_service_type': 'vbs',
    },
    'vpc': {
        'service_type': 'vpc',
        'append_project_id': True,
    },
    'vpcep': {
        'service_type': 'vpcep',
        'append_project_id': True,
    },
    'vpn': {
        'service_type': 'vpn',
        'endpoint_service_type': 'vpc2.0',
        'append_project_id': True,
    },
    'waf': {
        'service_type': 'waf',
        # 'set_endpoint_override': True
    },
    'wafd': {
        'service_type': 'wafd',
        'endpoint_service_type': 'premium-waf'
    }
}

# Specifies the number of seconds a temporary AK/SK
# is to be renewed before it expires
# Usually 30 seconds should be sufficient
TMP_AKSK_RENEWAL = 30


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


def _get_ak_sk_autocreate(conn):
    """Autocreate/Return a temporary AK/SK"""
    config_tmp_aksk = conn.config.config.get('_tmp_aksk', {})

    # Check if a new temporary AK/SK needs to be created
    if (config_tmp_aksk.get('expires', 0) - TMP_AKSK_RENEWAL) \
            < int(time.time()):
        # Create new temporary AK/SK with minimal duration of 900s
        tmp_aksk = conn.identity.create_security_token(duration=900)
        config_tmp_aksk['expires'] = int(time.time())
        config_tmp_aksk['access_key'] = tmp_aksk.access
        config_tmp_aksk['secret_key'] = tmp_aksk.secret
        config_tmp_aksk['security_token'] = tmp_aksk.security_token
        # Save temporary AK/SK in config
        conn.config.config['_tmp_aksk'] = config_tmp_aksk

    # Retrieve temporary AK/SK from config
    ak = config_tmp_aksk['access_key']
    sk = config_tmp_aksk['secret_key']
    token = config_tmp_aksk['security_token']
    return ak, sk, token


def get_ak_sk(conn):
    """Fetch AK/SK from the cloud configuration or ENV

      This method might be called by the proxy.
    """
    config = conn.config.config

    ak = config.get('access_key', config.get('ak'))
    sk = config.get('secret_key', config.get('sk'))
    token = config.get('security_token', config.get('token'))

    if not ak:
        ak = os.getenv('OS_ACCESS_KEY', os.getenv('S3_ACCESS_KEY_ID'))
    if not sk:
        sk = os.getenv('OS_SECRET_KEY', os.getenv('S3_SECRET_ACCESS_KEY'))
    if not token:
        token = os.getenv('OS_SECURITY_TOKEN', os.getenv('S3_SECURITY_TOKEN'))

    # Autocreate/return a temporary AK/SK if "autocreate_aksk" is enabled
    if not (ak and sk) and config.get('autocreate_aksk', False):
        (ak, sk, token) = _get_ak_sk_autocreate(conn)

    if not (ak and sk):
        _logger.error('AK/SK pair is not configured in the connection, '
                      'but is requested by the service.')
        return (None, None)

    else:
        if not token:
            return ak, sk
        else:
            return ak, sk, token


def extend_instance(obj, cls):
    """Apply mixins to a class instance after creation"""
    base_cls = obj.__class__
    base_cls_name = obj.__class__.__name__
    obj.__class__ = type(base_cls_name, (base_cls, cls), {})


def patch_openstack_resources():
    openstack.proxy.Proxy._report_stats_statsd = \
        proxy.Proxy._report_stats_statsd
    openstack.proxy.Proxy._report_stats_influxdb = \
        proxy.Proxy._report_stats_influxdb
    openstack.compute.v2.server.Server._get_tag_struct = \
        server.Server._get_tag_struct
    openstack.compute.v2.server.Server._prepare_override_url = \
        server.Server._prepare_override_url
    openstack.compute.v2.server.Server.add_tag = server.Server.add_tag
    openstack.compute.v2.server.Server.remove_tag = server.Server.remove_tag
    openstack.exceptions.raise_from_response = \
        exc.raise_from_response
    openstack.network.v2.service_provider.ServiceProvider.list = \
        service_provider.ServiceProvider.list


def register_single_service(conn, service_name, project_id=None, service=None):
    """Register single service in the SDK"""
    if not project_id:
        project_id = conn._get_project_info().id
    if not service and service_name in OTC_SERVICES:
        service = OTC_SERVICES[service_name]

    if service.get('replace_system', False):
        # system_proxy = getattr(conn, service['service_type'])
        # for service_type in system_proxy.all_types:
        if service['service_type'] in conn._proxies:
            del conn._proxies[service['service_type']]
        # attr = getattr(conn, service_name)
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
            key = '_'.join([
                sd.service_type.lower().replace('-', '_'),
                'endpoint_override'])
            if key not in conn.config.config:
                conn.config.config[key] = utils.urljoin(ep,
                                                        '%(project_id)s')

    elif service.get('set_endpoint_override', False):
        # SDK respects skip_discovery only if endpoint_override is set.
        # In case, when append_project_id is skipped for the service,
        # but the discovery on the service is not working - we might be
        # failing dramatically.
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


def load(conn, **kwargs):
    """Register supported OTC services and make them known to the OpenStackSDK

    :param conn: An established OpenStack cloud connection

    :returns: none
    """
    conn.authorize()
    project_id = conn._get_project_info().id

    for (service_name, service) in OTC_SERVICES.items():
        # _logger.debug('trying to register service %s' % service_name)
        register_single_service(conn, service_name, project_id, service)

    patch_openstack_resources()

    extend_instance(conn, _rds.RdsMixin)
    extend_instance(conn, _cce.CceMixin)
    extend_instance(conn, _dds.DdsMixin)

    return None


register_otc_extensions = load
