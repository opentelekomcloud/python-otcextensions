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


class CurrentNodeDetailSpec(resource.Resource):
    #: Start time of the current task.
    begin_time = resource.Body('beginTime')
    #: Description of the current task.
    desc = resource.Body('desc')
    #: End time of the current task.
    end_time = resource.Body('endTime')
    #: Upgrade task name.
    name = resource.Body('name')
    #: Sequence number of an upgrade task.
    order = resource.Body('order', type=int)
    #: Status of the current task.
    status = resource.Body('status')


class GetTargetImageIdDetailSpec(resource.Resource):
    #: Image engine type.
    datastore_type = resource.Body('datastoreType')
    #: Image engine version.
    datastore_version = resource.Body('datastoreVersion')
    #: Name of an image that can be upgraded.
    display_name = resource.Body('displayName')
    #: ID of an image that can be upgraded.
    id = resource.Body('id')
    #: Image description.
    image_desc = resource.Body('imageDesc')
    #: Priority.
    priority = resource.Body('priority', type=int)


class ClusterUpgradeInfo(resource.Resource):
    base_path = '/clusters/%(cluster_id)s/upgrade/detail'

    allow_list = True

    resources_key = 'detailList'

    _query_mapping = resource.QueryParameters('start', 'limit', 'action_node')

    cluster_id = resource.URI('cluster_id')

    #: Agency name.
    agency_name = resource.Body('agencyName')
    #: Names of the nodes that have been upgraded.
    completed_nodes = resource.Body('completedNodes')
    #: Task details of the node that is being upgraded.
    current_node_detail = resource.Body(
        'currentNodeDetail', type=list, list_type=CurrentNodeDetailSpec
    )
    #: Names of the nodes that are being upgraded.
    current_node_name = resource.Body('currentNodeName')
    #: End time of the upgrade.
    end_time = resource.Body('endTime')
    #: Retried times.
    execute_times = resource.Body('executeTimes')
    #:
    fail_message = resource.Body('failMessage')
    #: Expected result of the cluster upgrade.
    final_az_info_map = resource.Body('finalAzInfoMap')
    #: Task ID.
    id = resource.Body('id')
    #: Image details.
    image_info = resource.Body('imageInfo', type=GetTargetImageIdDetailSpec)
    #: Current upgrade behavior of the cluster.
    migrate_param = resource.Body('migrateParam')
    #: Start time of the upgrade.
    start_time = resource.Body('startTime')
    #: Task status.
    status = resource.Body('status')
    #: Names of the nodes to be upgraded.
    total_nodes = resource.Body('totalNodes')
