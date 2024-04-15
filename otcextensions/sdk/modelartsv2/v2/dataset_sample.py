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
from openstack import exceptions
from openstack import resource
from openstack import utils
from otcextensions.sdk.modelartsv2.v2.dataset import DataSourceSpec


class SampleMetadataSpec(resource.Resource):
    #: Whether the sample is labeled as a hard sample, which is a default
    #:  attribute.
    hard = resource.Body("@modelarts:hard", type=float)
    #: Coefficient of difficulty of each sample level, which is a default
    #:  attribute.
    hard_coefficient = resource.Body("@modelarts:hard_coefficient", type=float)
    #: ID of a hard sample reason, which is a default attribute.
    hard_reasons = resource.Body(
        "@modelarts:hard_reasons", type=list, list_type=int
    )
    #: Image size (width, height, and depth of the image), which is a default
    #:  attribute, with type of List.
    size = resource.Body("@modelarts:size", type=list, list_type=int)


class SampleLabelPropertySpec(resource.Resource):
    #: Speech text content, which is a default attribute dedicated to the
    #:  speech label (including the speech content and speech start and end
    #:  points).
    content = resource.Body("@modelarts:content")
    #: End position of the text, which is a default attribute dedicated to the
    #:  named entity label.
    end_index = resource.Body("@modelarts:end_index", type=int)
    #: Speech end time, which is a default attribute dedicated to the speech
    #:  start/end point label, in the format of hh:mm:ss.
    end_time = resource.Body("@modelarts:end_time")
    #: Shape feature, which is a default attribute dedicated to the object
    #:  detection label, with type of List.
    feature = resource.Body("@modelarts:feature", type=dict)
    #: ID of the head entity in the triplet relationship label, which is a
    #:  default attribute dedicated to the triplet relationship label.
    from_id = resource.Body("@modelarts:from")
    #: Sample labeled as a hard sample or not, which is a default attribute.
    hard = resource.Body("@modelarts:hard")
    #: Coefficient of difficulty of each label level, which is a default
    #:  attribute.
    hard_coefficient = resource.Body("@modelarts:hard_coefficient")
    #: Reasons that the sample is a hard sample, which is a default attribute.
    hard_reasons = resource.Body("@modelarts:hard_reasons")
    #: Object shape, which is a default attribute dedicated to the object
    #:  detection label and is left empty by default.
    shape = resource.Body("@modelarts:shape")
    #: Speech source, which is a default attribute dedicated to the speech
    #:  start/end point label and can be set to a speaker or narrator.
    source = resource.Body("@modelarts:source")
    #: Start position of the text, which is a default attribute dedicated to
    #:  the named entity label.
    start_index = resource.Body("@modelarts:start_index", type=int)
    #: Speech start time, which is a default attribute dedicated to the speech
    #:  start/end point label, in the format of hh:mm:ss.
    start_time = resource.Body("@modelarts:start_time")
    #: ID of the tail entity in the triplet relationship label, which is a
    #:  default attribute dedicated to the triplet relationship label.
    to = resource.Body("@modelarts:to")


class SampleLabelSpec(resource.Resource):
    #: Video labeling method, which is used to distinguish whether a video is
    #:  labeled manually or automatically.
    annotated_by = resource.Body("annotated_by")
    #: Label ID.
    id = resource.Body("id")
    #: Label name.
    name = resource.Body("name")
    #: Attribute key-value pair of the sample label, such as the object shape
    #:  and shape feature.
    property = resource.Body("property", type=SampleLabelPropertySpec)
    #: Confidence.
    score = resource.Body("score", type=float)
    #: Label type.
    type = resource.Body("type", type=int)


class WorkerSpec(resource.Resource):
    #: Creation time.
    create_time = resource.Body("create_time", type=int)
    #: Labeling team member description.
    description = resource.Body("description")
    #: Email address of a labeling team member.
    email = resource.Body("email")
    #: Role.
    role = resource.Body("role", type=int)
    #: Current login status of a labeling team member.
    status = resource.Body("status", type=int)
    #: Update time.
    update_time = resource.Body("update_time", type=int)
    #: ID of a labeling team member.
    worker_id = resource.Body("worker_id")
    #: ID of a labeling team.
    workforce_id = resource.Body("workforce_id")


class HardDetailSpec(resource.Resource):
    #: Alias.
    alias_name = resource.Body("alo_name")
    #: Reason ID.
    id = resource.Body("id", type=int)
    #: Reason description.
    reason = resource.Body("reason")
    #: Handling suggestion.
    suggestion = resource.Body("suggestion")


class LabelFormatSpec(resource.Resource):
    #: Label type of text classification.
    label_type = resource.Body("label_type")
    #: Separator between labels.
    text_label_separator = resource.Body("text_label_separator")
    #: Separator between the text and label.
    text_sample_separator = resource.Body("text_sample_separator")


class SampleSpec(resource.Resource):
    # Video labeling method, which is used to distinguish
    #:  whether a video is labeled manually or automatically.
    annotated_by = resource.Body("annotated_by")
    #: Whether the acceptance is passed, which is used for team labeling.
    check_accept = resource.Body("check_accept", type=bool)
    #: Acceptance comment, which is used for team labeling.
    check_comment = resource.Body("check_comment")
    #: Acceptance score, which is used for team labeling.
    check_score = resource.Body("check_score")
    #: Byte data of sample files.
    data = resource.Body("data", type=dict)
    #: Data source.
    data_source = resource.Body("data_source", type=DataSourceSpec)
    #: Reason for deleting a sample, which is used for healthcare.
    deletion_reasons = resource.Body("deletion_reasons", type=list)
    #: Encoding type of sample files, which is used to upload .
    encoding = resource.Body("encoding")
    #: Check the document. Details about difficulties, including
    #:  description, causes, and suggestions of difficult problems.
    hard_details = resource.Body("hard_details")
    #: Labeling personnel list of sample assignment.
    labelers = resource.Body("labelers", type=list, list_type=WorkerSpec)
    #: Sample label list.
    labels = resource.Body("labels", type=list, list_type=SampleLabelSpec)
    #: Key-value pair of the sample metadata attribute.
    metadata = resource.Body("metadata", type=SampleMetadataSpec)
    #: Name of sample files.
    name = resource.Body("name")
    #: Preview dataset sample.
    preview = resource.Body("preview")
    #: Whether to accept the review, which is used for team labeling.
    review_accept = resource.Body("review_accept", type=bool)
    #: Review comment, which is used for team labeling.
    review_comment = resource.Body("review_comment")
    #: Review score, which is used for team labeling.
    review_score = resource.Body("review_score")
    #: Sample data list.
    sample_data = resource.Body("sample_data", type=list)
    #: Sample path.
    sample_dir = resource.Body("sample_dir")
    #: Sample ID.
    sample_id = resource.Body("sample_id")
    #: Sample name.
    sample_name = resource.Body("sample_name")
    #: Sample size or text length, in bytes.
    sample_size = resource.Body("sample_size", type=int)
    #: Sample status.
    sample_status = resource.Body("sample_status")
    #: Sample time, when OBS is last modified.
    sample_time = resource.Body("sample_time", type=int)
    #: Sample type.
    sample_type = resource.Body("sample_type", type=int)
    #: Comprehensive score, which is used for team labeling.
    score = resource.Body("score")
    #: Source address of sample data.
    source = resource.Body("source")
    #: Subsample URL, which is used for healthcare.
    sub_sample_url = resource.Body("sub_sample_url")
    #: ID of a labeling team member, which is used for team labeling.
    worker_id = resource.Body("worker_id")


class SampleRespSpec(resource.Resource):
    #: Error code.
    error_code = resource.Body("error_code")
    #: Error message.
    error_msg = resource.Body("error_msg")
    #: Description.
    info = resource.Body("info")
    #: Name of a sample file.
    name = resource.Body("name")
    #: Whether the operation is successful.
    success = resource.Body("success", type=bool)


class DatasetSample(SampleSpec):
    base_path = "/datasets/%(dataset_id)s/data-annotations/samples"

    resources_key = "samples"

    _query_mapping = resource.QueryParameters(
        "email",
        "high_score",
        "label_name",
        "label_type",
        "limit",
        "locale",
        "low_score",
        "offset",
        "order",
        "preview",
        "process_parameter",
        "sample_state",
        "sample_type",
        "search_conditions",
        "version_id",
    )

    # Capabilities
    allow_create = True
    allow_list = True
    allow_fetch = True

    # Properties
    #: Dataset ID.
    dataset_id = resource.URI("dataset_id")
    #: Whether to directly import to the final result.
    final_annotation = resource.Body("final_annotation", type=bool)
    #: Label format.
    label_format = resource.Body("label_format", type=LabelFormatSpec)
    #: Sample list.
    samples = resource.Body("samples", type=list, list_type=SampleSpec)
    #: Sample ID.
    sample_id = resource.Body("sample_id", alternate_id=True)

    #: Error code.
    error_code = resource.Body("error_code")
    #: Error message.
    error_msg = resource.Body("error_msg")
    #: Response list for adding samples in batches.
    results = resource.Body("results", type=list, list_type=SampleRespSpec)
    #: Whether the operation is successful.
    success = resource.Body("success", type=bool)

    def delete_samples(
        self, session, dataset_id, samples=[], delete_source=False
    ):
        """Delete dataset samples"""
        url = utils.urljoin(
            self.base_path % {"dataset_id": dataset_id}, "delete"
        )
        json_body = {"samples": samples}
        if delete_source:
            json_body.update(delete_source=True)
        response = session.post(url, json=json_body)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self
