#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
# import datetime
import random

import mock
import time
import uuid

from otcextensions.tests.unit.osclient import test_base

from otcextensions.sdk.anti_ddos.v1 import config
from otcextensions.sdk.anti_ddos.v1 import floating_ip
from otcextensions.sdk.anti_ddos.v1 import status


class TestAntiDDoS(test_base.TestCommand):

    def setUp(self):
        super(TestAntiDDoS, self).setUp()

        self.app.client_manager.anti_ddos = mock.Mock()
        self.client = self.app.client_manager.anti_ddos


class FakeConfig(test_base.Fake):
    """Fake one or more Config"""

    @classmethod
    def generate(cls):
        object_info = {
            'traffic_limited_list': [
                {
                    'traffic_pos_id': i,
                    'traffic_per_second': random.randint(1, 600),
                    'packet_per_second': random.randint(1, 600),
                } for i in range(1, random.randint(1, 5))
            ],
            'http_limited_list': [
                {
                    'http_request_pos_id': i,
                    'http_packet_per_second': random.randint(1, 600),
                } for i in range(1, random.randint(1, 5))
            ],
            'connection_limited_list': [
                {
                    'cleaning_access_pos_id': i,
                    'new_connection_limited': random.randint(1, 600),
                    'total_connection_limited': random.randint(1, 600),
                } for i in range(1, random.randint(1, 5))
            ],
        }
        obj = config.Config.existing(**object_info)
        return obj


class FakeFloatingIP(test_base.Fake):
    """Fake one or more Floating IP"""

    @classmethod
    def generate(cls):
        object_info = {
            'floating_ip_address': uuid.uuid4().hex,
            'floating_ip_id': uuid.uuid4().hex,
            'network_type': random.choice(['EIP', 'ELB']),
            'status': random.choice(['normal', 'configging', 'notConfig']),
            'is_enable_l7': random.choice([False, True]),
            'app_type_id': random.randint(1, 5),
            'cleaning_access_pos_id': random.randint(1, 5),
            'http_request_pos_id': random.randint(1, 5),
        }
        obj = floating_ip.FloatingIP.existing(**object_info)
        return obj


class FakeFloatingIPEvent(test_base.Fake):
    """Fake one or more Floating IP events"""

    @classmethod
    def generate(cls):
        object_info = {
            'floating_ip_id': uuid.uuid4().hex,
            'start_time': time.time() * 1000,
            'end_time': time.time() * 1000,
            'trigger_bps': random.randint(1, 5),
            'trigger_pps': random.randint(1, 5),
            'trigger_http_pps': random.randint(1, 5),
            'status': random.choice([1, 2]),
        }
        obj = status.FloatingIPEvent.existing(**object_info)
        return obj


class FakeFloatingIPStatDay(test_base.Fake):
    """Fake one or more Floating IP stat day"""

    @classmethod
    def generate(cls):
        object_info = {
            'floating_ip_id': uuid.uuid4().hex,
            'period_start': time.time() * 1000,
            'bps_in': random.randint(1, 5),
            'bps_attack': random.randint(1, 5),
            'total_bps': random.randint(1, 5),
            'pps_in': random.randint(1, 5),
            'pps_attack': random.randint(1, 5),
            'total_pps': random.randint(1, 5),
        }
        obj = status.FloatingIPDayStat.existing(**object_info)
        return obj


class FakeFloatingIPStatWeek(test_base.Fake):
    """Fake one or more Floating IP stat week"""

    @classmethod
    def generate(cls):
        object_info = {
            'weekdata': [({
                'period_start': time.time() * 1000,
                'ddos_intercept_times': random.randint(1, 5),
                'ddos_blackhole_times': random.randint(1, 5),
                'max_attack_bps': random.randint(1, 5),
                'max_attack_conns': random.randint(1, 5),
            } for i in range(1, 2))]

        }
        obj = status.FloatingIPWeekStat.existing(**object_info)
        return obj
