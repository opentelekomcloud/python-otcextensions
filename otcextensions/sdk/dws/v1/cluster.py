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


class PublicIP(resource.Resource):
    #: Binding type of an EIP. The value can be one of the following:
    #:  - auto_assign
    #:  - not_use
    #:  - bind_existing
    public_bind_type = resource.Body('public_bind_type')
    #: EIP ID
    eip_id = resource.Body('eip_id')
    #: EIP Address
    eip_address = resource.Body('eip_address')


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
    #: Cluster name.
    name = resource.Body('name')
    #: Administrator username for logging in to a data warehouse cluster.
    user_name = resource.Body('user_name')
    #: Data warehouse version.
    version = resource.Body('version')
    #: Node Type (DWS Flavor).
    flavor = resource.Body('node_type')
    #: Node Type ID (DWS Flavor ID).
    flavor_id = resource.Body('node_type_id')
    #: Nodes List.
    nodes = resource.Body('nodes', type=list)
    #: Number of nodes in a cluster. The value ranges from 3 to 32.
    number_of_node = resource.Body('number_of_node')
    #: number_of_free_node
    number_of_free_node = resource.Body('number_of_free_node', type=int)
    #: Cluster status. The value can be one of the following:
    #:  - CREATING
    #:  - AVAILABLE
    #:  - UNAVAILABLE
    #:  - CREATION FAILED
    status = resource.Body('status')
    #: Sub-status of clusters in the AVAILABLE state.
    sub_status = resource.Body('sub_status')
    #: Cluster management task.
    task_status = resource.Body('task_status')
    #: The key indicates an ongoing task.
    action_progress = resource.Body('action_progress')
    #: Last modification time of a cluster.
    updated_at = resource.Body('updated')
    #: Number of events.
    recent_event = resource.Body('recent_event', type=int)
    #: spec_version
    spec_version = resource.Body('spec_version')
    #: Cluster creation time.
    created_at = resource.Body('created')
    #: Availabilitu Zone of a Cluster
    availability_zone = resource.Body('availability_zone')
    #: Service port of a cluster. The value ranges from 8000 to 30000.
    #: The default value is 8000.
    port = resource.Body('port')
    #: List of private network IP addresses.
    private_ip = resource.Body('private_ip', type=list)
    #: Router ID, which is used for configuring cluster network.
    router_id = resource.Body('vpc_id')
    #: Network ID, which is used for configuring cluster network.
    network_id = resource.Body('subnet_id')
    #: ID of a security group, which is used for configuring cluster network
    security_group_id = resource.Body('security_group_id')
    #: Cluster maintenance window.
    maintain_window = resource.Body('maintain_window', type=dict)
    #: Parameter group details.
    parameter_group = resource.Body('parameter_group', type=dict)
    #: Public IP address. If the parameter is not specified,
    #:  public connection is not used by default.
    public_ip = resource.Body('public_ip', type=PublicIP)
    floating_ip_address = resource.Computed('floating_ip_address', default='')
    floating_ip_id = resource.Computed('floating_ip_id', default='')
    #: Private network connection information about the cluster.
    endpoints = resource.Body('endpoints', type=list, list_type=dict)
    private_domain = resource.Computed('private_domain', default='', type=list)
    #: Public network connection information about the cluster.
    public_endpoints = resource.Body('public_endpoints',
                                     type=list, list_type=dict)
    public_domain = resource.Computed('public_domain', default='', type=list)
    #: plugins
    plugins = resource.Body('plugins', type=list)
    #: Labels in a cluster.
    tags = resource.Body('tags', type=list, list_type=dict)
    #: Enterprise project ID.
    #: If no enterprise project is specified for a cluster,
    #: the default enterprise project ID 0 is used.
    enterprise_project_id = resource.Body('enterprise_project_id')
    #: Cluster scale-out details.
    resize_info = resource.Body('resize_info', type=dict)
    #: Guest Agent Version
    guest_agent_version = resource.Body('guest_agent_version')
    #: use_logical_cluster
    use_logical_cluster = resource.Body('use_logical_cluster', type=bool)
    #: logical_cluster_initialed
    logical_cluster_initialed = resource.Body(
        'logical_cluster_initialed', type=bool)
    #: logical_cluster_mode
    logical_cluster_mode = resource.Body('logical_cluster_mode', type=bool)

    #: The number of latest manual snapshots that
    #:  need to be retained for a cluster.
    keep_last_manual_snapshot = resource.Body(
        'keep_last_manual_snapshot', type=int)

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
