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
import copy
from unittest.mock import MagicMock

import mock
from openstackclient.tests.unit import utils
from osc_lib import utils as _osc_lib_utils

from otcextensions.sdk.modelartsv1.v1 import devenv
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


class FakeDevenv(test_base.Fake):
    """Fake one or more Modelarts devenv."""

    @classmethod
    def generate(cls):
        """Create a fake Modelarts devenv.

        :return:
            A FakeResource object, with id, name and so on
        """
        return devenv.Devenv(**examples.EXAMPLE_DEVENV)


class FakeModel(test_base.Fake):
    """Fake one or more Modelarts model."""

    @classmethod
    def generate(cls):
        """Create a fake Modelarts model.

        :return:
            A FakeResource object, with id, name and so on
        """
        EXAMPLE2 = copy.deepcopy(examples.EXAMPLE_MODEL)
        sot = model.Model()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = EXAMPLE2
        sot._translate_response(mock_response)

        return sot  # model.Model(**examples.EXAMPLE_MODEL)


class FakeService(test_base.Fake):
    """Fake one or more Modelarts service."""

    @classmethod
    def generate(cls):
        """Create a fake Modelarts service.

        :return:
            A FakeResource object, with id, name and so on
        """
        return service.Service(**examples.EXAMPLE_SERVICE)


class FakeServiceLog(test_base.Fake):
    """Fake one or more Modelarts service log."""

    @classmethod
    def generate(cls):
        """Create a fake Modelarts service Log.

        :return:
            A FakeResource object, with id, name and so on
        """
        object_info = {
            "config": [
                {
                    "model_id": "f565ac47-6239-4e8c-b2dc-0665dc52e302",
                    "model_name": "model-demo",
                    "model_version": "0.0.1",
                    "specification": "modelarts.vm.cpu.2u",
                    "custom_spec": {},
                    "weight": 100,
                    "instance_count": 1,
                    "scaling": False,
                    "envs": {},
                    "cluster_id": "2c9080f86d37da64016d381fe5940002",
                }
            ],
            "extend_config": [],
            "update_time": 1586250930708,
            "result": "RUNNING",
            "cluster_id": "2c9080f86d37da64016d381fe5940002",
        }
        return service_log.ServiceLog(**object_info)


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
        object_info = {
            "model_id": "xxxx",
            "model_name": "minst",
            "model_version": "1.0.0",
            "invocation_times": 50,
            "failed_times": 1,
            "cpu_core_usage": 2.4,
            "cpu_core_total": 4,
            "cpu_memory_usage": 2011,
            "cpu_memory_total": 8192,
            "gpu_usage": 0.6,
            "gpu_total": 1,
        }
        monitor = service_monitor.ServiceMonitor(**object_info)
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
        object_info = {
            "cluster_id": "cluster-uuid",
            "cluster_name": "pool-a1cf",
            "tenant": "tenant-uuid",
            "project": "project-uuid",
            "owner": "owner-uuid",
            "created_at": 1658743383618,
            "status": "running",
            "allocatable_cpu_cores": 7.06,
            "allocatable_memory": 27307.0,
            "allocatable_gpus": 0.0,
            "charging_mode": "postpaid",
            "max_node_count": 50,
            "nodes": {
                "specification": "modelarts.vm.cpu.8ud",
                "count": 1,
                "available_count": 1,
            },
            "services_count": {"realtime_count": 0, "batch_count": 0},
        }
        cluster = service_cluster.ServiceCluster(**object_info)
        cluster.allocatable_resources = {
            "cpu_cores": cluster.allocatable_cpu_cores,
            "memory": cluster.allocatable_memory,
            "gpus": cluster.allocatable_gpus,
        }
        return cluster


class FakeVisualizationJob(test_base.Fake):
    """Fake one or more Modelarts visualization job."""

    @classmethod
    def generate(cls):
        """Create a fake Modelarts visualization job.

        :return:
            A FakeResource object, with id, name and so on
        """
        object_info = {
            "job_id": 1,
            "job_name": "visualization-job",
            "status": 1,
            "create_time": 15099239923,
            "resource_id": "4787c885-e18d-4ef1-aa12-c4ed0c364b27",
            "duration": 1502323,
            "job_desc": "This is a visualization job",
            "service_url": "https://XXX/modelarts/tensoarbod/xxxx/111",
            "train_url": "/obs/name/",
            "schedule": [{"type": "stop", "timeUnit": "HOURS", "duration": 1}],
            "remaining_duration": None,
        }

        return visualization_job.VisualizationJob(**object_info)


class FakeTrainingJob(test_base.Fake):
    """Fake one or more Modelarts visualization job."""

    @classmethod
    def generate(cls):
        """Create a fake Modelarts visualization job.

        :return:
            A FakeResource object, with id, name and so on
        """
        object_info = {
            "is_success": True,
            "job_id": "10",
            "job_name": "TestModelArtsJob",
            "status": "1",
            "create_time": "1524189990635",
            "version_id": "10",
            "version_name": "V0001",
            "resource_id": "jobafd08896",
        }

        return training_job.TrainingJob(**object_info)


class FakeTrainingJobVersion(test_base.Fake):
    """Fake one or more Modelarts training job version."""

    @classmethod
    def generate(cls):
        """Create a fake Modelarts training job version.

        :return:
            A FakeResource object, with id, name and so on
        """

        return training_job_version.TrainingJobVersion(
            **examples.EXAMPLE_TRAINING_JOB_VERSION
        )


class FakeTrainingJobConfig(test_base.Fake):
    """Fake one or more Modelarts training job configuration."""

    @classmethod
    def generate(cls):
        """Create a fake Modelarts training job configuration.

        :return:
            A FakeResource object, with id, name and so on
        """
        object_info = {
            "spec_code": "modelarts.vm.gpu.v100",
            "user_image_url": "100.125.5.235:20202/jobmng/custom-cpu-base:1.0",
            "user_command": "bash -x /home/work/run_train.sh python \
                /home/work/user-job-dir/app/mnist/mnist_softmax.py \
                --data_url /home/work/user-job-dir/app/mnist_data",
            "dataset_version_id": "2ff0d6ba-c480-45ae-be41-09a8369bfc90",
            "engine_name": "TensorFlow",
            "is_success": True,
            "nas_mount_path": "/home/work/nas",
            "worker_server_num": 1,
            "nas_share_addr": "192.168.8.150:/",
            "train_url": "/test/minst/train_out/out1/",
            "nas_type": "nfs",
            "spec_id": 4,
            "parameter": [{"label": "learning_rate", "value": 0.01}],
            "log_url": "/usr/log/",
            "config_name": "config123",
            "app_url": "/usr/app/",
            "create_time": 1559045426000,
            "dataset_id": "38277e62-9e59-48f4-8d89-c8cf41622c24",
            "volumes": [
                {
                    "nfs": {
                        "id": "43b37236-9afa-4855-8174-32254b9562e7",
                        "src_path": "192.168.8.150:/",
                        "dest_path": "/home/work/nas",
                        "read_only": False,
                    }
                },
                {
                    "host_path": {
                        "src_path": "/root/work",
                        "dest_path": "/home/mind",
                        "read_only": False,
                    }
                },
            ],
            "cpu": "64",
            "model_id": 4,
            "boot_file_url": "/usr/app/boot.py",
            "dataset_name": "dataset-test",
            "pool_id": "pool9928813f",
            "config_desc": "This is a config desc test",
            "gpu_num": 1,
            "data_source": [{"type": "obs", "data_url": "/test/minst/data/"}],
            "pool_name": "p100",
            "dataset_version_name": "dataset-version-test",
            "core": "8",
            "engine_type": 1,
            "engine_id": 3,
            "engine_version": "TF-1.8.0-python2.7",
            "data_url": "/test/minst/data/",
        }
        return training_job_config.TrainingJobConfig(**object_info)
