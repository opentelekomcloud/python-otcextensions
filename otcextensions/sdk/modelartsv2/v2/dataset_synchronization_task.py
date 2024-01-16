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


class SynchronizeDataset(resource.Resource):
    base_path = "/datasets/%(dataset_id)s/sync-data"
    dataset_id = resource.URI("dataset_id", type=str)
    allow_create = True


class DatasetSynchronizationTask(resource.Resource):
    base_path = "/datasets/%(dataset_id)s/sync-data/status"

    allow_list = True

    #: Status of a data synchronization task. Possible values are as follows:
    #:  QUEUING
    #:  STARTING
    #:  RUNNING
    #:  FAILED
    #:  COMPLETED
    #:  NOT_EXIST
    status = resource.Body("status", type=str)
    #: Dataset ID
    dataset_id = resource.URI("dataset_id", type=str)
    #: Error code of a failed API call. For details, see Error Code.
    #:  This parameter is not included when the API call succeeds.
    error_code = resource.Body("error_code", type=str)
    #: Error message of a failed API call.
    #:  This parameter is not included when the API call succeeds.
    error_msg = resource.Body("error_msg", type=str)
