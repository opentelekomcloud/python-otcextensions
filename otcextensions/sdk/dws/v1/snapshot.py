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
from otcextensions.sdk.dws.v1 import cluster as _cluster


class Snapshot(resource.Resource):
    base_path = '/snapshots'

    resource_key = 'snapshot'
    resources_key = 'snapshots'

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_delete = True
    allow_list = True

    # Properties
    #: ID of the cluster for which snapshots are created.
    cluster_id = resource.Body('cluster_id')
    #: Time when a snapshot starts to be created.
    created_at = resource.Body('started')
    #: Snapshot description.
    description = resource.Body('description')
    #: Snapshot size, in GB.
    size = resource.Body('size', type=float)
    #: Snapshot status:
    #:  - CREATING
    #:  - AVAILABLE
    #:  - UNAVAILABLE
    status = resource.Body('status')
    #: Snapshot type. It can be:
    #:  - MANUAL
    #:  - AUTOMATED
    type = resource.Body('type')
    #: Time when a snapshot is complete.
    updated_at = resource.Body('finished')


class Restore(_cluster.Cluster):
    base_path = '/snapshots/%(snapshot_id)s/actions'

    resources_key = None
    resource_key = 'restore'

    snapshot_id = resource.URI('snapshot_id')

    # capabilities
    allow_create = True
    allow_fetch = False
    allow_delete = False
    allow_list = False
    allow_commit = False
    allow_patch = False

    #: Returns `~otcextensions.sdk.dws.v1.cluster.Cluster` object.
    cluster = resource.Body('cluster', type=_cluster.Cluster)
