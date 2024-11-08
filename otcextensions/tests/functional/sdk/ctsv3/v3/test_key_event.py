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

from otcextensions.tests.functional.sdk.ctsv3 import TestCtsv3


class TestKeyEvent(TestCtsv3):

    def test_01_create_event(self):
        attrs = {
            "notification_name": "test",
            "operation_type": "complete",
        }
        event = self.conn.ctsv3.create_key_event(**attrs)
        self.assertGreater(len(event['notification_id']), 0)

    def test_02_key_events(self):
        events = list(self.conn.ctsv3.key_events(notification_type='smn'))
        self.assertGreater(len(events), 0)

    def test_03_update_event(self):
        event = list(self.conn.ctsv3.key_events(notification_type='smn',
                                                notification_name='test'))[0]
        attrs = {
            "notification_name": "test_1",
            "operation_type": "complete",
            "status": "disabled",
            "notification_id": event['notification_id']
        }
        event = self.conn.ctsv3.update_key_event(**attrs)
        self.assertGreater(len(event['notification_id']), 0)

    def test_04_delete_event(self):
        event = list(self.conn.ctsv3.key_events(notification_type='smn',
                                                notification_name='test_1'))[0]
        self.conn.ctsv3.delete_key_event(event)
        events = list(self.conn.ctsv3.key_events(notification_type='smn'))
        test_event = [event for event in events
                      if event['notification_name'] == 'test_1']
        self.assertEqual(len(test_event), 0)
