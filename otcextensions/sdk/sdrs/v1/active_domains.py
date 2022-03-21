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


class ReplicationCluster(resource.Resource):
    #: Properties
    #: Availability zone name
    availability_zone = resource.Body('availability_zone')


class Domains(resource.Resource):
    #: Properties
    #: Active-active domain id
    id = resource.Body('id')
    #: Active-active domain name
    name = resource.Body('name')
    #: Active-active domain description
    description = resource.Body('description')
    #: Active-active domain availability
    sold_out = resource.Body('sold_out', type=bool)
    #: Active-active domain local replication cluster parameters
    local_replication_cluster = resource.Body('local_replication_cluster',
                                              type=ReplicationCluster)
    #: Active-active domain remote replication cluster parameters
    remote_replication_cluster = resource.Body(
        'remote_replication_cluster',
        type=ReplicationCluster)


class ActiveDomains(resource.Resource):
    """SDRS Active-Active Domain Resource"""
    base_path = '/active-domains'

    #: capabilities
    allow_list = True

    #: Properties
    #: List of available domains
    domains = resource.Body('domains', type=list, list_type=Domains)
