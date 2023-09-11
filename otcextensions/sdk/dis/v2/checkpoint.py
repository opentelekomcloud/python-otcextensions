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
from openstack import resource


class Checkpoint(resource.Resource):
    base_path = '/checkpoints'

    allow_create = True
    allow_delete = True
    allow_fetch = True

    # Properties
    #: Name of the app, which is the unique identifier of a user data "
    #:  consumption program.
    app_name = resource.Body('app_name')
    #: Type of the checkpoint
    #:  \nLAST_READ: Only sequence numbers are recorded in databases.
    checkpoint_type = resource.Body('checkpoint_type')
    #: Metadata information of the consumer application.
    #:  The metadata information can contain a maximum of 1,000 characters.
    metadata = resource.Body('metadata')
    #: Partition ID of the stream.
    partition_id = resource.Body('partition_id')
    #: Sequence number to be submitted, which is used to record the
    #:  consumption checkpoint of the stream.
    sequence_number = resource.Body('sequence_number')
    #: Name of the stream.
    stream_name = resource.Body('stream_name')

    def get_checkpoint(self, session, **params):
        """Querying Checkpoint Details.
        """
        response = session.get(self.base_path, params=params)
        self._translate_response(response)
        return self

    def delete_checkpoint(self, session, **params):
        """Deleting Checkpoint.
        """
        response = session.delete(self.base_path, params=params)
        self._translate_response(response, has_body=False)
        return self
