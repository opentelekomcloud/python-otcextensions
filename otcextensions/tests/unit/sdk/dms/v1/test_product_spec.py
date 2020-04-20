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

from otcextensions.sdk.dms.v1 import product


JSON_DATA = {
    'tps': '50000',
    'storage': '600',
    'partition_num': '300',
    'product_id': '00300-30308-0--0',
    'spec_code': 'dms.instance.kafka.cluster.c3.mini',
    'io': [{
        'io_type': 'high',
        'storage_spec_code': 'dms.physical.storage.high',
        'available_zones': ['eu-de-02', 'eu-de-01'],
        'volume_type': 'SAS'
    }, {
        'io_type': 'ultra',
        'storage_spec_code': 'dms.physical.storage.ultra',
        'available_zones': ['eu-de-02', 'eu-de-01'],
        'volume_type': 'SSD'
    }],
    'bandwidth': '100MB',
    'unavailable_zones': ['eu-de-02'],
    'available_zones': ['eu-de-01'],
    'ecs_flavor_id': 'c4.large.2',
    'arch_type': 'X86'
}


class TestProduct(base.TestCase):

    def test_basic(self):
        sot = product.Product()

        self.assertEqual('/products', sot.base_path)

        self.assertTrue(sot.allow_list)

    def test_make_it(self):

        sot = product.Product(**JSON_DATA)
        self.assertEqual(JSON_DATA['tps'], sot.tps)
