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
from openstack import _log

from otcextensions.sdk import sdk_resource

_logger = _log.setup_logging('openstack')

class Cluster(sdk_resource.Resource):
    resource_key = 'cluster'
    resources_key = 'clusters'
    base_path = '/cluster_infos'

    # capabilities
    allow_create = True
    allow_list = True
    allow_get = True
    allow_delete = True
    allow_update = True

    _query_mapping = resource.QueryParameters('id', 'name','status','cluster_type','flavor','core_flavor','masternum','corenum','vpc','availability_zone','version','keypair')

    #: Properties
    #: Specifies CLUSTER ID
    id = resource.Body('clusterId', alternate_id=True)

    #: Name of the cluster 
    name = resource.Body('clusterName')

    #: status of the cluster 
    status = resource.Body('clusterState')

    #: tpye of the cluster 
    cluster_type = resource.Body('clusterType')

    #: flavor of the cluster 
    flavor = resource.Body('masterNodeSize')

    #: core_flavor  of the cluster 
    core_flavor = resource.Body('coreNodeSize')

    #:  master node number of the cluster 
    masternum = resource.Body('masterNodeNum')

    #: core node number of the clsuter 
    corenum = resource.Body('coreNodeNum')

    #: vpc of the cluster 
    vpc = resource.Body('vpc')

    #: az of the cluster 
    availability_zone = resource.Body('azName')

    #:version of the cluster 
    version = resource.Body('clusterVersion')

    #: keypair of the cluster 
    keypair = resource.Body('nodePublicCertName')


class Host(sdk_resource.Resource):
    resource_key = 'host'
    resources_key = 'hosts'
    base_path = '/clusters/%(cluster_id)s/hosts'


    # capabilities
    allow_create = True
    allow_list = True
    allow_get = True
    allow_delete = True
    allow_update = True

    _query_mapping = resource.QueryParameters('id', 'name','status','type','flavor','ip','mem','cpu','data_volume_size')


    cluster_id = resource.URI('cluster_id')
    
    #: Properties
    #: Specifies HOST ID
    id = resource.Body('id', alternate_id=True)

    #: Name of the host
    name = resource.Body('name')

    #: status of the host
    status = resource.Body('status')

    #: type of the host
    type = resource.Body('type')

    #: flavor of the host
    flavor = resource.Body('flavor')

    #: ip  of the host
    ip = resource.Body('ip')

    #:  mem of the host
    mem = resource.Body('mem')

    #:  cpu of the host
    cpu = resource.Body('cpu')

    #:  data_volume_size of the host
    data_volume_size = resource.Body('data_volume_size')
