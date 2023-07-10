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
# import six
from openstack import exceptions
from openstack import resource
from openstack import utils


class ProcessingSchemaSpec(resource.Resource):
    # Properties
    #: Attribute name of the source data timestamp.
    timestamp_name = resource.Body('timestamp_name')
    #: Type of the source data timestamp.
    timestamp_type = resource.Body('timestamp_type')
    #: OBS directory generated based on the timestamp format. This parameter
    #:  is mandatory when the timestamp type of the source data is String.
    #: \nValues:
    #: \nyyyy/MM/dd HH:mm:ss
    #: \nMM/dd/yyyy HH:mm:ss
    #: \ndd/MM/yyyy HH:mm:ss
    #: \nyyyy-MM-dd HH:mm:ss
    #: \nMM-dd-yyyy HH:mm:ss
    #: \ndd-MM-yyyy HH:mm:ss
    timestamp_format = resource.Body('timestamp_format')


class ObsDestinationSpec(resource.Resource):

    # Properties
    #: Name of the agency created on IAM. DIS uses an agency to
    #:  access your specified resources.
    agency_name = resource.Body('agency_name')
    #: Offset. Types:
    #: \nLATEST: Maximum offset, indicating that the latest data will
    #:  be extracted. \nTRIM_HORIZON: Minimum offset, indicating
    #:  that the earliest data will be extracted.
    consumer_strategy = resource.Body('consumer_strategy')
    #: User-defined interval at which data is imported from the
    #:  current DIS stream into OBS.
    deliver_time_interval = resource.Body('deliver_time_interval', type=int)
    #: Dump file format. Possible values:
    #: \nText (default)
    destination_file_type = resource.Body('destination_file_type')
    #: Directory to store files that will be dumped to OBS. Different directory
    #:  levels are separated by slashes (/) and cannot start with slashes.
    file_prefix = resource.Body('file_prefix')
    #: Name of the OBS bucket used to store data from the DIS stream.
    obs_bucket_path = resource.Body('obs_bucket_path')
    #: Directory structure of the object file written into OBS. The directory
    #:  structure is in the format of yyyy/MM/dd/HH/mm (time at which the
    #:  dump task was created).
    partition_format = resource.Body('partition_format')
    #: Dump time directory generated based on the timestamp of the
    #:  source data and the configured partition_format.
    processing_schema = resource.Body('processing_schema', type=dict,
                                      dict_type=ProcessingSchemaSpec)
    #: Delimiter for the dump file, which is used to separate the
    #:  user data that is written into the dump file.
    record_delimiter = resource.Body('record_delimiter')
    #: Name of the dump task.
    task_name = resource.Body('task_name')


class DumpTask(resource.Resource):
    base_path = '/streams/%(uri_stream_name)s/transfer-tasks'

    resources_key = 'tasks'

    allow_create = True
    allow_list = True
    allow_commit = True
    allow_delete = True
    allow_fetch = True
    allow_patch = True

    #: Name of the stream to which the dump task belongs.
    uri_stream_name = resource.URI('uri_stream_name')

    # Properties
    #: Time when the dump task is created.
    created_at = resource.Body('create_time')
    #: Dump destination. Possible values:
    #: \nOBS: Data is dumped to OBS.
    destination_type = resource.Body('destination_type')
    #: Exception Strategy
    exception_strategy = resource.Body('exception_strategy')
    #: Latest dump time of the dump task.
    last_transfer_timestamp = resource.Body('last_transfer_timestamp')
    #: Parameter list of OBS to which data in the DIS stream will be dumped.
    obs_destination_descriptor = resource.Body('obs_destination_descriptor',
                                               type=dict,
                                               dict_type=ObsDestinationSpec)
    #: Parameter list of OBS to which data in the DIS stream will be dumped.
    obs_destination_description = resource.Body('obs_destination_description',
                                                type=dict,
                                                dict_type=ObsDestinationSpec)
    #: List of partition dump details.
    partitions = resource.Body('partitions', type=list, list_type=dict)
    #: Dump task status. Possible values:
    #: \nERROR: An error occurs.
    #: \nSTARTING: The dump task is being started.
    #: \nPAUSED: The dump task has been stopped.
    #: \nRUNNING: The dump task is running.
    #: \nDELETE: The dump task has been deleted.
    #: \nABNORMAL: The dump task is abnormal.
    status = resource.Body('state')
    #: ID of the stream to which the dump task belongs.
    stream_id = resource.Body('stream_id')
    #: Name of the stream to which the dump task belongs.
    stream_name = resource.Body('stream_name')
    #: ID of the dump task.
    task_id = resource.Body('task_id', alternate_id=True)
    #: Name of the dump task.
    task_name = resource.Body('task_name')

    def _action(self, session, stream_name, action, *task_id):
        """Perform start or stop action on the give dump tasks.
        """
        uri = utils.urljoin('streams', stream_name, 'transfer-tasks/action')
        tasks = [{'id': i} for i in list(*task_id)]
        body = {
            'action': action,
            'tasks': tasks
        }
        response = session.post(uri, json=body)
        exceptions.raise_from_response(response)
