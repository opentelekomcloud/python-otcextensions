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
#
from openstack import resource


class Node(resource.Resource):
    #: Node specifications
    specification = resource.Body("specification", type=str)
    #: Number of nodes
    count = resource.Body("count", type=int)
    #: Number of available nodes
    available_count = resource.Body("available_count", type=int)


class Cluster(resource.Resource):
    #: Cluster ID
    cluster_id = resource.Body("cluster_id", type=str)
    #: Cluster name
    cluster_name = resource.Body("cluster_name", type=str)
    #: Cluster remarks
    description = resource.Body("description", type=str)
    #: Tenant to which a cluster belongs
    tenant = resource.Body("tenant", type=str)
    #: Project to which a cluster belongs
    project = resource.Body("project", type=str)
    #: User to which a cluster belongs
    owner = resource.Body("owner", type=str)
    #: Time when a cluster is created, in milliseconds
    #:  calculated from 1970.1.1 0:0:0 UTC
    created_at = resource.Body("created_at", type=int)
    #: Cluster status. The value can be deploying, running,
    #:  concerning, or abnormal.
    status = resource.Body("status", type=str)
    #: Node configuration.
    nodes = resource.Body("nodes", type=list, list_type=Node)
    #: Number of available CPU cores
    allocatable_cpu_cores = resource.Body("allocatable_cpu_cores", type=str)
    #: Number of available memory resources
    allocatable_memory = resource.Body("allocatable_memory", type=str)
    #: Number of available GPU cores
    allocatable_gpus = resource.Body("allocatable_gpus", type=str)
    #: Product ID
    product_id = resource.Body("product_id", type=str)
    #: Order ID
    order_id = resource.Body("order_id", type=str)
    #: Subscription period type
    period_type = resource.Body("period_type", type=str)
    #: Number of subscription periods
    period_num = resource.Body("period_num", type=int)


class DedicatedResourcePool(resource.Resource):
    base_path = "/clusters"

    allow_list = True

    #: Total number of clusters that meet the search criteria
    #:  when no paging is implemented
    total_count = resource.Body("total_count", type=int)
    #: Number of clusters in the query result. If offset and limit
    #:  are not set, the values of count and total are the same.
    count = resource.Body("count", type=int)
    #: List of queried clusters.
    clusters = resource.Body("clusters", type=list, list_type=Cluster)
