# Licensed under the Apache License, Version 2.0 (the 'License'); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import copy

from keystoneauth1 import adapter
import mock

from openstack.tests.unit import base

from otcextensions.sdk.rds.v1 import configuration

OS_HEADERS = {
    'Content-Type': 'application/json',
}

ENDPOINT = 'http://some_endpoint'

PROJECT_ID = '23'
IDENTIFIER = 'IDENTIFIER'
EXAMPLE_GROUP = {
    'id': IDENTIFIER,
    'name': 'default-SQLServer-2014',
    'datastore_version_id': '4f71c5b5-8939-424e-8825-8e3816e4303d',
    'datastore_version_name': '2014',
    'datastore_name': 'sqlserver',
    'description': 'Default parameter group for sqlserver 2014',
    'instance_count': 0,
    'created': '2017-05-05T04:40:51',
    'updated': '2017-05-05T04:40:51',
    'values': {
        'xp_cmdshell': '0'
    },
    'parameters': [{
        'name': 'auto_increment_increment',
        'value': '1',
        'needRestart': '0',
        'readonly': '1',
        'valueRange': '1-65535',
        'datatype': 'integer',
        'description': 'auto_increment_increment and auto_increment_offset.'
    }, {
        'name': 'autocommit',
        'value': 'ON',
        'needRestart': '0',
        'readonly': '1',
        'valueRange': 'ON|OFF',
        'datatype': 'boolean',
        'description': 'The autocommit mode. If set to ON, all changes'
    }
    ],
}


class TestConfigurationGroup(base.TestCase):

    # TODO(agoncharov)
    # - test all fields
    # - test negative server responses

    def setUp(self):
        super(TestConfigurationGroup, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()
        self.sess.post = mock.Mock()
        self.sess.delete = mock.Mock()
        self.sess.put = mock.Mock()
        self.sess.patch = mock.Mock()
        self.sess.get_project_id = mock.Mock(return_value=PROJECT_ID)
        self.sot = configuration.ConfigurationGroup(**EXAMPLE_GROUP)

    def test_basic(self):
        sot = configuration.ConfigurationGroup()
        self.assertEqual('configuration', sot.resource_key)
        self.assertEqual('configurations', sot.resources_key)
        self.assertEqual('/%(project_id)s/configurations', sot.base_path)
        self.assertEqual('rds', sot.service.service_type)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_get)
        self.assertTrue(sot.allow_update)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        # TODO(agoncharov) check all parameters
        sot = configuration.ConfigurationGroup(**EXAMPLE_GROUP)
        self.assertEqual(IDENTIFIER, sot.id)
        self.assertEqual(EXAMPLE_GROUP['name'], sot.name)
        self.assertEqual(EXAMPLE_GROUP['created'], sot.created)

    def test_list(self):

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'configurations': [EXAMPLE_GROUP]}

        self.sess.get.return_value = mock_response

        result = list(self.sot.list(
            self.sess,
            project_id=PROJECT_ID,
            headers=OS_HEADERS
        ))

        self.sess.get.assert_called_once_with(
            '/%s/configurations' % (PROJECT_ID),
            headers=OS_HEADERS,
            params={}
        )

        self.assertEqual([configuration.ConfigurationGroup(**EXAMPLE_GROUP)],
                         result)

    def test_get(self):

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'configuration': copy.deepcopy(EXAMPLE_GROUP)
        }
        mock_response.headers = {}

        self.sess.get.return_value = mock_response

        sot = configuration.ConfigurationGroup.new(
            project_id=PROJECT_ID,
            id=IDENTIFIER,
            # **EXAMPLE_GROUP
        )

        result = sot.get(self.sess, headers=OS_HEADERS)

        self.sess.get.assert_called_once_with(
            '%s/configurations/%s' % (PROJECT_ID, IDENTIFIER),
            headers=OS_HEADERS,
        )

        self.assertEqual(
            configuration.ConfigurationGroup(
                project_id=PROJECT_ID,
                **EXAMPLE_GROUP
            ),
            result)

    def test_create(self):

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'configuration': copy.deepcopy(EXAMPLE_GROUP)
        }
        mock_response.headers = {}

        self.sess.post.return_value = mock_response

        sot = configuration.ConfigurationGroup.new(
            project_id=PROJECT_ID,
            **EXAMPLE_GROUP)

        result = sot.create(self.sess, headers=OS_HEADERS)

        self.sess.post.assert_called_once_with(
            '/%s/configurations' % (PROJECT_ID),
            headers=OS_HEADERS,
            json={'configuration': EXAMPLE_GROUP}
        )

        self.assertEqual(
            configuration.ConfigurationGroup(
                project_id=PROJECT_ID,
                **EXAMPLE_GROUP
            ),
            result)

        # TODO(agoncharov)
        # {"badRequest":{"code":400,"message":
        # "The server could not comply with the request since it is malformed
        # or incorrect."},"errCode":"RDS.0001","externalMessage":
        # "Parameter error!"}

    def test_delete(self):

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_response.headers = {}

        self.sess.delete.return_value = mock_response

        sot = configuration.ConfigurationGroup(
            project_id=PROJECT_ID,
            **EXAMPLE_GROUP
        )

        sot.delete(self.sess, headers=OS_HEADERS)

        url = '%(project_id)s/configurations/%(id)s' % \
            {
                'project_id': PROJECT_ID,
                'id': sot.id
            }

        # utils.urljoin strips leading '/', but it is not a problem
        self.sess.delete.assert_called_once_with(
            url,
            headers=OS_HEADERS
        )

    def _verify2(self, mock_method, test_method,
                 method_args=None, method_kwargs={}, method_result=None,
                 expected_args=None, expected_kwargs=None,
                 expected_result=None):
        """Internal invoke helper

        """

        mock_method.reset_mock()
        mock_method.return_value = expected_result

        test_method(*method_args, **method_kwargs)

        mock_method.assert_called_once_with(
            *expected_args,
            **expected_kwargs
        )

    def test_get_associated_instances(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_response.headers = {}

        self.sess.get.return_value = mock_response

        sot = configuration.ConfigurationGroup(
            project_id=PROJECT_ID,
            **EXAMPLE_GROUP
        )

        url = '%(project_id)s/configurations/%(id)s/instances' % \
            {
                'project_id': PROJECT_ID,
                'id': sot.id
            }

        # Invoke without endpoint_override
        self._verify2(
            expected_result=mock_response,
            mock_method=self.sess.get,
            test_method=sot.get_associated_instances,
            method_args=[self.sess],
            method_kwargs={},
            expected_args=[url],
            expected_kwargs={
                'headers': OS_HEADERS,
            }
        )

        # Invoke with endpoint_override as argument
        self._verify2(
            expected_result=mock_response,
            mock_method=self.sess.get,
            test_method=sot.get_associated_instances,
            method_args=[self.sess],
            method_kwargs={'endpoint_override': ENDPOINT},
            expected_args=[url],
            expected_kwargs={
                'headers': OS_HEADERS,
                'endpoint_override': ENDPOINT
            }
        )

        # Invoke with endpoint_override as attribute
        sot.endpoint_override = ENDPOINT
        self._verify2(
            expected_result=mock_response,
            mock_method=self.sess.get,
            test_method=sot.get_associated_instances,
            method_args=[self.sess],
            method_kwargs={},
            expected_args=[url],
            expected_kwargs={
                'headers': OS_HEADERS,
                'endpoint_override': ENDPOINT
            }
        )

    # def test_add_custom_parameter(self):
    #     mock_response = mock.Mock()
    #     mock_response.status_code = 200
    #     mock_response.json.return_value = {
    #         'errCode': 'RDS.0041',
    #         'externalMessage': 'Operation accepted success.'
    #     }
    #     mock_response.headers = {}
    #
    #     config = {
    #         'values': {
    #             'a': 'x',
    #             'b': 'y'
    #         }
    #     }
    #
    #     req = {
    #         'configuration': dict(**config)
    #     }
    #
    #     sot = configuration.ConfigurationGroup(
    #         project_id=PROJECT_ID,
    #         **EXAMPLE_GROUP
    #     )
    #
    #     url = '%(project_id)s/configurations/%(id)s' % \
    #         {
    #             'project_id': PROJECT_ID,
    #             'id': sot.id
    #         }
    #
    #     # Invoke without endpoint_override
    #     self._verify2(
    #         expected_result=mock_response,
    #         mock_method=self.sess.patch,
    #         test_method=sot.add_custom_parameter,
    #         method_args=[self.sess],
    #         method_kwargs=config,
    #         expected_args=[url],
    #         expected_kwargs={
    #             'json': req,
    #             # 'headers': OS_HEADERS,
    #         }
    #     )
    #
    #     # Invoke with endpoint_override as argument
    #     self._verify2(
    #         expected_result=mock_response,
    #         mock_method=self.sess.patch,
    #         test_method=sot.add_custom_parameter,
    #         method_args=[self.sess],
    #         method_kwargs=dict(endpoint_override=ENDPOINT, **config),
    #         expected_args=[url],
    #         expected_kwargs={
    #             'json': req,
    #             # 'headers': OS_HEADERS,
    #             'endpoint_override': ENDPOINT
    #         }
    #     )
    #
    #     # Invoke with endpoint_override as attribute
    #     sot.endpoint_override = ENDPOINT
    #     self._verify2(
    #         expected_result=mock_response,
    #         mock_method=self.sess.patch,
    #         test_method=sot.add_custom_parameter,
    #         method_args=[self.sess],
    #         method_kwargs=config,
    #         expected_args=[url],
    #         expected_kwargs={
    #             'json': req,
    #             # 'headers': OS_HEADERS,
    #             'endpoint_override': ENDPOINT
    #         }
    #     )

    def test_update(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'errCode': 'RDS.0041',
            'externalMessage': 'Operation accepted success.'
        }
        mock_response.headers = {}

        config = {
            'name': 'test',
            'description': 'descr',
            'values': {
                'a': 'x',
                'b': 'y'
            }
        }

        req = {
            'configuration': dict(**config)
        }

        sot_tmpl = configuration.ConfigurationGroup.existing(
            project_id=PROJECT_ID,
            **EXAMPLE_GROUP
        )

        sot = copy.deepcopy(sot_tmpl)
        sot._update(**config)

        url = '%(project_id)s/configurations/%(id)s' % \
            {
                'project_id': PROJECT_ID,
                'id': sot.id
            }

        # Invoke without endpoint_override
        self._verify2(
            expected_result=mock_response,
            mock_method=self.sess.put,
            test_method=sot.update,
            method_args=[self.sess],
            # method_kwargs=None,
            expected_args=[url],
            expected_kwargs={
                'json': req,
                # 'headers': OS_HEADERS,
            }
        )

        sot = copy.deepcopy(sot_tmpl)
        sot._update(**config)

        # Invoke with endpoint_override as argument
        self._verify2(
            expected_result=mock_response,
            mock_method=self.sess.put,
            test_method=sot.update,
            method_args=[self.sess],
            method_kwargs=dict(endpoint_override=ENDPOINT),
            expected_args=[url],
            expected_kwargs={
                'json': req,
                # 'headers': OS_HEADERS,
                'endpoint_override': ENDPOINT
            }
        )

        sot = copy.deepcopy(sot_tmpl)
        sot._update(**config)

        # # Invoke with endpoint_override as attribute
        # sot.endpoint_override = ENDPOINT
        # self._verify2(
        #     expected_result=mock_response,
        #     mock_method=self.sess.put,
        #     test_method=sot.update,
        #     method_args=[self.sess],
        #     # method_kwargs=None,
        #     expected_args=[url],
        #     expected_kwargs={
        #         'json': req,
        #         # 'headers': OS_HEADERS,
        #         'endpoint_override': ENDPOINT
        #     }
        # )
