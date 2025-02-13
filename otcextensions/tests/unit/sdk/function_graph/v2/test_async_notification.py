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

from otcextensions.sdk.function_graph.v2 import async_notification

EXAMPLE_NOTIFICATION = {
    "func_urn": "urn",
    "max_async_event_age_in_seconds": 60,
    "max_async_retry_attempts": 1,
    "created_at": "2021-03-04T14:50:02+08:00",
    "updated_at": "2021-03-04 14:50:02"
}
EXAMPLE_REQUEST = {
    "request_id": "403fcbd6-ec41-401f-9fa7-386f3d3d****",
    "status": "SUCCESS",
    "error_message": "",
    "start_time": "2019-10-25T15:37:27",
    "end_time": "2019-10-25T15:37:27",
    "error_code": 0
}


class TestFunctionAsyncNotification(base.TestCase):

    def test_basic(self):
        sot = async_notification.Notification()
        path = '/fgs/functions/%(function_urn)s/async-invoke-config'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)

    def test_make_it(self):
        sot = async_notification.Notification(**EXAMPLE_NOTIFICATION)
        self.assertEqual(EXAMPLE_NOTIFICATION['func_urn'], sot.func_urn)
        self.assertEqual(
            EXAMPLE_NOTIFICATION['max_async_event_age_in_seconds'],
            sot.max_async_event_age_in_seconds
        )
        self.assertEqual(
            EXAMPLE_NOTIFICATION['max_async_retry_attempts'],
            sot.max_async_retry_attempts
        )
        self.assertEqual(EXAMPLE_NOTIFICATION['created_at'], sot.created_at)
        self.assertEqual(EXAMPLE_NOTIFICATION['updated_at'], sot.updated_at)


class TestFunctionAsyncRequest(base.TestCase):

    def test_basic(self):
        sot = async_notification.Requests()
        path = '/fgs/functions/%(function_urn)s/async-invocations'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_list)

    def test_make_it(self):
        sot = async_notification.Requests(**EXAMPLE_REQUEST)
        self.assertEqual(EXAMPLE_REQUEST['request_id'], sot.request_id)
        self.assertEqual(EXAMPLE_REQUEST['status'], sot.status)
        self.assertEqual(EXAMPLE_REQUEST['status'], sot.status)
        self.assertEqual(EXAMPLE_REQUEST['start_time'], sot.start_time)
        self.assertEqual(EXAMPLE_REQUEST['end_time'], sot.end_time)
        self.assertEqual(EXAMPLE_REQUEST['error_code'], sot.error_code)
