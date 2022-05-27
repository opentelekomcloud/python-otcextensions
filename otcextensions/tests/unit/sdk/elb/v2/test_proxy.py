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
import mock
from openstack.tests.unit import test_proxy_base

from otcextensions.sdk.elb.v2 import _proxy
from otcextensions.sdk.elb.v2 import listener_tag
from otcextensions.sdk.elb.v2 import load_balancer_tag


class TestElbProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestElbProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)
        self.session.get_project_id = mock.Mock(return_value='aa')


class TestElbLoadBalancerTag(TestElbProxy):
    def test_load_balancer_tag_create(self):
        self.verify_create(
            self.proxy.create_load_balancer_tag,
            load_balancer_tag.Tag,
            method_kwargs={
                'key': 'key1',
                'value': 'value1',
                'load_balancer': 'id',
            },
            expected_kwargs={
                'key': 'key1',
                'value': 'value1',
                'loadbalancer_id': 'id',
            }
        )

    def test_load_balancer_delete(self):
        self.verify_delete(
            self.proxy.delete_load_balancer_tag,
            load_balancer_tag.Tag,
            True,
            method_kwargs={
                'key': 'resource_id',
            },
            expected_kwargs={
                'loadbalancer_id': 'resource_id',
                'ignore_missing': True
            }
        )

    def test_load_balancers(self):
        self.verify_list(
            self.proxy.load_balancer_tags,
            load_balancer_tag.Tag,
            method_kwargs={
                'load_balancer': 'id',
            },
            expected_kwargs={
                'loadbalancer_id': 'id',
            }
        )


class TestElbLoadBalancerListenerTag(TestElbProxy):
    def test_listener_tag_create(self):
        self.verify_create(
            self.proxy.create_listener_tag,
            listener_tag.Tag,
            method_kwargs={
                'key': 'key1',
                'value': 'value1',
                'listener': 'id',
            },
            expected_kwargs={
                'key': 'key1',
                'value': 'value1',
                'listener_id': 'id',
            }
        )

    def test_load_balancer_delete(self):
        self.verify_delete(
            self.proxy.delete_listener_tag,
            listener_tag.Tag,
            True,
            method_kwargs={
                'key': 'resource_id',
            },
            expected_kwargs={
                'listener_id': 'resource_id',
                'ignore_missing': True
            }
        )

    def test_listeners(self):
        self.verify_list(
            self.proxy.listener_tags,
            listener_tag.Tag,
            method_kwargs={
                'listener': 'id',
            },
            expected_kwargs={
                'listener_id': 'id',
            }
        )
