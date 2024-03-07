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


class ScheduleSpec(resource.Resource):
    #: Auto stop duration.
    duration = resource.Body("duration", type=int)
    #: Unit of auto stop duration.
    time_unit = resource.Body("time_unit")
    #: Set this parameter to stop.
    type = resource.Body("type")


class FlavorSpec(resource.Resource):
    #: Resource specification code of a visualization job.
    code = resource.Body("code")


class VisualizationJob(resource.Resource):
    base_path = "/visualization-jobs"

    resources_key = "jobs"

    # capabilities
    allow_create = True
    allow_list = True
    allow_commit = True
    allow_delete = True
    allow_fetch = True

    _query_mapping = resource.QueryParameters(
        "order",
        "offset",
        "limit",
        "search_content",
        "sort_by",
        "status",
        offset="page",
        limit="per_page",
    )

    # Parameters
    #: Time when a visualization job is created, in timestamp format.
    created_at = resource.Body("create_time", type=int)
    #: Visualization job running duration, in milliseconds.
    duration = resource.Body("duration", type=int)
    #: Error code of a failed API call.
    error_code = resource.Body("error_code")
    #: Error message of a failed API call.
    error_message = resource.Body("error_message")
    #: Specifications when a visualization job is created.
    flavor = resource.Body("flavor", type=FlavorSpec)
    #: Whether the request is successful
    is_success = resource.Body("is_success", type=bool)
    #: Description of a visualization job.
    job_desc = resource.Body("job_desc")
    #: ID of a visualization job.
    job_id = resource.Body("job_id", type=int, alternate_id=True)
    #: Name of a visualization job.
    job_name = resource.Body("job_name")
    #: Type of a visualization job.
    job_type = resource.Body("job_type")
    #: Name of a visualization job.
    name = resource.Body("name", alias="job_name")
    #: Remaining auto stop duration
    remaining_duration = resource.Body("remaining_duration", type=float)
    #: Charged resource ID of a visualization job.
    resource_id = resource.Body("resource_id")
    #: Auto stop setting.
    schedule = resource.Body("schedule", type=ScheduleSpec)
    #: Endpoint of a visualization job.
    service_url = resource.Body("service_url")
    #: Status of a visualization job.
    status = resource.Body("status", type=int)
    #: OBS path of the visualization job output file.
    train_url = resource.Body("train_url")

    def _action(self, session, action, body=None):
        """Preform actions given the message body."""
        uri = utils.urljoin("visualization-jobs", self.id, action)
        response = session.post(uri, json=body)
        self._translate_response(response)
        return self

    def restart(self, session):
        """Restart the Visualization job."""
        self._action(session, "restart")

    def stop(self, session):
        """Restart the Visualization job."""
        self._action(session, "stop")
