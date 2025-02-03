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
from openstack import resource
from openstack import exceptions


class CbcOperationLockSpec(resource.Resource):
    lock_scene = resource.Body('lock_scene')
    lock_source_id = resource.Body('lock_source_id')


class TmsKeyValueSpec(resource.Resource):
    key = resource.Body('key')
    value = resource.Body('value')


class EndPointServiceSpec(resource.Resource):
    service_name = resource.Body('service_name')
    created_at = resource.Body('created_at')


class NodeIpsSpec(resource.Resource):
    livedata = resource.Body('livedata')
    shubao = resource.Body('shubao')


class IpSpec(resource.Resource):
    ip_address = resource.Body('ip_address')
    bandwidth_size = resource.Body('bandwidth_size', type=int)


class Gateway(resource.Resource):
    base_path = '/apigw/instances'

    allow_list = True
    allow_fetch = True
    allow_create = True
    allow_commit = True
    allow_delete = True

    _query_mapping = resource.QueryParameters('limit', 'offset', 'instance_id',
                                              'instance_name', 'status')

    # Properties
    description = resource.Body('description')
    maintain_begin = resource.Body('maintain_begin')
    maintain_end = resource.Body('maintain_end')
    instance_name = resource.Body('instance_name')
    security_group_id = resource.Body('security_group_id')
    vpcep_service_name = resource.Body('vpcep_service_name')

    # Attributes
    id = resource.Body('id')
    project_id = resource.Body('project_id')
    status = resource.Body('status')
    instance_status = resource.Body('instance_status', type=int)
    type = resource.Body('type')
    spec = resource.Body('spec')
    create_time = resource.Body('create_time')
    enterprise_project_id = resource.Body('enterprise_project_id')
    eip_address = resource.Body('eip_address')
    charging_mode = resource.Body('charging_mode', type=int)
    cbc_metadata = resource.Body('cbc_metadata', type=int)
    loadbalancer_provider = resource.Body('loadbalancer_provider')
    cbc_operation_locks = resource.Body('cbc_operation_locks', type=list,
                                        list_type=CbcOperationLockSpec)
    instance_id = resource.Body('instance_id')
    spec_id = resource.Body('spec_id')
    vpc_id = resource.Body('vpc_id')
    subnet_id = resource.Body('subnet_id')
    eip_id = resource.Body('eip_id')
    available_zone_ids = resource.Body('available_zone_ids', type=list)
    bandwidth_size = resource.Body('bandwidth_size', type=int)
    bandwidth_charging_mode = resource.Body('bandwidth_charging_mode')
    tags = resource.Body('tags', type=list, list_type=TmsKeyValueSpec)
    ingress_bandwidth_size = resource.Body('ingress_bandwidth_size', type=int)
    ingress_bandwidth_charging_mode = resource.Body(
        'ingress_bandwidth_charging_mode')
    message = resource.Body('message')
    job_id = resource.Body('job_id')
    ingress_ip = resource.Body('ingress_ip')
    ingress_ip_v6 = resource.Body('ingress_ip_v6')
    user_id = resource.Body('user_id')
    nat_eip_address = resource.Body('nat_eip_address')
    instance_version = resource.Body('instance_version')
    virsubnet_id = resource.Body('virsubnet_id')
    roma_eip_address = resource.Body('roma_eip_address')
    supported_features = resource.Body('supported_features', type=list)
    endpoint_service = resource.Body('endpoint_service',
                                     type=EndPointServiceSpec)
    endpoint_services = resource.Body('endpoint_services', type=list,
                                      list_type=EndPointServiceSpec)
    node_ips = resource.Body('node_ips', type=NodeIpsSpec)
    publicips = resource.Body('publicips', type=IpSpec)
    privateips = resource.Body('privateips', type=IpSpec)
    unreliable_ips = resource.Body('unreliable_ips', type=list)
    is_releasable = resource.Body('is_releasable', type=bool)
    progress = resource.Body('progress', type=int)
    error_code = resource.Body('error_code')
    error_msg = resource.Body('error_msg')
    start_time = resource.Body('start_time')
    end_time = resource.Body('end_time')
    listeners = resource.Body('listeners', type=dict)
    restrict_cidrs = resource.Body('restrict_cidrs', type=list)
    resource_subnet_cidr = resource.Body('resource_subnet_cidr')
    cloud_eip_id = resource.Body("cloudEipId")
    cloud_eip_address = resource.Body("cloudEipAddress")
    cloud_bandwidth_id = resource.Body('cloudBandwidthId')
    bandwidth_name = resource.Body('bandwidthName')
    charge_mode = resource.Body('chargeMode')

    def _get_creation_progress(self, session, gateway):
        gw_id = gateway.instance_id if gateway.id is None else gateway.id
        url = f'{self.base_path}/{gw_id}/progress'
        response = session.get(url)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self

    def _get_constraints(self, session, gateway):
        gw_id = gateway.instance_id if gateway.id is None else gateway.id
        url = f'{self.base_path}/{gw_id}/restriction'
        response = session.get(url)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self

    def _modify_spec(self, session, gateway, **attrs):
        gw_id = gateway.instance_id if gateway.id is None else gateway.id
        url = f'{self.base_path}/{gw_id}/postpaid-resize'
        response = session.post(url, json=attrs)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self

    def _bind_eip(self, session, gateway, **attrs):
        gw_id = gateway.instance_id if gateway.id is None else gateway.id
        url = f'{self.base_path}/{gw_id}/eip'
        response = session.put(url, json=attrs)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self

    def _unbind_eip(self, session, gateway):
        gw_id = gateway.instance_id if gateway.id is None else gateway.id
        url = f'{self.base_path}/{gw_id}/eip'
        response = session.delete(url)
        exceptions.raise_from_response(response)
        return None

    def _enable_public_access(self, session, gateway, **attrs):
        return self._enable_eip(session, gateway, 'nat-eip', **attrs)

    def _update_public_access(self, session, gateway, **attrs):
        return self._update_eip(session, gateway, 'nat-eip', **attrs)

    def _disable_public_access(self, session, gateway):
        return self._delete_eip(session, gateway, 'nat-eip')

    def _enable_ingress(self, session, gateway, **attrs):
        return self._enable_eip(session, gateway, 'ingress-eip', **attrs)

    def _update_ingress(self, session, gateway, **attrs):
        return self._update_eip(session, gateway, 'ingress-eip', **attrs)

    def _disable_ingress(self, session, gateway):
        return self._delete_eip(session, gateway, 'ingress-eip')

    def _enable_eip(self, session, gateway, url, **attrs):
        gw_id = gateway.instance_id if gateway.id is None else gateway.id
        url = f'{self.base_path}/{gw_id}/{url}'
        response = session.post(url, json=attrs)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self

    def _update_eip(self, session, gateway, url, **attrs):
        gw_id = gateway.instance_id if gateway.id is None else gateway.id
        url = f'{self.base_path}/{gw_id}/{url}'
        response = session.put(url, json=attrs)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self

    def _delete_eip(self, session, gateway, url):
        gw_id = gateway.instance_id if gateway.id is None else gateway.id
        url = f'{self.base_path}/{gw_id}/{url}'
        response = session.delete(url)
        exceptions.raise_from_response(response)
        return None
