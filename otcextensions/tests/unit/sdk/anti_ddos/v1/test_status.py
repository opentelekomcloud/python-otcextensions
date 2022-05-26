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

from otcextensions.common import format
from otcextensions.sdk.anti_ddos.v1 import status

FAKE_ID = "68d5745e-6af2-40e4-945d-fe449be00148"
EXAMPLE_STATUS = {
    "status": "enable",
}

EXAMPLE_TASK = {
    "task_status": "running",
    "task_msg": "",
}

EXAMPLE_LOG = {
    "start_time": 1473217200000,
    "end_time": 1473242400000,
    "status": 1,
    "trigger_bps": 51106,
    "trigger_pps": 2600,
    "trigger_http_pps": 3589
}

EXAMPLE_DAY_STAT = {
    "period_start": 1472713370609,
    "bps_in": 0,
    "bps_attack": 0,
    "total_bps": 0,
    "pps_in": 0,
    "pps_attack": 0,
    "total_pps": 0
}

EXAMPLE_WEEK_DATA_STAT = {
    "ddos_intercept_times": 0,
    "ddos_blackhole_times": 0,
    "max_attack_bps": 0,
    "max_attack_conns": 0,
    "period_start_date": 1474214461651
}

EXAMPLE_WEEK_STAT = {
    "ddos_intercept_times": 0,
    "weekdata": [EXAMPLE_WEEK_DATA_STAT],
    "top10": [
        {
            "floating_ip_address": "192.168.44.69",
            "times": 23
        }
    ]
}


class TestStatus(base.TestCase):

    def test_basic(self):
        sot = status.FloatingIPStatus()

        self.assertEqual('/antiddos/%(floating_ip_id)s/status', sot.base_path)

        self.assertTrue(sot.allow_fetch)

    def test_make_it(self):

        sot = status.FloatingIPStatus(floating_ip_id=FAKE_ID, **EXAMPLE_STATUS)
        self.assertEqual(FAKE_ID, sot.floating_ip_id)
        self.assertEqual(EXAMPLE_STATUS['status'], sot.status)


class TestTask(base.TestCase):

    def test_basic(self):
        sot = status.TaskStatus()

        self.assertEqual('/query_task_status', sot.base_path)

        self.assertTrue(sot.allow_fetch)

    def test_make_it(self):

        sot = status.TaskStatus(**EXAMPLE_TASK)
        self.assertEqual(EXAMPLE_TASK['task_status'], sot.task_status)
        self.assertEqual(EXAMPLE_TASK['task_msg'], sot.task_msg)


class TestLog(base.TestCase):

    def test_basic(self):
        sot = status.FloatingIPEvent()

        self.assertEqual('/antiddos/%(floating_ip_id)s/logs', sot.base_path)
        self.assertEqual('logs', sot.resources_key)

        self.assertTrue(sot.allow_list)

    def test_make_it(self):

        sot = status.FloatingIPEvent(**EXAMPLE_LOG)
        self.assertEqual(
            format.TimeTMsStr().deserialize(EXAMPLE_LOG['start_time']),
            sot.start_time),
        self.assertEqual(
            format.TimeTMsStr().deserialize(EXAMPLE_LOG['end_time']),
            sot.end_time),
        self.assertEqual(EXAMPLE_LOG['status'], sot.status)
        self.assertEqual(EXAMPLE_LOG['trigger_bps'], sot.trigger_bps)
        self.assertEqual(EXAMPLE_LOG['trigger_pps'], sot.trigger_pps)
        self.assertEqual(EXAMPLE_LOG['trigger_http_pps'],
                         sot.trigger_http_pps)


class TestStatDay(base.TestCase):

    def test_basic(self):
        sot = status.FloatingIPDayStat()

        self.assertEqual('/antiddos/%(floating_ip_id)s/daily', sot.base_path)
        self.assertEqual('data', sot.resources_key)

        self.assertTrue(sot.allow_list)

    def test_make_it(self):

        sot = status.FloatingIPDayStat(**EXAMPLE_DAY_STAT)
        self.assertEqual(
            format.TimeTMsStr().deserialize(EXAMPLE_DAY_STAT['period_start']),
            sot.period_start),
        self.assertEqual(EXAMPLE_DAY_STAT['bps_in'], sot.bps_in)
        self.assertEqual(EXAMPLE_DAY_STAT['bps_attack'], sot.bps_attack)
        self.assertEqual(EXAMPLE_DAY_STAT['total_bps'], sot.total_bps)
        self.assertEqual(EXAMPLE_DAY_STAT['pps_in'], sot.pps_in)
        self.assertEqual(EXAMPLE_DAY_STAT['pps_attack'], sot.pps_attack)
        self.assertEqual(EXAMPLE_DAY_STAT['total_pps'], sot.total_pps)


class TestStatWeek(base.TestCase):

    def test_basic(self):
        sot = status.FloatingIPWeekStat()

        self.assertEqual('/antiddos/weekly', sot.base_path)

        self.assertTrue(sot.allow_fetch)

    def test_make_it(self):

        sot = status.FloatingIPWeekStat(**EXAMPLE_WEEK_STAT)
        self.assertEqual(EXAMPLE_WEEK_STAT['ddos_intercept_times'],
                         sot.ddos_intercept_times)
        self.assertEqual(EXAMPLE_WEEK_STAT['top10'],
                         sot.top10)

    def test_make_data(self):

        sot = status.FloatingIPWeekStatData(**EXAMPLE_WEEK_DATA_STAT)
        self.assertEqual(
            format.TimeTMsStr().deserialize(
                EXAMPLE_WEEK_DATA_STAT['period_start_date']),
            sot.period_start_date),
        self.assertEqual(EXAMPLE_WEEK_DATA_STAT['ddos_intercept_times'],
                         sot.ddos_intercept_times)
        self.assertEqual(EXAMPLE_WEEK_DATA_STAT['ddos_blackhole_times'],
                         sot.ddos_blackhole_times)
        self.assertEqual(EXAMPLE_WEEK_DATA_STAT['max_attack_bps'],
                         sot.max_attack_bps)
        self.assertEqual(EXAMPLE_WEEK_DATA_STAT['max_attack_conns'],
                         sot.max_attack_conns)
