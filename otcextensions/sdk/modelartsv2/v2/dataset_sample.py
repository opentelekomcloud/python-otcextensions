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


class WorkerSpec(resource.Resource):
    #: Creation time.
    created_at = resource.Body("create_time", type=int)
    #: Labeling team member description.
    description = resource.Body("description")
    #: Email address of a labeling team member.
    email = resource.Body("email")
    #: Role.
    role = resource.Body("role", type=int)
    #: Current login status of a labeling team member.
    status = resource.Body("status")
    #: Update time.
    updated_at = resource.Body("update_time", type=int)
    #: ID of a labeling team member.
    worker_id = resource.Body("worker_id", alternate_id=True)
    #: ID of a labeling team.
    workforce_id = resource.Body("workforce_id")


class SampleLabelSpec(resource.Resource):
    #: Video labeling method, which is used to distinguish whether a
    #:  video is labeled manually or automatically.
    annotated_by = resource.Body("annotated_by")
    #: Attribute key-value pair of the sample label, such as the object
    #:  shape and shape feature.
    property = resource.Body("property", type=dict)
    #: Confidence.
    score = resource.Body("score", type=float)
    #: Label type.
    type = resource.Body("type", type=int)


class DatasetSample(resource.Resource):
    base_path = "/datasets/%(dataset_id)s/data-annotations/samples"

    resource_key = "sample"
    resources_key = "samples"

    allow_create = True
    allow_list = True
    allow_fetch = True

    #: Dataset ID
    dataset_id = resource.URI("dataset_id", type=str)

    # Video labeling method, which is used to distinguish
    #:  whether a video is labeled manually or automatically.
    annotated_by = resource.Body("annotated_by")
    #: Whether the acceptance is passed, which is used for team labeling.
    is_acceptance_passed = resource.Body("check_accept")
    #: Acceptance comment, which is used for team labeling.
    check_comment = resource.Body("check_comment")
    #: Acceptance score, which is used for team labeling.
    check_score = resource.Body("check_score")
    #: Reason for deleting a sample, which is used for healthcare.
    deletion_reasons = resource.Body("deletion_reasons", type=list)
    #: Details about difficulties, including description, causes,
    #:  and suggestions of difficult problems.
    hard_details = resource.Body("hard_details", type=dict)
    #: Labeling personnel list of sample assignment. The labelers
    #:  record the team members to which the sample is allocated
    #:  for team labeling.
    labelers = resource.Body("labelers", type=list, list_type=WorkerSpec)
    #: Sample label list.
    labels = resource.Body("labels", type=list, list_type=SampleLabelSpec)
    #: Key-value pair of the sample metadata attribute.
    metadata = resource.Body("metadata", type=dict)
    #: Whether to accept the review, which is used for team labeling.
    is_preview_supported = resource.Body("preview", type=bool)
    is_review_accepted = resource.Body("review_accept", type=bool)
    #: Review comment, which is used for team labeling.
    review_comment = resource.Body("review_comment")
    #: Review score, which is used for team labeling.
    review_score = resource.Body("review_score")
    #: Sample data list.
    sample_data = resource.Body("sample_data", type=list)
    #: Sample path.
    sample_dir = resource.Body("sample_dir")
    #: Sample ID.
    sample_id = resource.Body("sample_id", alternate_id=True)
    #: Sample name.
    sample_name = resource.Body("sample_name", alias="name")
    name = resource.Body("name", alias="sample_name")
    #: Sample size or text length, in bytes.
    sample_size = resource.Body("sample_size", type=int)
    #: Sample status.
    sample_status = resource.Body("sample_status")
    #: Sample time, when OBS is last modified.
    sample_time = resource.Body("sample_time", type=int, alias="updated_at")
    updated_at = resource.Body("updated_at", type=int, alias="sample_time")
    #: Sample type.
    sample_type = resource.Body("sample_type")  # type=SampleTypeEnum)
    #: Comprehensive score, which is used for team labeling.
    score = resource.Body("score")
    #: Source address of sample data.
    source = resource.Body("source")
    #: Subsample URL, which is used for healthcare.
    sub_sample_url = resource.Body("sub_sample_url")
    #: ID of a labeling team member, which is used for team labeling.
    worker_id = resource.Body("worker_id")

    def delete_samples(self, session, sample_ids=[], delete_source=False):
        """Deleting Samples in Batches"""
        url = utils.urljoin(self.base_path, "delete")
        body = {"samples": sample_ids}
        headers = {
            "Accept": "application/json",
            "Content-type": "application/json",
        }
        if delete_source:
            body.update(delete_source=delete_source)
        res = session.post(url, json=body, headers=headers)
        self._translate_response(res, has_body=False)
        return self
