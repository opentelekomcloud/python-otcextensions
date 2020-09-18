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

from otcextensions.sdk.ces.v1 import alarm


EXAMPLE = {
    'alarm_name': 'alarm-qht9',
    'alarm_action_enabled': False,
    'alarm_description': 'Test description',
    'alarm_enabled': True,
    'metric': {
        'namespace': 'SYS.ECS',
        'metric_name': 'cpu_util',
        'dimensions': [
            {
                'name': 'instance_id',
                'value': 'ccb27344-1ec4-423e-a4d9-f3a885a23e72'
            }
        ]
    },
    'condition': {
        'period': 1,
        'filter': 'average',
        'comparison_operator': '>=',
        'value': 80,
        'unit': '%',
        'count': 3
    }
}


class TestAlarm(base.TestCase):

    def test_basic(self):
        sot = alarm.Alarm()
        self.assertEqual('metric_alarms', sot.resources_key)
        path = '/alarms'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = alarm.Alarm(**EXAMPLE)
        self.assertEqual(EXAMPLE['alarm_name'], sot.name)
        self.assertEqual(EXAMPLE['alarm_action_enabled'],
                         sot.alarm_action_enabled)
        self.assertEqual(EXAMPLE['alarm_description'],
                         sot.alarm_description)
        self.assertEqual(EXAMPLE['alarm_enabled'], sot.alarm_enabled)
        self.assertEqual(EXAMPLE['metric']['namespace'], sot.metric.namespace)
        self.assertEqual(EXAMPLE['metric']['metric_name'],
                         sot.metric.metric_name)
        self.assertEqual(EXAMPLE['metric']['dimensions'][0]['name'],
                         sot.metric.dimensions[0].name)
        self.assertEqual(EXAMPLE['metric']['dimensions'][0]['value'],
                         sot.metric.dimensions[0].value)
        self.assertEqual(EXAMPLE['condition']['period'],
                         sot.condition.period)
        self.assertEqual(EXAMPLE['condition']['filter'],
                         sot.condition.filter)
        self.assertEqual(EXAMPLE['condition']['comparison_operator'],
                         sot.condition.comparison_operator)
        self.assertEqual(EXAMPLE['condition']['value'], sot.condition.value)
        self.assertEqual(EXAMPLE['condition']['unit'], sot.condition.unit)
        self.assertEqual(EXAMPLE['condition']['count'], sot.condition.count)
