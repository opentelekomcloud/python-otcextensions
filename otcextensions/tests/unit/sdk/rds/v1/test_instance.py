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

import copy

from keystoneauth1 import adapter
import mock

from openstack.tests.unit import base

from otcextensions.sdk.rds.v1 import instance


PROJECT_ID = '123'
IDENTIFIER = '37f52707-2fb3-482c-a444-77a70a4eafd6'
EXAMPLE = {
    "status": "ACTIVE",
    "name": "rds-new-channle-read",
    "links": [
        {
            "rel": "self",
            "href": ""
        },
        {
            "rel": "bookmark",
            "href": ""
        }
    ],
    "id": IDENTIFIER,
    "volume": {
        "type": "COMMON",
        "size": 100
    },
    "flavor": {
        "id": "7fbf27c5-07e5-43dc-cf13-ad7a0f1c5d9a",
        "links": [
            {
                "rel": "self",
                "href": ""
            },
            {
                "rel": "bookmark",
                "href": ""
            }
        ]
    },
    "datastore": {
        "type": "PostgreSQL",
        "version": "PostgreSQL-9.5.5"
    },
    "publicEndpoint": "10.11.77.101:8635",
    "dbPort": 8635,
    "region": "eu-de",
    "ip": "192.168.1.29",
    "replica_of": [
        {
            "id": "c42cdd29-9912-4b57-91a8-c37a845566b1",
            "links": [
                {
                    "rel": "self",
                    "href": ""
                },
                {
                    "rel": "bookmark",
                    "href": ""
                }
            ]
        }
    ],
    "hostname": 'test'
}


class TestInstance(base.TestCase):

    def setUp(self):
        super(TestInstance, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()
        self.sess.get_project_id = mock.Mock(return_value=PROJECT_ID)
        self.sot = instance.Instance(**EXAMPLE)
        # print(self.sot.to_dict())

    def test_basic(self):
        sot = instance.Instance()
        self.assertEqual('instance', sot.resource_key)
        self.assertEqual('instances', sot.resources_key)
        self.assertEqual('/%(project_id)s/instances', sot.base_path)
        self.assertEqual('rds', sot.service.service_type)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_get)
        self.assertTrue(sot.allow_update)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = instance.Instance(**EXAMPLE)
        self.assertEqual(IDENTIFIER, sot.id)
        self.assertEqual(EXAMPLE['status'], sot.status)
        self.assertEqual(EXAMPLE['hostname'], sot.hostname)
        self.assertEqual(EXAMPLE['links'], sot.links)
        self.assertEqual(EXAMPLE['volume'], sot.volume)
        self.assertEqual(EXAMPLE['flavor'], sot.flavor)
        self.assertEqual(EXAMPLE['datastore'], sot.datastore)
        self.assertEqual(EXAMPLE['publicEndpoint'], sot.publicEndpoint)
        self.assertEqual(EXAMPLE['region'], sot.region)

    def test_list(self):

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"instances": [
            {"instance": {
                "status": "ACTIVE",
                "name": "rds-new-channle-read",
                "links": [
                    {
                        "rel": "self",
                        "href": ""
                    },
                    {
                        "rel": "bookmark",
                        "href": ""
                    }
                ],
                "id": "37f52707-2fb3-482c-a444-77a70a4eafd6",
                "volume": {
                    "type": "COMMON",
                    "size": 100
                },
                "flavor": {
                    "id": "7fbf27c5-07e5-43dc-cf13-ad7a0f1c5d9a",
                    "links": [
                        {
                            "rel": "self",
                            "href": ""
                        },
                        {
                            "rel": "bookmark",
                            "href": ""
                        }
                    ]
                },
                "datastore": {
                    "type": "PostgreSQL",
                    "version": "PostgreSQL-9.5.5"
                },
                "publicEndpoint": "10.11.77.101:8635",
                "dbPort": 8635,
                "region": "eu-de",
                "ip": "192.168.1.29",
                "replica_of": [
                    {
                        "id": "c42cdd29-9912-4b57-91a8-c37a845566b1",
                        "links": [
                            {
                                "rel": "self",
                                "href": ""
                            },
                            {
                                "rel": "bookmark",
                                "href": ""
                            }
                        ]
                    }
                ],
                "hostname": 'test'
            }
            }
        ]}

        self.sess.get.return_value = mock_response

        result = list(self.sot.list(self.sess, project_id=PROJECT_ID))

        self.sess.get.assert_called_once_with(
            '/%s/instances' % (PROJECT_ID),
            headers={"Content-Type": "application/json"},
            params={})

        self.assertEqual([instance.Instance(**EXAMPLE)], result)

    def test_get(self):

        sot = instance.Instance.new(id='1234', project_id=PROJECT_ID)
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.headers = {}

        res_json = {"instance": {
            "configurationStatus": "In-Sync",
            "paramsGroupId": "b89db814-6ba1-454f-a9ad-380064ef0c6f",
            "type": "MySQL",
            "subnetid": "0fb5d084-4e5d-463b-8920-fca10e6b4028",
            "role": "master",
            "internalSubnetId": "330a10fd-3962-44c5-b3a1-1d282617a183",
            "group": "1",
            "securegroup": "ca99fcef-502f-495f-b28d-85c9c6f4666e",
            "vpc": "292997f2-3bf7-4d60-86a5-4e9d593bc850",
            "azcode": "eu-de-01",
            "region": None,
            "created": "2017-05-12T02:18:46",
            "updated": "2017-05-12T02:18:46",
            "status": "ACTIVE",
            "name": "rds-MySQL-1-1",
            "publicEndpoint": "10.11.77.101:8635",
            "dbPort": 8635,
            "links": [
                {
                    "rel": "self",
                    "href": ""
                },
                {
                    "rel": "bookmark",
                    "href": ""
                }
            ],
            "id": "e8faac23-8129-4c68-a231-480e46fc5f4f",
            "flavor": {
                "id": "31b2863c-0e15-44fd-a80d-1e83a7aca338",
                "links": [
                    {
                        "rel": "self",
                        "href": ""
                    },
                    {
                        "rel": "bookmark",
                        "href": ""
                    }
                ]
            },
            "volume": {
                "type": "COMMON",
                "size": 210,
                "used": 25.07
            },
            "datastore": {
                "type": "MySQL",
                "version": "MySQL-5.7.17"
            },
            "fault": None,
            "configuration": None,
            "locality": None,
            "replicas": None,
            "dbuser": "root",
            "storageEngine": None,
            "payModel": 0,
            "cluster_id": "fb22f24c-0466-48f2-8275-70af04ef4935"
        }
        }

        # Sadly res_json is deleted somewhere in __GET__, so
        # pass a copy of it
        mock_response.json.return_value = copy.deepcopy(res_json)

        self.sess.get.return_value = mock_response

        res = sot.get(self.sess)

        self.sess.get.assert_called_once_with(
            '%s/instances/%s' % (PROJECT_ID, '1234'),
            headers={"Content-Type": "application/json"}
        )

        self.assertEqual(res_json['instance']['vpc'], res.vpc)
        self.assertEqual(res_json['instance']['id'], res.id)
        self.assertEqual(res_json['instance']['paramsGroupId'],
                         res.paramsGroupId)

    def test_action_restart(self):
        sot = instance.Instance(**EXAMPLE, project_id=PROJECT_ID)
        response = mock.Mock()
        response.json = mock.Mock(return_value='')
        sess = mock.Mock()
        sess.post = mock.Mock(return_value=response)

        self.assertIsNone(sot.restart(sess))

        url = ("%(project_id)s/instances/%(id)s/action" % {
            'id': IDENTIFIER,
            'project_id': PROJECT_ID
        })
        body = {'restart': {}}
        sess.post.assert_called_with(url,
                                     json=body)

    def test_action_resize(self):
        sot = instance.Instance(**EXAMPLE, project_id=PROJECT_ID)
        response = mock.Mock()
        response.json = mock.Mock(return_value='')
        sess = mock.Mock()
        sess.post = mock.Mock(return_value=response)
        flavor = 'http://flavor/flav'

        self.assertIsNone(sot.resize(sess, flavor))

        url = ("%(project_id)s/instances/%(id)s/action" % {
            'id': IDENTIFIER,
            'project_id': PROJECT_ID
        })
        body = {'resize': {'flavorRef': flavor}}
        sess.post.assert_called_with(url,
                                     json=body)

    def test_action_resize_volume(self):
        sot = instance.Instance(**EXAMPLE, project_id=PROJECT_ID)
        response = mock.Mock()
        response.json = mock.Mock(return_value='')
        sess = mock.Mock()
        sess.post = mock.Mock(return_value=response)
        size = 4

        self.assertIsNone(sot.resize_volume(sess, size))

        url = ("%(project_id)s/instances/%(id)s/action" % {
            'id': IDENTIFIER,
            'project_id': PROJECT_ID
        })
        body = {'resize': {'volume': size}}
        sess.post.assert_called_with(url,
                                     json=body)

    def test_action_restore(self):
        sot = instance.Instance(**EXAMPLE, project_id=PROJECT_ID)
        response = mock.Mock()
        response.json = mock.Mock(return_value='')
        sess = mock.Mock()
        sess.post = mock.Mock(return_value=response)
        backupRef = 'backupRef'

        self.assertIsNone(sot.restore(sess, backupRef))

        url = ("%(project_id)s/instances/%(id)s/action" % {
            'id': IDENTIFIER,
            'project_id': PROJECT_ID
        })
        body = {'restore': {'backupRef': backupRef}}
        sess.post.assert_called_with(url,
                                     json=body)
