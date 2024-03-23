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
from openstack import utils
from otcextensions.sdk.modelartsv1.v1.training_job import ConfigSpec


class TrainingJobVersion(ConfigSpec):
    base_path = "/training-jobs/%(jobId)s/versions"

    resources_key = "versions"

    # capabilities
    allow_create = True
    allow_delete = True
    allow_fetch = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        "limit",
        "offset",
        limit="per_page",
        offset="page",
    )

    #: Job ID
    jobId = resource.URI("jobId")

    #: Parameters for creating a training job For details, see Table 3.
    config = resource.Body("config", type=ConfigSpec)
    #: Description of a training job.
    job_desc = resource.Body("job_desc")
    #: Version ID of a training job.
    version_id = resource.Body("version_id", type=int, alternate_id=True)

    def stop(self, session):
        """Preform actions given the message body."""
        uri = utils.urljoin(
            self.base_path % self._uri.attributes, self.id, "stop"
        )
        response = session.post(uri, json=None)
        self._translate_response(response)
        return self
