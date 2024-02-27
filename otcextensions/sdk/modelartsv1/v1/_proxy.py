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
import time

from openstack import exceptions
from openstack import proxy
from otcextensions.sdk.modelartsv1.v1 import \
    builtin_algorithms as _builtin_algorithms
from otcextensions.sdk.modelartsv1.v1 import devenv as _devenv
from otcextensions.sdk.modelartsv1.v1 import \
    job_engine_specifications as _job_engine_specifications
from otcextensions.sdk.modelartsv1.v1 import \
    job_resource_specifications as _job_resource_specifications
from otcextensions.sdk.modelartsv1.v1 import model as _model
from otcextensions.sdk.modelartsv1.v1 import service as _service
from otcextensions.sdk.modelartsv1.v1 import training_job as _training_job
from otcextensions.sdk.modelartsv1.v1 import \
    visualization_job as _visualization_job


class Proxy(proxy.Proxy):
    skip_discovery = True

    def __init__(self, session, *args, **kwargs):
        super(Proxy, self).__init__(session=session, *args, **kwargs)
        self.additional_headers = {
            "Accept": "application/json",
            "Content-type": "application/json",
        }

    # ======== Model Management ========

    def models(self, **params):
        """List all Models.

        :param dict params: Optional query parameters to be sent to limit
            the models being returned.

        :returns: a generator of
            :class:`~otcextensions.sdk.modelartsv1.v1.models.Model` instances
        """
        return self._list(_model.Model, **params)

    def create_model(self, **attrs):
        """Create a model from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.modelartsv1.v1.models.Model`,
            comprised of the properties on the Model class.
        :returns: The results of model creation
        :rtype: :class:`~otcextensions.modelartsv1.v1.model.Model`
        """
        return self._create(_model.Model, prepend_key=False, **attrs)

    def get_model(self, model):
        """Get the model by id

        :param model: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.model.Model`

        :returns: instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.model.Model`
        """
        return self._get(_model.Model, model)

    def find_model(self, name_or_id, ignore_missing=False):
        """Find a single model

        :param name_or_id: The name or ID of a ModelArts model
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            if the model does not exist.
            When set to ``True``, no exception will be set when attempting
            to find a nonexistent cluster.

        :returns:
            One :class:`~otcextensions.sdk.modelartsv1.v1.model.Model`
            or ``None``
        """
        return self._find(
            _model.Model, name_or_id, ignore_missing=ignore_missing
        )

    def delete_model(self, model, ignore_missing=False):
        """Delete a model

        :param model: Thie value can be the id of a model
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the model does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent model.
        """
        return self._delete(_model.Model, model, ignore_missing=ignore_missing)

    # ======== DevEnviron Management ========

    def devenv_instances(self, **params):
        """List all Devenv Instances.

        :param dict params: Optional query parameters to be sent to limit
            the instances being returned.
        :returns: a generator of
            :class:`~otcextensions.sdk.modelartsv1.v1.devenv.Devenv` instances.
        """
        if params.get("limit"):
            params.update(paginated=False)
        return self._list(_devenv.Devenv, **params)

    def create_devenv_instance(self, **attrs):
        """Create a devenv instance from attributes.

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.modelartsv1.v1.devenv.Devenv`,
            comprised of the properties on the Devenv class.
        :returns: The results of demanager creation
        :rtype: :class:`~otcextensions.sdk.modelartsv1.v1.devenv.Devenv`
        """
        return self._create(_devenv.Devenv, prepend_key=False, **attrs)

    def delete_devenv_instance(self, instance, ignore_missing=False):
        """Delete a Devenv instance.

        :param instance: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.devenv.Devenv`
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the group does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent devenv.
        """
        return self._delete(
            _devenv.Devenv, instance, ignore_missing=ignore_missing
        )

    def get_devenv_instance(self, instance):
        """Get details of a Devenv Instance.

        :param instance: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.devenv.Devenv`

        :returns: instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.devenv.Devenv`
        """
        return self._get(_devenv.Devenv, instance)

    def find_devenv_instance(self, name_or_id, ignore_missing=False):
        """Find a single Devenv instance by name or Id.

        :param name_or_id: The name or ID of a Devenv instance.

        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            if the devenv does not exist.
            When set to ``True``, no exception will be set when attempting
            to find a nonexistent devenv.

        :returns:
            One :class:`~otcextensions.sdk.modelartsv1.v1.devenv.Devenv`
            or ``None``
        """
        return self._find(
            _devenv.Devenv,
            name_or_id,
            ignore_missing=ignore_missing,
            de_type="Notebook",
        )

    def update_devenv_instance(self, instance, **attrs):
        """Update a Devenv Instance Configurations.

        :param instance: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.devenv.Devenv`
        :param dict attrs: Keyword arguments which will be used to update
            a :class:`~otcextensions.sdk.modelartsv1.v1.devenv.Devenv`,
            comprised of the properties on the Devenv class.

        """
        return self._update(_devenv.Devenv, instance, **attrs)

    def start_devenv_instance(self, instance):
        """Start a Devenv instance.

        :param instance: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.devenv.Devenv`
        :returns: instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.devenv.Devenv`
        """
        devenv = self._get_resource(_devenv.Devenv, instance)
        return devenv.start(self)

    def stop_devenv_instance(self, instance):
        """Stop a Devenv instance.

        :param instance: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.devenv.Devenv`

        :returns: instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.devenv.Devenv`
        """
        devenv = self._get_resource(_devenv.Devenv, instance)
        return devenv.stop(self)

    # Service Management

    def services(self, **params):
        """List all Services.

        :param dict params: Optional query parameters to be sent to limit
            the services being returned.

        :returns: a generator of
            :class:`~otcextensions.sdk.modelartsv1.v1.services.Services`
            instances
        """
        return self._list(_service.Service, paginated=False, **params)

    def create_service(self, **attrs):
        """Deploy a model from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.modelartsv1.v1.service.Service`,
            comprised of the properties on the Service class.
        :returns: The result of service creation.
        :rtype: :class:`~otcextensions.sdk.modelartsv1.v1.service.Service`
        """
        return self._create(_service.Service, prepend_key=False, **attrs)

    def delete_service(self, service, ignore_missing=False):
        """Delete a service
        :param service: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.service.Service`
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the service does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent service.
        :returns: ``None``
        """
        return self._delete(
            _service.Service, service, ignore_missing=ignore_missing
        )

    def get_service(self, service):
        """Get the service by UUID

        :param service: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.service.Service`

        :returns: instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.service.Service`
        """
        return self._get(_service.Service, service)

    def update_service(self, service, **attrs):
        """Update a Service Configurations.

        :param service: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.service.Service`
        :param dict attrs: Keyword arguments which will be used to update
            a :class:`~otcextensions.sdk.modelartsv1.v1.service.Service`,
            comprised of the properties on the Service class.

        """
        return self._update(_service.Service, service, **attrs)

    def stop_service(self, service):
        """Stop a Service.

        :param service: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.service.Service`

        """
        return self._update(_service.Service, service, status="stopped")

    def start_service(self, service):
        """Start a Service.

        :param service: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.service.Service`
        """
        return self._update(_service.Service, service, status="running")

    def find_service(self, name_or_id, ignore_missing=False):
        """Find a single service

        :param name_or_id: The name or ID of a ModelArts service
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            if the service does not exist.
            When set to ``True``, no exception will be set when attempting
            to find a nonexistent service.

        :returns:
            One :class:`~otcextensions.sdk.modelartsv1.v1.service.Service`
            or ``None``
        """
        return self._find(
            _service.Service, name_or_id, ignore_missing=ignore_missing
        )

    def service_logs(self, service_id, **params):
        """List update logs of a real-time service.

        :returns: a generator of
            :class:`~otcextensions.sdk.modelartsv1.v1.service.Log`
            instances
        """
        return self._list(_service.Log, service_id=service_id, **params)

    def service_events(self, service_id, **params):
        """List events logs of a service.

        :returns: a generator of
            :class:`~otcextensions.sdk.modelartsv1.v1.service.Event`
            instances
        """
        return self._list(
            _service.Event,
            service_id=service_id,
            paginated=False,
            **params,
        )

    def service_monitor(self, service_id, **params):
        """List a service monitoring informations.

        :returns: a generator of
            :class:`~otcextensions.sdk.modelartsv1.v1.service.Monitor`
            instances
        """
        return self._list(_service.Monitor, service_id=service_id, **params)

    def service_deployment_specifications(self, **params):
        """List all specifications for a service deployment.

        :returns: a generator of
            :class:`~otcextensions.sdk.modelartsv1.v1.service.Specification`
            instances
        """
        return self._list(_service.Specification, **params)

    def service_resource_pools(self, **params):
        """List all dedicated resource pools (clusters) available
        for a service deployment.

        :returns: a generator of
            :class:`~otcextensions.sdk.modelartsv1.v1.service.Cluster`
            instances
        """
        return self._list(_service.Cluster, **params)

    def wait_for_service(self, service, timeout=1200, wait=5):
        while timeout > 0:
            obj = self.get_service(service)
            status = obj.status.lower()
            if status == "deploying":
                pass
            elif status in ["running", "finished"]:
                return True
            else:
                raise exceptions.SDKException(obj.error_msg)
            timeout = timeout - wait
            time.sleep(wait)
        raise exceptions.SDKException(
            f"Wait Timed Out. service status is: {status}"
        )

    # Training Job Management

    def training_jobs(self, **params):
        """List all training jobs.

        :param dict params: Optional query parameters to be sent to limit
            the training jobs being returned.

        :returns: a generator of
            :class:`~otcextensions.sdk.modelartsv1.v1.training_job.TrainingJob`
            instances
        """
        return self._list(_training_job.TrainingJob, **params)

    def create_training_job(self, **attrs):
        """Create a training job from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.modelartsv1.v1.training_job.\
            TrainingJob`,
            comprised of the properties on the TrainingJob class.

        :returns: The results of training job creation.
        :rtype:
            :class:`~otcextensions.sdk.modelartsv1.v1.training_job.TrainingJob`
        """
        return self._create(_training_job.TrainingJob, **attrs)

    # def find_training_job(self, name_or_id, ignore_missing=False):
    #     """Find a single trainjob

    #     :param name_or_id: The name or ID of a ModelArts trainjob
    #     :param bool ignore_missing: When set to ``False``
    #         :class:`~openstack.exceptions.ResourceNotFound` will be raised
    #         if the trainjob does not exist.
    #         When set to ``True``, no exception will be set when attempting
    #         to find a nonexistent trainjob.

    #     :returns: One :class:
    #       `~otcextensions.sdk.modelartsv1.v1.training_job.TrainingJob`
    #       or ``None``
    #     """
    #     return self._find(
    #         _training_job.TrainingJob,
    #         name_or_id,
    #         ignore_missing=ignore_missing,
    #     )

    def update_training_job(self, job_id, description):
        """Update training job description.

        :param dataset: key id or an instance of
            :class:`~otcextensions.sdk.modelarts.v2.training_job.TrainingJob`

        :param description: Description of a training job.

        :returns: instance of
            :class:`~otcextensions.sdk.modelarts.v2.training_job.TrainingJob`
        """
        return self._update(
            _training_job.TrainingJob,
            job_id,
            job_desc=description,
        )

    def delete_training_job(self, job_id, ignore_missing=False):
        """Delete a training job

        :param job_id: Thie value can be the id of a training job
        """
        return self._delete(
            _training_job.TrainingJob,
            job_id,
            ignore_missing=ignore_missing,
        )

    def training_job_versions(self, job_id, **attrs):
        """List versions of a training job.

        :param dict params: Optional query parameters to be sent to limit
            the training job versions being returned.

        :returns: a generator of
            :class:`~otcextensions.sdk.modelartsv1.v1.training_job.\
                    TrainingJobVersion` instances
        """
        return self._list(
            _training_job.TrainingJobVersion, jobId=job_id, **attrs
        )

    def get_training_job_version(self, job_id, version_id):
        """Get details of a training job by version id.

        :param version_id: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.training_job.TrainingJobVersion`

        :returns: instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.training_job.TrainingJobVersion`
        """
        return self._get(
            _training_job.TrainingJobVersion,
            version_id,
            jobId=job_id,
        )

    def create_training_job_version(self, job_id, **attrs):
        """Create a training job from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.modelartsv1.v1.trainjob.Trainjob`,
            comprised of the properties on the Trainjob class.

        :returns: The results of trainjobs creation
        :rtype: :class:`~otcextensions.sdk.modelartsv1.v1.training_job.\
            TrainingJobVersion`
        """
        return self._create(
            _training_job.TrainingJobVersion,
            jobId=job_id,
            **attrs,
        )

    def delete_training_job_version(
        self, job_id, version_id, ignore_missing=False
    ):
        """Delete a training job version

        :param version_id: Thie value can be the id of a training job version
        """
        return self._delete(
            _training_job.TrainingJobVersion,
            version_id,
            jobId=job_id,
            ignore_missing=ignore_missing,
        )

    # def list_trainingjob_version_logs(self, job_id, version_id):
    #     """Get the trainjob version by id

    #     :param version_id: key id or an instance of
    #         :class:`~otcextensions.sdk.modelartsv1.v1.trainjob_version.TrainjobVersion`

    #     :returns: instance of
    #         :class:`~otcextensions.sdk.modelartsv1.v1.trainjob_version.TrainjobVersion`
    #     """
    #     return self._list(
    #         _trainingjob_version.TrainingJobVersionLogs,
    #         jobId=job_id,
    #         versionId=version_id,
    #     )

    # def list_trainingjob_version_logfile_names(self, job_id, version_id):
    #     """Get the trainjob version by id

    #     :param version_id: key id or an instance of
    #         :class:`~otcextensions.sdk.modelartsv1.v1.trainjob_version.TrainjobVersion`

    #     :returns: instance of
    #         :class:`~otcextensions.sdk.modelartsv1.v1.trainjob_version.TrainjobVersion`
    #     """
    #     return self._list(
    #         _trainingjob_version.GetLogfileName,
    #         versionId=version_id,
    #         jobId=job_id,
    #     )

    def stop_traningjob_version(self, job_id, version_id):
        """Stop a Devenv instance.

        :param instance: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.devenv.Devenv`

        :returns: instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.devenv.Devenv`
        """
        obj = self._get_resource(
            _training_job.TrainingJobVersion, job_id, version_id
        )
        return obj.stop(self)

    def training_job_configs(self, **params):
        """List all Training Job Configurations.

        :returns: a generator of
            (:class:`~otcextensions.sdk.modelartsv1.v1.trainjob_configs.\
                TrainjobConfigs`) instances
        """
        return self._list(_training_job.TrainingJobConfig, **params)

    def create_training_job_config(self, **attrs):
        """Create a Training Job Configuration from attributes.

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.modelartsv1.v1.trainjob_configs.\
                TrainjobConfigs`, comprised of the properties on the
                Training Job Configuration class.
        :returns: The results of Training Job Configuration creation
        :rtype: :class:`~otcextensions.sdk.modelartsv1.v1.training_job.\
            TrainingJobConfig`
        """
        return self._create(_training_job.TrainingJobConfig, **attrs)

    def delete_training_job_config(self, config_name, ignore_missing=False):
        """Delete Training Job Configuration.

        :param config_name: Name of a training job configuration.

        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the config does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent Training Job Configuration.
        """
        return self._delete(
            _training_job.TrainingJobConfig,
            config_name,
            ignore_missing=ignore_missing,
        )

    def get_training_job_config(self, config_name):
        """Get the Training Job Configuration by id

        :param config_name: Name of a training job configuration.

        :returns: instance of :class:`~otcextensions.sdk.modelartsv1.v1.\
            training_job.TrainingJobConfig`
        """
        return self._get(_training_job.TrainingJobConfig, config_name)

    def update_training_job_config(self, config_name, **attrs):
        """Update training job configuration.

        :param config_name: Name of a training job configuration.
        :param dict attrs: Keyword arguments which will be used to update
            a :class:`~otcextensions.sdk.modelartsv1.v1.training_job.\
                TrainingJobConfig`, comprised of the properties on the class.
        """
        return self._update(
            _training_job.TrainingJobConfig, config_name, **attrs
        )

    def show_builtin_algorithms(self):
        """Get the Training Job Configuration by id

        :param trainjob_config: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.trainjob_config.TrainjobConfigs`

        :returns: instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.trainjob_config.TrainjobConfigs`
        """
        return self._get(_builtin_algorithms.BuiltinAlgorithms)

    # Visualization Job Management

    def visualization_jobs(self):
        """List all Visualization Job.

        :returns: a generator of :class:
          `~otcextensions.sdk.modelartsv1.v1.visualization_job.VisualizationJob`
          instances
        """
        return self._list(_visualization_job.VisualizationJob)

    def create_visualization_job(self, **attrs):
        """Create a Visualization Job from attributes

        :param dict attrs: Keyword arguments which will be used to create a
            :class:`~otcextensions.sdk.modelartsv1.v1.visualization_job.\
                VisualizationJob` comprised of the properties on
                the Visualization Job class.

        :returns: The results of Visualization Job creation

        :rtype:
            :class:`~otcextensions.sdk.modelartsv1.v1.visualization_job.\
                VisualizationJob`
        """
        return self._create(
            _visualization_job.VisualizationJob, prepend_key=False, **attrs
        )

    def delete_visualizationjob(self, job_id, ignore_missing=False):
        """Delete a Visualization Job

        :param visualization_job: Thie value can be the name of a
            Visualization Job
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the group does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent Visualization Job.
        """
        return self._delete(
            _visualization_job.VisualizationJob,
            job_id,
            ignore_missing=ignore_missing,
        )

    def show_visualizationjob(self, visualization_job):
        """Get the Visualization Job by id

        :param visualization_job: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.visualization_jobs.\
                VisualizationJobs`

        :returns: instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.visualization_jobs.\
                VisualizationJobs`
        """
        return self._get(
            _visualization_job.VisualizationJob, visualization_job
        )

    def update_visualizationjob_description(self, **attrs):
        """Get the dataset by id

        :param dataset: key id or an instance of
            :class:`~otcextensions.sdk.modelarts.v2.datasets.Datasets`

        :returns: instance of
            :class:`~otcextensions.sdk.modelarts.v2.datasets.Datasets`
        """
        return self._update(_visualization_job.VisualizationJob, **attrs)

    def stop_visualizationjob(self, visualization_job):
        """Stop a VisualizationJob

        :param instance: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.visualization_jobs`

        :returns: instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.visualization_jobs`
        """
        visjob = self._get_resource(
            _visualization_job.VisualizationJobStop, visualization_job
        )
        return visjob.stop(self)

    def restart_visualizationjob(self, visualization_job):
        """Restart a VisualizationJob

        :param instance: key id or an instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.visualization_jobs`

        :returns: instance of
            :class:`~otcextensions.sdk.modelartsv1.v1.visualization_jobs`
        """
        visjob = self._get_resource(
            _visualization_job.VisualizationJobRestart, visualization_job
        )
        return visjob.restart(self)

    def job_resource_specifications(self):
        """List all JobResourceSpecifications .

        :returns: a generator of :class:
          `~otcextensions.sdk.modelartsv1.v1._job_resource_specifications.JobResourceSpecifications`
          instances
        """
        return self._list(
            _job_resource_specifications.JobResourceSpecifications
        )

    def job_engine_specifications(self):
        """List all JobResourceSpecifications .

        :returns: a generator of :class:
          `~otcextensions.sdk.modelartsv1.v1._job_resource_specifications.JobResourceSpecifications`
          instances
        """
        return self._list(_job_engine_specifications.JobEngineSpecifications)
