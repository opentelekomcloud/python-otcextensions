#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json
import uuid
import random

from openstackclient.tests.functional import base


class DnsTests(base.TestCase):
    """Functional tests for DNS. """

    NAME = uuid.uuid4().hex
    OTHER_NAME = uuid.uuid4().hex

    def setUp(self):
        super(DnsTests, self).setUp()
        self.ZONE_NAME = 'example-{0}.org.'.format(random.randint(1, 10000))

    def test_zone_list(self):
        json_output = json.loads(self.openstack(
            'dns zone create {name} -f json'.format(name=self.ZONE_NAME)
        ))
        self.zone_id = json_output["id"]
        self.assertOutput(self.ZONE_NAME, json_output['name'])
        self.addCleanup(self.openstack, 'dns zone delete {name}'.format(
            name=self.ZONE_NAME))

        json_output = json.loads(self.openstack(
            'dns zone list -f json '
        ))
        self.assertIn(
            self.ZONE_NAME,
            [zone['name'] for zone in json_output]
        )

        json_output = json.loads(self.openstack(
            'dns zone show {name} -f json'.format(name=self.ZONE_NAME)
        ))
        self.assertEqual(
            self.zone_id,
            json_output['id']
        )

        json_output = json.loads(self.openstack(
            'dns zone set --description test {name} -f json'.format(
                name=self.ZONE_NAME)
        ))

        self.assertEqual(
            'test',
            json_output['description']
        )

        rs_name = '{a}.{name}'.format(
            a=random.randint(1, 10000),
            name=self.ZONE_NAME
        )
        json_output = json.loads(self.openstack(
            'dns recordset create --name {rs_name} '
            '--type A --record 127.0.0.1 {zone_name} -f json'.format(
                zone_name=self.ZONE_NAME,
                rs_name=rs_name)
        ))

        self.assertOutput(rs_name, json_output['name'])
        self.assertIn('127.0.0.1', json_output['records'])

        rsid = json_output['id']

        self.addCleanup(self.openstack,
                        'dns recordset delete {z} {r}'.format(
                            r=rsid,
                            z=self.ZONE_NAME))

        json_output = json.loads(self.openstack(
            'dns recordset show {z} {r} -f json'.format(
                r=rsid,
                z=self.ZONE_NAME
            )
        ))

        self.assertEqual(rs_name, json_output['name'])

        json_output = json.loads(self.openstack(
            'dns recordset list {zone} -f json'.format(
                zone=self.ZONE_NAME)
        ))

        self.assertIn(
            rs_name,
            [rec['name'] for rec in json_output]
        )

        json_output = json.loads(self.openstack(
            'dns recordset set --record 192.168.0.1 {z} {r} -f json'.format(
                z=self.ZONE_NAME,
                r=rsid)
        ))

        self.assertIn('192.168.0.1', json_output['records'])

        net_id = self.openstack(
            'network list --name admin_external_net -f value -c ID')

        json_output = json.loads(self.openstack(
            'floating ip create {net} -f json'.format(
                net=net_id)
        ))

        fip_id = json_output['id']

        self.addCleanup(self.openstack,
                        'floating ip delete {fip}'.format(
                            fip=fip_id))

        ptr_fip = 'eu-de:' + fip_id
        json_output = json.loads(self.openstack(
            'dns ptr record set {id} {z} -f json'.format(
                id=ptr_fip,
                z=rs_name)))

        self.assertEqual(rs_name, json_output['ptrdname'])

        self.addCleanup(self.openstack,
                        'dns ptr record unset {id}'.format(
                            id=ptr_fip))

        json_output = json.loads(self.openstack(
            'dns ptr record show {ptr} -f json'.format(
                ptr=ptr_fip)))

        self.assertEqual(rs_name, json_output['ptrdname'])

        json_output = json.loads(self.openstack(
            'dns ptr record list -f json'))

        self.assertIn(
            rs_name,
            [rec['ptrdname'] for rec in json_output]
        )
