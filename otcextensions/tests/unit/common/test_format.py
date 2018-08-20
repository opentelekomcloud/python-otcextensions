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


class TestTimeTMsStr(base.TestCase):

    def test_serialize(self):
        obj = format.TimeTMsStr()

        self.assertEqual(
            1534583170000,
            obj.serialize('2018-08-18T09:06:10+00:00')
        )

    def test_deserialize(self):
        obj = format.TimeTMsStr()

        self.assertEqual(
            '2018-08-18T09:06:10.432+00:00',
            obj.deserialize(1534583170432)
        )
