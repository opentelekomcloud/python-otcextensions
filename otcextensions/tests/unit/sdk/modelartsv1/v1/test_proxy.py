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
from openstack.tests.unit import test_proxy_base
from otcextensions.sdk.modelartsv1.v1 import _proxy
from otcextensions.sdk.modelartsv1.v1 import builtin_model
from otcextensions.sdk.modelartsv1.v1 import devenv
from otcextensions.sdk.modelartsv1.v1 import job_engine
from otcextensions.sdk.modelartsv1.v1 import job_flavor
from otcextensions.sdk.modelartsv1.v1 import model
from otcextensions.sdk.modelartsv1.v1 import service
from otcextensions.sdk.modelartsv1.v1 import service_log
from otcextensions.sdk.modelartsv1.v1 import service_event
from otcextensions.sdk.modelartsv1.v1 import service_monitor
from otcextensions.sdk.modelartsv1.v1 import service_flavor
from otcextensions.sdk.modelartsv1.v1 import service_cluster
from otcextensions.sdk.modelartsv1.v1 import training_job
from otcextensions.sdk.modelartsv1.v1 import training_job_config
from otcextensions.sdk.modelartsv1.v1 import training_job_version
from otcextensions.sdk.modelartsv1.v1 import visualization_job


class TestModelartsV1Proxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestModelartsV1Proxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestBuiltInModel(TestModelartsV1Proxy):
    def test_builtin_models(self):
        self.verify_list(
            self.proxy.builtin_models,
            builtin_model.BuiltInModel,
        )


class TestModel(TestModelartsV1Proxy):
    def test_models(self):
        self.verify_list(
            self.proxy.models,
            model.Model,
        )

    def test_get_model(self):
        self.verify_get(
            self.proxy.get_model,
            model.Model,
        )

    def test_find_model(self):
        self.verify_find(
            self.proxy.find_model,
            model.Model,
            False,
        )

    def test_find_model_ignore(self):
        self.verify_find(
            self.proxy.find_model,
            model.Model,
            True,
        )

    def test_create_model(self):
        self.verify_create(
            self.proxy.create_model,
            model.Model,
            method_kwargs={"a": "b"},
            expected_kwargs={"prepend_key": False, "a": "b"},
        )

    def test_delete_model(self):
        self.verify_delete(
            self.proxy.delete_model,
            model.Model,
            False,
        )

    def test_delete_model_ignore(self):
        self.verify_delete(
            self.proxy.delete_devenv_instance,
            devenv.Devenv,
            True,
        )


class TestDevenv(TestModelartsV1Proxy):
    def test_devenv_instances(self):
        self.verify_list(
            self.proxy.devenv_instances,
            devenv.Devenv,
            method_kwargs={"limit": 10},
            expected_kwargs={"limit": 10, "paginated": False},
        )

    def test_get_devenv_instance(self):
        self.verify_get(
            self.proxy.get_devenv_instance,
            devenv.Devenv,
        )

    def test_find_devenv_instance(self):
        self.verify_find(
            self.proxy.find_devenv_instance,
            devenv.Devenv,
            False,
            expected_kwargs={"de_type": "Notebook"},
        )

    def test_find_devenv_instance_ignore(self):
        self.verify_find(
            self.proxy.find_devenv_instance,
            devenv.Devenv,
            True,
            expected_kwargs={"de_type": "Notebook"},
        )

    def test_create_devenv_instance(self):
        self.verify_create(
            self.proxy.create_devenv_instance,
            devenv.Devenv,
            method_kwargs={"a": "b"},
            expected_kwargs={"prepend_key": False, "a": "b"},
        )

    def test_delete_devenv_instance(self):
        self.verify_delete(
            self.proxy.delete_devenv_instance,
            devenv.Devenv,
            False,
        )

    def test_delete_devenv_instance_ignore(self):
        self.verify_delete(
            self.proxy.delete_devenv_instance,
            devenv.Devenv,
            True,
        )

    def test_update_devenv_instance(self):
        self.verify_update(
            self.proxy.update_devenv_instance,
            devenv.Devenv,
        )

    def test_start_devenv_instance(self):
        self._verify(
            "otcextensions.sdk.modelartsv1.v1.devenv.Devenv.start",
            self.proxy.start_devenv_instance,
            method_args=["val"],
            expected_args=[self.proxy],
        )

    def test_stop_devenv_instance(self):
        self._verify(
            "otcextensions.sdk.modelartsv1.v1.devenv.Devenv.stop",
            self.proxy.stop_devenv_instance,
            method_args=["val"],
            expected_args=[self.proxy],
        )


class TestService(TestModelartsV1Proxy):
    def test_services(self):
        self.verify_list(
            self.proxy.services,
            service.Service,
            method_kwargs={"limit": 10},
            expected_kwargs={"limit": 10, "paginated": False},
        )

    def test_get_service(self):
        self.verify_get(
            self.proxy.get_service,
            service.Service,
        )

    def test_create_service(self):
        self.verify_create(
            self.proxy.create_service,
            service.Service,
            method_kwargs={"a": "b"},
            expected_kwargs={"prepend_key": False, "a": "b"},
        )

    def test_start_service(self):
        self.verify_update(
            self.proxy.update_service,
            service.Service,
            method_kwargs={"status": "running"},
            expected_kwargs={"status": "running"},
        )

    def test_stop_service(self):
        self.verify_update(
            self.proxy.update_service,
            service.Service,
            method_kwargs={"status": "stopped"},
            expected_kwargs={"status": "stopped"},
        )

    def test_delete_service(self):
        self.verify_delete(
            self.proxy.delete_service,
            service.Service,
            False,
        )

    def test_delete_service_ignore(self):
        self.verify_delete(
            self.proxy.delete_service,
            service.Service,
            True,
        )

    def test_update_service(self):
        self.verify_update(
            self.proxy.update_service,
            service.Service,
        )


class TestJobFlavor(TestModelartsV1Proxy):
    def test_job_flavors(self):
        self.verify_list(
            self.proxy.job_flavors,
            job_flavor.JobFlavor,
        )


class TestJobEngine(TestModelartsV1Proxy):
    def test_job_engines(self):
        self.verify_list(
            self.proxy.job_engines,
            job_engine.JobEngine,
        )


class TestServiceLog(TestModelartsV1Proxy):
    def test_service_logs(self):
        self.verify_list(
            self.proxy.service_logs,
            service_log.ServiceLog,
            method_kwargs={"service_id": "service-id"},
            expected_kwargs={"serviceId": "service-id"},
        )


class TestServiceEvent(TestModelartsV1Proxy):
    def test_service_events(self):
        self.verify_list(
            self.proxy.service_events,
            service_event.ServiceEvent,
            method_kwargs={"service_id": "service-id"},
            expected_kwargs={"serviceId": "service-id"},
        )


class TestServiceMonitor(TestModelartsV1Proxy):
    def test_service_monitor(self):
        self.verify_list(
            self.proxy.service_monitor,
            service_monitor.ServiceMonitor,
            method_kwargs={"service_id": "service-id"},
            expected_kwargs={"serviceId": "service-id"},
        )


class TestServiceFlavor(TestModelartsV1Proxy):
    def test_service_flavors(self):
        self.verify_list(
            self.proxy.service_flavors,
            service_flavor.ServiceFlavor,
        )


class TestServiceCluster(TestModelartsV1Proxy):
    def test_service_clusters(self):
        self.verify_list(
            self.proxy.service_clusters,
            service_cluster.ServiceCluster,
        )


class TestTrainingJob(TestModelartsV1Proxy):
    def test_training_jobs(self):
        self.verify_list(
            self.proxy.training_jobs,
            training_job.TrainingJob,
        )

    def test_create_training_job(self):
        self.verify_create(
            self.proxy.create_training_job,
            training_job.TrainingJob,
        )

    def test_update_training_job(self):
        trainingjob_instance = training_job.TrainingJob()
        description = "test description"
        self._verify(
            "openstack.proxy.Proxy._update",
            self.proxy.update_training_job,
            method_args=[trainingjob_instance, description],
            expected_args=[training_job.TrainingJob, trainingjob_instance],
            expected_kwargs={"job_desc": description},
        )

    def test_delete_training_job(self):
        self.verify_delete(
            self.proxy.delete_training_job,
            training_job.TrainingJob,
            False,
        )

    def test_delete_training_job_ignore(self):
        self.verify_delete(
            self.proxy.delete_training_job,
            training_job.TrainingJob,
            True,
        )


class TestTrainingJobVersion(TestModelartsV1Proxy):
    def test_training_job_versions(self):
        self.verify_list(
            self.proxy.training_job_versions,
            training_job_version.TrainingJobVersion,
            method_kwargs={"job_id": "job-id"},
            expected_kwargs={"jobId": "job-id"},
        )

    def test_create_training_job_version(self):
        self.verify_create(
            self.proxy.create_training_job_version,
            training_job_version.TrainingJobVersion,
            method_kwargs={"job_id": "job-id"},
            expected_kwargs={"jobId": "job-id"},
        )

    def test_get_training_job_version(self):
        self.verify_get(
            self.proxy.get_training_job_version,
            training_job_version.TrainingJobVersion,
            method_args=["job-id", "version-id"],
            expected_args=["version-id"],
            expected_kwargs={"jobId": "job-id"},
        )

    def test_delete_training_job_version(self):
        self.verify_delete(
            self.proxy.delete_training_job_version,
            training_job_version.TrainingJobVersion,
            False,
            method_args=["job-id", "version-id"],
            expected_args=["version-id"],
            expected_kwargs={"jobId": "job-id"},
        )

    def test_delete_training_job_version_ignore(self):
        self.verify_delete(
            self.proxy.delete_training_job_version,
            training_job_version.TrainingJobVersion,
            True,
            method_args=["job-id", "version-id"],
            expected_args=["version-id"],
            expected_kwargs={"jobId": "job-id"},
        )

    def test_stop_training_job(self):
        self._verify(
            "otcextensions.sdk.modelartsv1.v1.training_job.TrainingJob.stop",
            self.proxy.stop_training_job,
            method_args=["job-id", "version-id"],
            expected_args=[self.proxy, "version-id"],
        )


class TestTrainingJobConfig(TestModelartsV1Proxy):
    def test_training_job_configs(self):
        self.verify_list(
            self.proxy.training_job_configs,
            training_job_config.TrainingJobConfig,
        )

    def test_create_training_job_config(self):
        self.verify_create(
            self.proxy.create_training_job_config,
            training_job_config.TrainingJobConfig,
        )

    def test_get_training_job_config(self):
        self.verify_get(
            self.proxy.get_training_job_config,
            training_job_config.TrainingJobConfig,
        )

    def test_update_training_job_config(self):
        self.verify_update(
            self.proxy.update_training_job_config,
            training_job_config.TrainingJobConfig,
        )

    def test_delete_training_job_config(self):
        self.verify_delete(
            self.proxy.delete_training_job_config,
            training_job_config.TrainingJobConfig,
            False,
        )

    def test_delete_training_job_config_ignore(self):
        self.verify_delete(
            self.proxy.delete_training_job_config,
            training_job_config.TrainingJobConfig,
            True,
        )


class TestVisualizationJob(TestModelartsV1Proxy):
    def test_visualization_jobs(self):
        self.verify_list(
            self.proxy.visualization_jobs,
            visualization_job.VisualizationJob,
        )

    def test_create_visualization_job(self):
        self.verify_create(
            self.proxy.create_visualization_job,
            visualization_job.VisualizationJob,
        )

    def test_update_visualization_job(self):
        visualizationjob_instance = visualization_job.VisualizationJob()
        description = "test description"
        self._verify(
            "openstack.proxy.Proxy._update",
            self.proxy.update_visualization_job,
            method_args=[visualizationjob_instance, description],
            expected_args=[
                visualization_job.VisualizationJob,
                visualizationjob_instance,
            ],
            expected_kwargs={"job_desc": description},
        )

    def test_delete_visualization_job(self):
        self.verify_delete(
            self.proxy.delete_visualization_job,
            visualization_job.VisualizationJob,
            False,
        )

    def test_delete_visualization_job_ignore(self):
        self.verify_delete(
            self.proxy.delete_visualization_job,
            visualization_job.VisualizationJob,
            True,
        )

    def test_restart_visualization_job(self):
        self._verify(
            ("otcextensions.sdk.modelartsv1.v1.visualization_job."
             "VisualizationJob.restart"),
            self.proxy.restart_visualization_job,
            method_args=["val"],
            expected_args=[self.proxy],
        )

    def test_stop_visualization_job(self):
        self._verify(
            "otcextensions.sdk.modelartsv1.v1.visualization_job.VisualizationJob.stop", # noqa
            self.proxy.stop_visualization_job,
            method_args=["val"],
            expected_args=[self.proxy],
        )
