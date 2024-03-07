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
import json

from openstack import exceptions
from openstack import resource


class SpecificationSpec(resource.Resource):
    #: Minimum CPU.
    min_cpu = resource.Body("min_cpu")
    #: Minimum GPU.
    min_gpu = resource.Body("min_gpu")
    #: Minimum memory capacity.
    min_memory = resource.Body("min_memory")


class HealthSpec(resource.Resource):
    #: After an instance is started, a health check starts after seconds
    #:  configured in initial_delay_seconds.
    initial_delay_seconds = resource.Body("initial_delay_seconds")
    #: Request protocol of the health check interface.
    protocol = resource.Body("protocol")
    #: Health check timeout.
    timeout_seconds = resource.Body("timeout_seconds")
    #: URL of the health check interface.
    url = resource.Body("url")


class OutputParamsSpec(resource.Resource):
    #: Properties of an object element in JSON Schema.
    properties = resource.Body("properties", type=dict)
    #: Type in JSON Schema, which can be object.
    type = resource.Body("type")


class InputParamsSpec(resource.Resource):
    #: Properties of an object element in JSON Schema.
    properties = resource.Body("properties", type=dict)
    #: Type in JSON Schema, which can be object.
    type = resource.Body("type")


class ApisSpec(resource.Resource):
    #: Input parameters in apis, described in JSON Schema format.
    input_params = resource.Body("input_params", type=InputParamsSpec)
    #: Request method.
    method = resource.Body("method")
    #: Output parameters in apis, described in JSON Schema format.
    output_params = resource.Body("output_params", type=OutputParamsSpec)
    #: Request protocol.
    protocol = resource.Body("protocol")
    #: Inference request URL.
    url = resource.Body("url")


class TemplateInputsSpec(resource.Resource):
    #: Template input path, which can be an OBS file path or OBS directory
    #:  path.
    input = resource.Body("input")
    #: Input item ID, which is obtained from the template details.
    input_id = resource.Body("input_id")


class TemplateSpec(resource.Resource):
    #: Input and output mode.
    infer_format = resource.Body("infer_format")
    #: ID of the used template.
    template_id = resource.Body("template_id")
    #: Template input configuration, specifying the source path for
    #:  configuring a model.
    template_inputs = resource.Body(
        "template_inputs", type=list, list_type=TemplateInputsSpec
    )


class DocSpec(resource.Resource):
    #: Document name, which must start with a letter.
    doc_name = resource.Body("doc_name")
    #: HTTP(S) link of the document.
    doc_url = resource.Body("doc_url")


class MetricSpec(resource.Resource):
    #: Accuracy.
    accuracy = resource.Body("accuracy", type=float)
    #: F1 score.
    f1 = resource.Body("f1", type=float)
    #: Precision.
    precision = resource.Body("precision", type=float)
    #: Recall.
    recall = resource.Body("recall", type=float)


class PackageSpec(resource.Resource):
    #: Name of a dependency package.
    package_name = resource.Body("package_name")
    #: Version of a dependency package.
    package_version = resource.Body("package_version")
    #: Version restriction.
    restraint = resource.Body("restraint")


class DependencySpec(resource.Resource):
    #: Installation mode.
    installer = resource.Body("installer")
    #: Collection of dependency packages.
    packages = resource.Body("packages", type=list, list_type=PackageSpec)


class ParamsSpec(resource.Resource):
    #: This parameter is optional when param_type is set to int or float.
    max = resource.Body("max", type=int)
    #: Request method.
    method = resource.Body("method")
    #: This parameter is optional when param_type is set to int or float.
    min = resource.Body("min", type=int)
    #: Parameter description.
    param_desc = resource.Body("param_desc")
    #: Parameter name.
    param_name = resource.Body("param_name")
    #: Parameter type.
    param_type = resource.Body("param_type")
    #: Request protocol.
    protocol = resource.Body("protocol")
    #: API URL.
    url = resource.Body("url")


class Model(resource.Resource):
    base_path = "/models"

    resources_key = "models"

    paginated = False

    # capabilities
    allow_create = True
    allow_list = True
    allow_delete = True
    allow_fetch = True

    _query_mapping = resource.QueryParameters(
        "name",
        "model_version",
        "status",
        "model_type",
        "not_model_type",
        "description",
        "offset",
        "marker",
        "limit",
        "sort_by",
        "order",
        "workspace_id",
        name="model_name",
        status="model_status",
    )

    # Properties
    #: AI project.
    ai_project = resource.Body("ai_project")
    #: All input and output apis parameter information of a model, which is
    #:  obtained from the model preview.
    apis = resource.Body("apis", type=list, list_type=ApisSpec)
    #: Model configurations.
    config = resource.Body("config")
    #: Time when a model is created, in milliseconds calculated from 1970.
    created_at = resource.Body("create_at", type=int)
    #: Package required for inference code and model.
    dependencies = resource.Body(
        "dependencies", type=list, list_type=DependencySpec
    )
    #: Model description.
    description = resource.Body("description")
    #: OBS path for storing the execution code. The name of the
    #:  execution code file is fixed to *customize_service.py*.
    execution_code = resource.Body("execution_code")
    #: Model health check interface information.
    health = resource.Body("health", type=HealthSpec)
    #: Character string converted from the final model configuration file.
    initial_config = resource.Body("initial_config")
    #: image path generated after model packaging.
    image_address = resource.Body("image_address")
    #: Collection of input parameters of a model.
    input_params = resource.Body(
        "input_params", type=list, list_type=ParamsSpec
    )
    #: Supported service type for deployment.
    install_type = resource.Body("install_type", type=list)
    #: Whether a model can be published to the marketplace.
    is_publishable = resource.Body("publishable_flag", type=bool)
    #: Whether a model is subscribed from the marketplace.
    is_subscribed = resource.Body("market_flag", type=bool)
    #: Whether a model can be tuned.
    is_tunable = resource.Body("tunable", type=bool)
    #: Model label map.
    labels_map = resource.Body("labels_map", type=dict)
    #: Model algorithm type. The value can be *predict_analysis*,
    #:  *object_detection*, or *image_classification*.
    model_algorithm = resource.Body("model_algorithm")
    #: List of model description documents.
    model_docs = resource.Body("model_docs", type=list, list_type=DocSpec)
    #: Model ID.
    model_id = resource.Body("model_id", alternate_id=True)
    #: Model label array.
    model_labels = resource.Body("model_labels", type=list)
    #: Model precision, which is read from the configuration file.
    model_metrics = resource.Body("model_metrics")
    #: Model name.
    model_name = resource.Body("model_name")
    #: Model size, in bytes.
    model_size = resource.Body("model_size", type=int)
    #: Model source.
    model_source = resource.Body("model_source")
    #: Model status.
    model_status = resource.Body("model_status")
    #: Model type. The value can be *TensorFlow*, *MXNet*, *Spark_MLlib*,
    #:  *Scikit_Learn*, *XGBoost*, *Image*, or *PyTorch*.
    model_type = resource.Body("model_type")
    #: Model version.
    model_version = resource.Body("model_version")
    #: Model name.
    name = resource.Body("name", alias="model_name")
    #: Collection of output parameters of a model.
    output_params = resource.Body(
        "output_params", type=list, list_type=ParamsSpec
    )
    #: User to which a model belongs.
    owner_id = resource.Body("owner")
    #: Project to which a model belongs.
    project_id = resource.Body("project")
    #: Model runtime environment.
    runtime = resource.Body("runtime")
    #: Download address of the model schema file.
    schema_doc = resource.Body("schema_doc")
    #: ID of the source training job.
    source_job_id = resource.Body("source_job_id")
    #: Version of the source training job.
    source_job_version = resource.Body("source_job_version")
    #: OBS path where the model is located or the SWR image location.
    source_location = resource.Body("source_location")
    #: Model source type. If a model is deployed through ExeML, the value is
    #:  auto. If a model is deployed through a training job or an OBS model
    #:  file, this parameter is left blank.
    source_type = resource.Body("source_type")
    #: Minimum model deployment specifications.
    specification = resource.Body("specification", type=SpecificationSpec)
    #: Template configuration items.
    template = resource.Body("template", type=TemplateSpec)
    #: Model status.
    status = resource.Body("status", alias="model_status")
    #: Tenant to which a model belongs.
    tenant_id = resource.Body("tenant")
    #: Model version.
    version = resource.Body("version", alias="model_version")
    #: ID of the workspace to which a service belongs.
    workspace_id = resource.Body("workspace_id")

    def _translate_response(self, response, has_body=None, error_message=None):
        """Given a KSA response, inflate this instance with its data
        DELETE operations don't return a body, so only try to work
        with a body when has_body is True.
        This method updates attributes that correspond to headers
        and body on this instance and clears the dirty set.
        """
        if has_body is None:
            has_body = self.has_body

        exceptions.raise_from_response(response, error_message=error_message)

        if has_body:
            try:
                body = response.json()
                if self.resource_key and self.resource_key in body:
                    body = body[self.resource_key]
                for key in (
                    "model_metrics",
                    "config",
                    "apis",
                    "output_params",
                    "input_params",
                ):
                    if key in body:
                        if isinstance(body[key], str):
                            body[key] = json.loads(body[key])
                        elif key in (
                            "output_params",
                            "input_params",
                        ) and isinstance(body[key], list):
                            for param in body[key]:
                                if isinstance(param.get("param_desc"), str):
                                    param["param_desc"] = json.loads(
                                        param["param_desc"]
                                    )

                # Do not allow keys called "self" through. Glance chose
                # to name a key "self", so we need to pop it out because
                # we can't send it through cls.existing and into the
                # Resource initializer. "self" is already the first
                # argument and is practically a reserved word.
                body.pop("self", None)
                body_attrs = self._consume_body_attrs(body)
                if self._allow_unknown_attrs_in_body:
                    body_attrs.update(body)
                    self._unknown_attrs_in_body.update(body)
                elif self._store_unknown_attrs_as_properties:
                    body_attrs = self._pack_attrs_under_properties(
                        body_attrs, body
                    )

                self._body.attributes.update(body_attrs)
                self._body.clean()
                if self.commit_jsonpatch or self.allow_patch:
                    # We need the original body to compare against
                    self._original_body = body_attrs.copy()
            except ValueError:
                # Server returned not parse-able response (202, 204, etc)
                # Do simply nothing
                pass

        headers = self._consume_header_attrs(response.headers)
        self._header.attributes.update(headers)
        self._header.clean()
