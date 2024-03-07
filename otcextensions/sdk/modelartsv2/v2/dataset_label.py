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
from otcextensions.sdk.modelartsv2.v2.dataset import LabelSpec


class ResponseSpec(resource.Resource):
    #: Error code.
    error_code = resource.Body("error_code")
    #: Error message.
    error_msg = resource.Body("error_msg")
    #: Check whether the operation is successful.
    success = resource.Body("success", type=bool)


class DatasetLabel(LabelSpec):
    base_path = "datasets/%(datasetId)s/data-annotations/labels"

    resources_key = "labels"

    # capabilities
    allow_create = True
    allow_list = True
    allow_delete = True
    allow_fetch = True
    allow_commit = True

    #: Dataset ID.
    datasetId = resource.URI("datasetId")

    #: List of labels to be created.
    labels = resource.Body("labels", type=list, list_type=LabelSpec)

    #: Error code.
    error_code = resource.Body("error_code")
    #: Error message.
    error_msg = resource.Body("error_msg")
    #: Response body for creating a label.
    results = resource.Body("results", type=list, list_type=ResponseSpec)
    #: Check whether the operation is successful.
    success = resource.Body("success", type=bool)

    def update_labels(self, session, labels=[]):
        """Preform actions given the message body."""
        uri = self.base_path % self._uri.attributes
        body = {"labels": labels}
        response = session.put(uri, json=body)
        self._translate_response(response)
        return self
