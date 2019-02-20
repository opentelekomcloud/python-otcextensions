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
