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
from otcextensions.sdk.apig.v2 import signature

EXAMPLE = {
    "name": "signature_demo",
    "sign_key": "signkeysignkey",
    "sign_secret": "sig************ret"
}


class TestThrottlingPolicy(base.TestCase):

    def test_basic(self):
        sot = signature.Signature()
        self.assertEqual(
            '/apigw/instances/%(gateway_id)s/signs',
            sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)
        self.assertEqual('signs', sot.resources_key)

    def test_make_it(self):
        sot = signature.Signature(**EXAMPLE)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['sign_key'], sot.sign_key)
        self.assertEqual(EXAMPLE['sign_secret'], sot.sign_secret)
