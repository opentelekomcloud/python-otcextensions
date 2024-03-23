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


class NodeSpec(resource.Resource):
    #: Number of available nodes.
    available_count = resource.Body("available_count", type=int)
    #: Number of nodes.
    count = resource.Body("count", type=int)
    #: Node specifications.
    specification = resource.Body("specification")


class ServiceCluster(resource.Resource):
    base_path = "/clusters"

    resources_key = "clusters"

    # capabilities
    allow_list = True

    _query_mapping = resource.QueryParameters(
        "project_id",
        "name",
        "status",
        "marker",
        "limit",
        "sort_by",
        "order",
        cluster_name="name",
        offset="marker",
    )

    # Properties
    #: Number of available CPU cores.
    allocatable_cpu_cores = resource.Body("allocatable_cpu_cores", type=float)
    #: Number of available GPU cores.
    allocatable_gpus = resource.Body("allocatable_gpus", type=float)
    #: Number of available memory resources.
    allocatable_memory = resource.Body("allocatable_memory", type=int)
    #: Charging Mode.
    charging_mode = resource.Body("charging_mode")
    #: Cluster ID.
    cluster_id = resource.Body("cluster_id")
    #: Cluster name.
    cluster_name = resource.Body("cluster_name")
    #: Time when a cluster is created, in milliseconds calculated
    #:  from 1970.1.1 0:0:0 UTC.
    created_at = resource.Body("created_at", type=int)
    #: Cluster description.
    description = resource.Body("description")
    #: Max Node Count.
    max_node_count = resource.Body("max_node_count", type=int)
    #: Node configuration.
    nodes = resource.Body("nodes", type=NodeSpec)
    #: Order ID.
    order_id = resource.Body("order_id")
    #: User to which a cluster belongs.
    owner = resource.Body("owner")
    #: Number of subscription periods.
    period_num = resource.Body("period_num", type=int)
    #: Subscription period type.
    period_type = resource.Body("period_type")
    #: Product ID.
    product_id = resource.Body("product_id")
    #: Project to which a cluster belongs.
    project = resource.Body("project")
    #: Services Count
    services_count = resource.Body("services_count", type=dict)
    #: Cluster status. The value can be
    #:  `deploying`, `running`, `concerning`, or `abnormal`.
    status = resource.Body("status")
    #: Tenant to which a cluster belongs.
    tenant = resource.Body("tenant")
