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
import base64
import os

from openstack.tests.unit import test_proxy_base
from otcextensions.sdk.modelartsv2.v2 import _proxy
from otcextensions.sdk.modelartsv2.v2 import dataset
from otcextensions.sdk.modelartsv2.v2 import dataset_sample


class TestModelartsV2Proxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestModelartsV2Proxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestDataset(TestModelartsV2Proxy):
    def test_datasets(self):
        self.verify_list(
            self.proxy.datasets,
            dataset.Dataset,
            method_kwargs={"limit": 10},
            expected_kwargs={"limit": 10},
        )

    def test_get_dataset(self):
        self.verify_get(
            self.proxy.get_dataset,
            dataset.Dataset,
            method_args=["dataset-uuid"],
            expected_args=["dataset-uuid"],
        )

    def test_create_dataset(self):
        self.verify_create(
            self.proxy.create_dataset,
            dataset.Dataset,
            method_kwargs={"arg1": "val1", "arg2": "val2"},
            expected_kwargs={"arg1": "val1", "arg2": "val2"},
        )

    def test_delete_dataset(self):
        self.verify_delete(
            self.proxy.delete_dataset,
            dataset.Dataset,
            False,
        )

    def test_delete_dataset_ignore(self):
        self.verify_delete(
            self.proxy.delete_dataset,
            dataset.Dataset,
            True,
        )


class TestDatasetSample(TestModelartsV2Proxy):
    def test_dataset_samples(self):
        self.verify_list(
            self.proxy.dataset_samples,
            dataset_sample.DatasetSample,
            method_args=["dataset-uuid"],
            expected_args=[],
            method_kwargs={"limit": 10},
            expected_kwargs={"datasetId": "dataset-uuid", "limit": 10},
        )

    def test_get_dataset_sample(self):
        self.verify_get(
            self.proxy.get_dataset_sample,
            dataset_sample.DatasetSample,
            method_args=["dataset-uuid", "sample-uuid"],
            expected_args=["sample-uuid"],
            expected_kwargs={"datasetId": "dataset-uuid"},
        )

    def test_add_dataset_samples(self):
        dirname = os.path.dirname(__file__)
        file_path = os.path.join(dirname, "8710109684_e2c5ef6aeb_n.jpg")
        with open(file_path, "rb") as file:
            sample = {
                "name": "8710109684_e2c5ef6aeb_n.jpg",
                "data": base64.b64encode(file.read()).decode(),
            }
        self.verify_create(
            self.proxy.add_dataset_samples,
            dataset_sample.DatasetSample,
            method_args=["dataset-uuid"],
            expected_args=[],
            method_kwargs={
                "file_path": file_path,
            },
            expected_kwargs={
                "datasetId": "dataset-uuid",
                "samples": [sample],
            },
        )

    # def test_delete_dataset_samples(self):
    #    self.verify_create(
    #        self.proxy.delete_dataset_samples,
    #        dataset.DeleteSample,
    #        method_args=["dataset-uuid"],
    #        expected_args=[],
    #        method_kwargs={
    #            "samples": ["s1-uuid", "s2-uuid"],
    #            "delete_source": False,
    #        },
    #        expected_kwargs={
    #            "dataset_id": "dataset-uuid",
    #            "samples": ["s1-uuid", "s2-uuid"],
    #            "delete_source": False,
    #        },
    #    )
