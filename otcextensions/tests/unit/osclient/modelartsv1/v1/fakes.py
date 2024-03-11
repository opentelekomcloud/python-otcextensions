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
import mock
from openstackclient.tests.unit import utils
from osc_lib import utils as _osc_lib_utils

from otcextensions.sdk.modelartsv1.v1 import builtin_model
from otcextensions.sdk.modelartsv1.v1 import devenv
from otcextensions.sdk.modelartsv1.v1 import job_engine
from otcextensions.sdk.modelartsv1.v1 import job_flavor
from otcextensions.sdk.modelartsv1.v1 import model
from otcextensions.sdk.modelartsv1.v1 import service
from otcextensions.sdk.modelartsv1.v1 import service_cluster
from otcextensions.sdk.modelartsv1.v1 import service_event
from otcextensions.sdk.modelartsv1.v1 import service_flavor
from otcextensions.sdk.modelartsv1.v1 import service_log
from otcextensions.sdk.modelartsv1.v1 import service_monitor
from otcextensions.sdk.modelartsv1.v1 import training_job
from otcextensions.sdk.modelartsv1.v1 import training_job_config
from otcextensions.sdk.modelartsv1.v1 import training_job_version
from otcextensions.sdk.modelartsv1.v1 import visualization_job
from otcextensions.tests.unit.osclient import test_base
from otcextensions.tests.unit.sdk.modelartsv1.v1 import examples


def gen_data(obj, columns, formatters=None):
    """Fill expected data tuple based on columns list"""
    return _osc_lib_utils.get_item_properties(
        obj, columns, formatters=formatters
    )


def gen_data_dict(data, columns):
    """Fill expected data tuple based on columns list"""
    return tuple(data.get(attr, "") for attr in columns)


class TestModelartsv1(utils.TestCommand):
    def setUp(self):
        super(TestModelartsv1, self).setUp()

        self.app.client_manager.modelartsv1 = mock.Mock()

        self.client = self.app.client_manager.modelartsv1


class FakeBuiltInModel(test_base.Fake):
    """Fake one or more Modelarts built-in model."""

    @classmethod
    def generate(cls):
        """Create a fake Modelarts built-in model.

        :return:
            A FakeResource object, with id, name and so on
        """
        return builtin_model.BuiltInModel(**examples.BUILT_IN_MODEL)


class FakeDevenv(test_base.Fake):
    """Fake one or more Modelarts devenv."""

    @classmethod
    def generate(cls):
        """Create a fake Modelarts devenv.

        :return:
            A FakeResource object, with id, name and so on
        """
        return devenv.Devenv(**examples.DEVENV)


class FakeModel(test_base.Fake):
    """Fake one or more Modelarts model."""

    @classmethod
    def generate(cls):
        """Create a fake Modelarts model.

        :return:
            A FakeResource object, with id, name and so on
        """
        return model.Model(**examples.MODEL)


class FakeJobFlavor(test_base.Fake):
    """Fake one or more Modelarts model."""

    @classmethod
    def generate(cls):
        """Create a fake Modelarts model.

        :return:
            A FakeResource object, with id, name and so on
        """

        return job_flavor.JobFlavor(**examples.JOB_FLAVOR)


class FakeJobEngine(test_base.Fake):
    """Fake one or more Modelarts model."""

    @classmethod
    def generate(cls):
        """Create a fake job resource engine.

        :return:
            A FakeResource object, with id, name and so on
        """
        object_info = {
            "engine_type": 4,
            "engine_name": "Caffe",
            "engine_id": 8,
            "engine_version": "Caffe-1.0.0-python2.7",
        }

        return job_engine.JobEngine(**object_info)


class FakeService(test_base.Fake):
    """Fake one or more Modelarts service."""

    @classmethod
    def generate(cls):
        """Create a fake Modelarts service.

        :return:
            A FakeResource object, with id, name and so on
        """
        return service.Service(**examples.SERVICE)


class FakeServiceLog(test_base.Fake):
    """Fake one or more Modelarts service log."""

    @classmethod
    def generate(cls):
        """Create a fake Modelarts service Log.

        :return:
            A FakeResource object, with id, name and so on
        """
        return service_log.ServiceLog(**examples.SERVICE_LOG)


class FakeServiceEvent(test_base.Fake):
    """Fake one or more Modelarts service event."""

    @classmethod
    def generate(cls):
        """Create a fake Modelarts service Event.

        :return:
            A FakeResource object.
        """
        object_info = {
            "occur_time": 1562597251764,
            "event_type": "normal",
            "event_info": "start to deploy service",
        }
        return service_event.ServiceEvent(**object_info)


class FakeServiceSpecification(test_base.Fake):
    """Fake one or more Modelarts service specification."""

    @classmethod
    def generate(cls):
        """Create a fake Modelarts service specification.

        :return:
            A FakeResource object.
        """
        object_info = {
            "specification": "modelarts.vm.gpu.v100",
            "billing_spec": "modelarts.vm.gpu.v100",
            "is_open": True,
            "spec_status": "normal",
            "is_free": False,
            "over_quota": False,
            "extend_params": 1,
        }
        return service_flavor.ServiceFlavor(**object_info)


class FakeServiceMonitor(test_base.Fake):
    """Fake one or more Modelarts service monitor."""

    @classmethod
    def generate(cls):
        """Create a fake Modelarts service monitor.

        :return:
            A FakeResource object.
        """
        monitor = service_monitor.ServiceMonitor(**examples.SERVICE_MONITOR)
        monitor.cpu_core = f"{monitor.cpu_core_usage}/{monitor.cpu_core_total}"
        monitor.cpu_memory = (
            f"{monitor.cpu_memory_usage}/{monitor.cpu_memory_total}"
        )
        monitor.gpu = f"{monitor.gpu_usage}/{monitor.gpu_total}"
        return monitor


class FakeServiceCluster(test_base.Fake):
    """Fake one or more Modelarts service cluster."""

    @classmethod
    def generate(cls):
        """Create a fake Modelarts service cluster.

        :return:
            A FakeResource object.
        """
        cluster = service_cluster.ServiceCluster(**examples.SERVICE_CLUSTER)
        cluster.allocatable_resources = {
            "cpu_cores": cluster.allocatable_cpu_cores,
            "memory": cluster.allocatable_memory,
            "gpus": cluster.allocatable_gpus,
        }
        return cluster


class FakeTrainingJob(test_base.Fake):
    """Fake one or more Modelarts visualization job."""

    @classmethod
    def generate(cls):
        """Create a fake Modelarts visualization job.

        :return:
            A FakeResource object, with id, name and so on
        """
        return training_job.TrainingJob(**examples.TRAINING_JOB)


class FakeTrainingJobVersion(test_base.Fake):
    """Fake one or more Modelarts training job version."""

    @classmethod
    def generate(cls):
        """Create a fake Modelarts training job version.

        :return:
            A FakeResource object, with id, name and so on
        """
        return training_job_version.TrainingJobVersion(
            **examples.TRAINING_JOB_VERSION
        )


class FakeTrainingJobConfig(test_base.Fake):
    """Fake one or more Modelarts training job configuration."""

    @classmethod
    def generate(cls):
        """Create a fake Modelarts training job configuration.

        :return:
            A FakeResource object, with id, name and so on
        """
        return training_job_config.TrainingJobConfig(
            **examples.TRAINING_JOB_CONFIG
        )


class FakeVisualizationJob(test_base.Fake):
    """Fake one or more Modelarts visualization job."""

    @classmethod
    def generate(cls):
        """Create a fake Modelarts visualization job.

        :return:
            A FakeResource object, with id, name and so on
        """
        return visualization_job.VisualizationJob(**examples.VISUALIZATION_JOB)
