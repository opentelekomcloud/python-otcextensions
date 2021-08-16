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
# import uuid
# from datetime import datetime

import mock

from openstackclient.tests.unit import utils
from otcextensions.tests.unit.osclient import test_base

from otcextensions.sdk.css.v1 import cluster
# from otcextensions.sdk.css.v1 import snapshot


def gen_data(data, columns):
    """Fill expected data tuple based on columns list
    """
    return tuple(getattr(data, attr, '') for attr in columns)


def gen_data_dict(data, columns):
    """Fill expected data tuple based on columns list
    """
    return tuple(data.get(attr, '') for attr in columns)


class TestCss(utils.TestCommand):
    def setUp(self):
        super(TestCss, self).setUp()

        self.app.client_manager.css = mock.Mock()

        self.client = self.app.client_manager.css


class FakeCluster(test_base.Fake):
    """Fake one or more Nat Gateways."""
    @classmethod
    def generate(cls):
        """Create a fake CSS Cluster.

        :return:
            A FakeResource object, with id, name and so on
        """
        # Set default attributes.
        object_info = {
            "datastore": {
                "type": "elasticsearch",
                "version": "7.6.2"
            },
            "instances": [
                {
                    "status": "200",
                    "type": "ess",
                    "id": "c2f29369-1985-4028-8e72-89cbb96a299d",
                    "name": "css-5977-ess-esn-1-1",
                    "specCode": "css.xlarge.2",
                    "azCode": "eu-de-01"
                }
            ],
            "updated": "2020-12-03T07:02:08",
            "name": "css-5977",
            "created": "2020-12-03T07:02:08",
            "id": "bc8ea974-77ef-46de-b011-918b0fdedb45",
            "status": "200",
            "endpoint": "10.16.0.88:9200",
            "vpcId": "e7daa617-3ee6-4ff1-b042-8cda4a006a46",
            "subnetId": "6253dc44-24cd-4c0a-90b3-f965e7f4dcd4",
            "securityGroupId": "d478041e-bcbe-4d69-a492-b6122d774b7f",
            "httpsEnable": True,
            "authorityEnable": True,
            "diskEncrypted": False,
            "actionProgress": {},
            "actions": [],
            "tags": []
        }
        return cluster.Cluster(**object_info)
