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

from otcextensions.sdk.smn.v2 import subscription


EXAMPLE = {
    "topic_urn": "urn:smn:regionId:762bdb3251034f268af0e..",
    "protocol": "sms",
    "subscription_urn": "urn:smn:regionId:762bdb3251034f268af0e..",
    "owner": "762bdb3251034f268af0e395c53ea09b",
    "endpoint": "xxxxxxxxxx",
    "remark": "",
    "status": 0
}


class TestSubscription(base.TestCase):

    def test_basic(self):
        sot = subscription.Subscription()
        self.assertEqual('subscriptions', sot.resources_key)
        path = '/notifications/topics/{topic_urn}s/subscriptions'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_commit)

    def test_make_it(self):
        sot = subscription.Subscription(**EXAMPLE)
        self.assertEqual(EXAMPLE['subscription_urn'], sot.subscription_urn)
        self.assertEqual(EXAMPLE['topic_urn'], sot.topic_urn)
        self.assertEqual(EXAMPLE['protocol'], sot.protocol)
        self.assertEqual(EXAMPLE['owner'], sot.owner)
        self.assertEqual(EXAMPLE['endpoint'], sot.endpoint)
        self.assertEqual(EXAMPLE['remark'], sot.remark)
        self.assertEqual(EXAMPLE['status'], sot.status)
