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
from openstack import exceptions
from openstack import resource
from openstack import utils


class Cluster(resource.Resource):
    base_path = '/clusters'

    resource_key = 'cluster'
    resources_key = 'clusters'

    # capabilities
    allow_create = True
    allow_list = True
    allow_commit = True
    allow_delete = True
    allow_fetch = True
    allow_patch = True

    # Properties
    #: The key indicates an ongoing task.
    action_progress = resource.Body('action_progress', type=dict)
    #: Availabilitu Zone of a Cluster
    availability_zone = resource.Body('availability_zone')
    #: Cluster creation time.
    created_at = resource.Body('created')
    #: Private network connection information about the cluster.
    endpoints = resource.Body('endpoints', type=list, list_type=dict)
    #: Enterprise project ID.
    #: If no enterprise project is specified for a cluster,
    #: the default enterprise project ID 0 is used.
    enterprise_project_id = resource.Body('enterprise_project_id')
    #: Cause of failure. If the parameter is left empty,
    #:  the cluster is in the normal state.
    error = resource.Body('failed_reasons', type=dict)
    #: Node Type (DWS Flavor).
    flavor = resource.Body('node_type')
    #: Node Type ID (DWS Flavor ID).
    flavor_id = resource.Body('node_type_id')
    #: Floating IP details
    floating_ip = resource.Body('public_ip', type=dict)
    #: Guest Agent Version
    guest_agent_version = resource.Body('guest_agent_version')
    #: Whether logical_cluster has been enabled.
    is_logical_cluster_enabled = resource.Body(
        'use_logical_cluster', type=bool)
    #: Whether logical_cluster has been initialed
    is_logical_cluster_initialed = resource.Body(
        'logical_cluster_initialed', type=bool)
    #: Whether logical_cluster_mode is set ``true``.
    is_logical_cluster_mode = resource.Body('logical_cluster_mode', type=bool)
    #: The number of latest manual snapshots that
    #:  need to be retained for a cluster.
    keep_last_manual_snapshot = resource.Body(
        'keep_last_manual_snapshot', type=int)
    #: Cluster maintenance window.
    maintenance_window = resource.Body('maintain_window', type=dict)
    #: Network ID, which is used for configuring cluster network.
    network_id = resource.Body('subnet_id')
    #: Nodes List.
    nodes = resource.Body('nodes', type=list)
    #: Number of deployed CNs.
    num_cn = resource.Body('number_of_cn', type=int)
    #: Number of events.
    num_recent_events = resource.Body('recent_event', type=int)
    #: number_of_free_node
    num_free_nodes = resource.Body('number_of_free_node', type=int)
    #: Number of nodes in a cluster. The value ranges from 3 to 32.
    num_nodes = resource.Body('number_of_node')
    #: Parameter group details.
    parameter_group = resource.Body('parameter_group', type=dict)
    #: plugins
    plugins = resource.Body('plugins', type=list)
    #: Service port of a cluster. The value ranges from 8000 to 30000.
    #: The default value is 8000.
    port = resource.Body('port')
    #: List of private network IP addresses.
    private_ip = resource.Body('private_ip', type=list)
    #: Public network connection information about the cluster.
    public_endpoints = resource.Body('public_endpoints',
                                     type=list, list_type=dict)
    #: Cluster scale-out details.
    resize_info = resource.Body('resize_info', type=dict)
    #: Router ID, which is used for configuring cluster network.
    router_id = resource.Body('vpc_id')
    #: Cluster status. The value can be one of the following:
    #:  - CREATING
    #:  - AVAILABLE
    #:  - UNAVAILABLE
    #:  - CREATION FAILED
    status = resource.Body('status')
    #: Sub-status of clusters in the AVAILABLE state.
    sub_status = resource.Body('sub_status')
    #: spec_version
    spec_version = resource.Body('spec_version')
    #: ID of a security group, which is used for configuring cluster network
    security_group_id = resource.Body('security_group_id')
    #: Cluster management task.
    task_status = resource.Body('task_status')
    #: Labels in a cluster.
    tags = resource.Body('tags', type=list, list_type=dict)
    #: Administrator username for logging in to a data warehouse cluster.
    user_name = resource.Body('user_name')
    #: Last modification time of a cluster.
    updated_at = resource.Body('updated')
    #: Data warehouse version.
    version = resource.Body('version')

    # Computed Resources
    #: Private Domain from endpoints connection_info
    private_domain = resource.Computed('private_domain', default='')
    #: Public Domain from public_endpoints connection_info
    public_domain = resource.Computed('public_domain', default='')

    def _action(self, session, action, body=None):
        """Preform actions given the message body.
        """
        uri = utils.urljoin('clusters', self.id, action)
        response = session.post(uri, json=body)
        exceptions.raise_from_response(response)

    def restart(self, session):
        """Restart the cluster.
        """
        self._action(session, 'restart', {"restart": {}})

    def extend(self, session, node_count):
        """Scale Out cluster Nodes.
        """
        self._action(session, 'resize',
                     {'scale_out': {'count': node_count}})

    def reset_password(self, session, new_password):
        """Reset Admin DB Password.
        """
        self._action(session, 'reset-password',
                     {'new_password': new_password})

    def remove(self, session, keep_last_manual_snapshot=0):
        """Delete a DWS Cluster.
        """
        uri = utils.urljoin('clusters', self.id)
        data = {
            "keep_last_manual_snapshot": keep_last_manual_snapshot
        }
        return session.delete(uri, json=data)
