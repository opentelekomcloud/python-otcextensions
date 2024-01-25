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


class Sync(resource.Resource):
    base_path = "/datasets/%(datasetId)s/sync-data"

    allow_create = True
    allow_fetch = True

    # Resource Key
    #: Dataset ID.
    datasetId = resource.URI("datasetId")

    # Properties
    #: Number of added samples.
    add_sample_count = resource.Body("add_sample_count", type=int)
    #: Task creation time.
    create_time = resource.Body("create_time", type=int)
    #: Dataset ID.
    dataset_id = resource.Body("dataset_id")
    #: Number of deleted samples.
    deleted_sample_count = resource.Body("deleted_sample_count", type=int)
    #: Task running time.
    duration_time = resource.Body("duration_time", type=int)
    #: Error code of a failed API call. For details, see Error Code.
    #:  This parameter is not included when the API call succeeds.
    error_code = resource.Body("error_code", type=str)
    #: Error message of a failed API call.
    #:  This parameter is not included when the API call succeeds.
    error_msg = resource.Body("error_msg", type=str)
    #: Status of a data synchronization task. Possible values are as follows:
    #: \nQUEUING
    #: \nSTARTING
    #: \nRUNNING
    #: \nFAILED
    #: \nCOMPLETED
    #: \nNOT_EXIST
    status = resource.Body("status")
    #: Synchronization task ID.
    task_id = resource.Body("task_id")
    #: Total number of samples.
    total_sample_count = resource.Body("total_sample_count", type=int)
