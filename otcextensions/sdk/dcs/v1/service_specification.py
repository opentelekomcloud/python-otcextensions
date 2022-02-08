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


class DetailsSpec(resource.Resource):
    #: Specification (total memory) of the DCS instance.
    capacity = resource.Body('capacity')
    #: Maximum bandwidth supported by the specification.
    max_bandwidth = resource.Body('max_bandwidth')
    #: Maximum number of clients supported by the specification,
    # which is usually equal to the maximum number of connections.
    max_clients = resource.Body('max_clients')
    #: Maximum number of connections supported by the specification.
    max_connections = resource.Body('max_connections')
    #: Maximum inbound bandwidth supported by the specification,
    # which is usually equal to the maximum bandwidth.
    max_in_bandwidth = resource.Body('max_in_bandwidth')
    #: Maximum available memory.
    max_memory = resource.Body('max_memory')
    #: Number of tenant IP addresses corresponding to the specifications.
    tenant_ip_count = resource.Body('tenant_ip_count')
    #: Number of shards supported by the specifications.
    sharding_num = resource.Body('sharding_num')
    #: Number of proxies supported by Proxy Cluster instances of the specified
    # specifications. If the instance is not a Proxy Cluster instance, the
    # value of this parameter is 0.
    proxy_num = resource.Body('proxy_num')
    #: Number of DBs of the specifications.
    db_number = resource.Body('db_number')


class FlavorsSpec(resource.Resource):
    #: Specification (total memory) of the DCS instance.
    capacity = resource.Body('capacity')
    #: Memory unit.
    unit = resource.Body('unit')
    #: AZ ID.
    available_zones = resource.Body('available_zones', type=list)


class ServiceSpecification(resource.Resource):

    resources_key = 'products'

    # capabilities
    allow_list = True

    #: Properties
    #: Product ID used to differentiate DCS specifications.
    product_id = resource.Body('product_id')
    #: DCS instance specification code.
    spec_code = resource.Body('spec_code')
    #: DCS instance type.
    cache_mode = resource.Body('cache_mode')
    #: Edition of DCS for Redis.
    product_type = resource.Body('product_type')
    #: CPU architecture
    cpu_type = resource.Body('cpu_type')
    #: Storage type.
    storage_type = resource.Body('storage_type')
    #: Details of the specifications.
    details = resource.Body('details', type=DetailsSpec)
    #: Cache engine.
    engine = resource.Body('engine')
    #: Cache engine version.
    engine_versions = resource.Body('engine_versions')
    # DCS specifications. The value subjects to the returned specifications.
    spec_details = resource.Body('spec_details')
    #: Detailed DCS specifications, including the maximum number of
    # connections and maximum memory size.
    spec_details2 = resource.Body('spec_details2')
    #: Billing mode. Value: Hourly.
    charging_type = resource.Body('charging_type')
    #: Price of the DCS service to which you can subscribe.
    price = resource.Body('price')
    #: Currency
    currency = resource.Body('currency')
    #: Product type.
    prod_type = resource.Body('prod_type')
    #: Cloud service type code.
    cloud_service_type_code = resource.Body('cloud_service_type_code')
    #: Cloud resource type code.
    cloud_resource_type_code = resource.Body('cloud_resource_type_code')
    #: AZs with available resources.
    flavors = resource.Body('flavors', type=list, list_type=FlavorsSpec)
