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
from openstack.tests.unit import base
from otcextensions.sdk.apig.v2 import resource_query as _rq

EXAMPLE = {
    "apis_num": 27,
    "apis_in_release": 11,
    "apis_not_in_release": 6
}


class TestApiQuantity(base.TestCase):

    def test_basic(self):
        sot = _rq.ApiQuantities()
        self.assertEqual(
            '/apigw/instances/%(gateway_id)s/resources/outline/apis',
            sot.base_path)
        self.assertTrue(sot.allow_fetch)

    def test_make_it(self):
        sot = _rq.ApiQuantities(**EXAMPLE)
        self.assertEqual(EXAMPLE['apis_num'], sot.apis_num)
        self.assertEqual(EXAMPLE['apis_in_release'], sot.apis_in_release)
        self.assertEqual(
            EXAMPLE['apis_not_in_release'], sot.apis_not_in_release
        )


EXAMPLE_GROUP = {
    "not_in_koogallery": 0,
    "in_koogallery": 23
}


class TestApiGroupQuantity(base.TestCase):

    def test_basic(self):
        sot = _rq.ApiGroupQuantities()
        self.assertEqual(
            '/apigw/instances/%(gateway_id)s/resources/outline/groups',
            sot.base_path)
        self.assertTrue(sot.allow_fetch)

    def test_make_it(self):
        sot = _rq.ApiGroupQuantities(**EXAMPLE_GROUP)
        self.assertEqual(
            EXAMPLE_GROUP['not_in_koogallery'], sot.not_in_koogallery
        )
        self.assertEqual(EXAMPLE_GROUP['in_koogallery'], sot.in_koogallery)


EXAMPLE_APP = {
    "authorized": 7,
    "not_authorized": 5
}


class TestAppQuantity(base.TestCase):

    def test_basic(self):
        sot = _rq.AppQuantities()
        self.assertEqual(
            '/apigw/instances/%(gateway_id)s/resources/outline/apps',
            sot.base_path)
        self.assertTrue(sot.allow_fetch)

    def test_make_it(self):
        sot = _rq.AppQuantities(**EXAMPLE_APP)
        self.assertEqual(EXAMPLE_APP['authorized'], sot.authorized)
        self.assertEqual(EXAMPLE_APP['not_authorized'], sot.not_authorized)
