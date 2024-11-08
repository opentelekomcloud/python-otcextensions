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


from otcextensions.sdk.ctsv3.v3 import _proxy
from otcextensions.sdk.ctsv3.v3 import key_event as _key_event

from openstack.tests.unit import test_proxy_base


class TestCTSv3Proxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestCTSv3Proxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestKeyEvent(TestCTSv3Proxy):
    def test_key_event_create(self):
        self.verify_create(
            self.proxy.create_key_event,
            _key_event.KeyEvent
        )

    def test_key_event_update(self):
        self.verify_update(
            self.proxy.update_key_event,
            _key_event.KeyEvent,
            method_args=[]
        )

    def test_key_event_list(self):
        self.verify_list(
            self.proxy.key_events,
            _key_event.KeyEvent,
            method_kwargs={'notification_type': 'type'},
            expected_kwargs={},
        )
