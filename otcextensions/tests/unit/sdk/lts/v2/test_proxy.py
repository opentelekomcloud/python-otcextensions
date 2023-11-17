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

from otcextensions.sdk.lts.v2 import _proxy
from otcextensions.sdk.lts.v2 import group as _group
from otcextensions.sdk.lts.v2 import stream as _stream

from openstack.tests.unit import test_proxy_base


class TestLtsProxy(test_proxy_base.TestProxyBase):

    def setUp(self):
        super(TestLtsProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestGroup(TestLtsProxy):

    def test_groups(self):
        self.verify_list(self.proxy.groups, _group.Group)
    def test_group_create(self):
        self.verify_create(self.proxy.create_group,
                           _group.Group,
                           method_kwargs={'log_group_name': 'log-group-name',
                                          'ttl_in_days': 5},
                           expected_kwargs={'log_group_name': 'log-group-name',
                                            'ttl_in_days': 5})

    def test_group_delete(self):
        self.verify_delete(self.proxy.delete_group,
                           _group.Group, True)


class TestStream(TestLtsProxy):

    def test_streams(self):
        group = _group.Group(id='id-group')
        self.verify_list(
            self.proxy.streams,
            _stream.Stream,
            method_args=[group],
            expected_kwargs={'log_group_id': group.id},
            expected_args=[]
        )
    def test_stream_create(self):
        self.verify_create(self.proxy.create_stream,
                           _stream.Stream,
                           method_kwargs={'log_group': 'log-group-id',
                                          'log_stream_name': 'log-stream-name'},
                           expected_kwargs={'log_group': 'log-group-id',
                                            'log_stream_name':
                                                'log-stream-name'})

    def test_stream_delete(self):
        group = _group.Group(id='id-group')
        stream = _stream.Stream(id='id-stream')
        self._verify(
            'otcextensions.sdk.lts.v2.group.Group.delete_stream',
            self.proxy.delete_stream,
            method_args=[group, stream, True],
            method_kwargs={},
            expected_args=[_stream.Stream, stream],
            expected_kwargs={
                'log_group_id': group.id,
                'ignore_missing': True}
        )
