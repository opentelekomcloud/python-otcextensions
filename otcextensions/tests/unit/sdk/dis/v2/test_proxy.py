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

from otcextensions.sdk.dis.v2 import _proxy
from otcextensions.sdk.dis.v2 import stream
from otcextensions.sdk.dis.v2 import app
from otcextensions.sdk.dis.v2 import checkpoint
from otcextensions.sdk.dis.v2 import dump_task

from openstack.tests.unit import test_proxy_base


class TestDisProxy(test_proxy_base.TestProxyBase):

    def setUp(self):
        super(TestDisProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestStream(TestDisProxy):

    def test_stream_create(self):
        self.verify_create(self.proxy.create_stream, stream.Stream,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={'name': 'id'})

    def test_stream_delete(self):
        self.verify_delete(self.proxy.delete_stream,
                           stream.Stream, True)

    def test_stream_get(self):
        self.verify_get(self.proxy.get_stream, stream.Stream)

    def test_streams(self):
        self.verify_list(self.proxy.streams, stream.Stream,
                         method_kwargs={'x': 1, 'y': 2},
                         expected_kwargs={'x': 1, 'y': 2})

    def test_stream_partition_update(self):
        self._verify('openstack.proxy.Proxy._update',
                     self.proxy.update_stream_partition,
                     method_args=['test-stream', 10],
                     expected_args=[stream.Stream, 'test-stream'],
                     expected_kwargs={
                         'stream_name': 'test-stream',
                         'target_partition_count': 10
                     })


class TestApp(TestDisProxy):

    def test_app_create(self):
        self.verify_create(self.proxy.create_app, app.App,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={'name': 'id'})

    def test_app_delete(self):
        self.verify_delete(self.proxy.delete_app, app.App, True)

    def test_app_get(self):
        self.verify_get(self.proxy.get_app, app.App)

    def test_apps(self):
        self.verify_list(self.proxy.apps, app.App)

    def test_app_consumptions(self):
        self.verify_list(self.proxy.app_consumptions, app.AppConsumption,
                         method_kwargs={
                             'app_name': 'test-app',
                             'stream_name': 'test-stream',
                         },
                         expected_kwargs={
                             'app_name': 'test-app',
                             'stream_name': 'test-stream',
                             'checkpoint_type': 'LAST_READ'
                         })


class TestCheckpoint(TestDisProxy):
    def test_checkpoint_create(self):
        self.verify_create(self.proxy.create_checkpoint,
                           checkpoint.Checkpoint,
                           method_kwargs={'arg1': 'a1'},
                           expected_kwargs={
                               'arg1': 'a1',
                               'checkpoint_type': 'LAST_READ'
                           })

    def test_checkpoint_delete(self):
        self._verify(
            'otcextensions.sdk.dis.v2.checkpoint.Checkpoint.delete_checkpoint',
            self.proxy.delete_checkpoint,
            method_args=['test-stream', 'test-app'],
            expected_args=[self.proxy],
            expected_kwargs={
                'stream_name': 'test-stream',
                'app_name': 'test-app',
                'checkpoint_type': 'LAST_READ'
            }
        )

    def test_checkpoint_get(self):
        self._verify(
            'otcextensions.sdk.dis.v2.checkpoint.Checkpoint.get_checkpoint',
            self.proxy.get_checkpoint,
            method_args=['test-stream', 'test-app', 'partition300'],
            expected_args=[self.proxy],
            expected_kwargs={
                'stream_name': 'test-stream',
                'app_name': 'test-app',
                'partition_id': 'partition300',
                'checkpoint_type': 'LAST_READ'
            }
        )


class TestDumpTask(TestDisProxy):
    def test_dump_task_create(self):
        self.verify_create(self.proxy.create_dump_task,
                           dump_task.DumpTask,
                           method_kwargs={
                               'stream_name': 'test-stream',
                               'arg1': 'test-arg'
                           },
                           expected_kwargs={
                               'arg1': 'test-arg',
                               'uri_stream_name': 'test-stream',
                           })

    def test_dump_task_delete(self):
        self.verify_delete(self.proxy.delete_dump_task,
                           dump_task.DumpTask, False,
                           method_args=['test-stream', 'test-dump-task'],
                           expected_kwargs={
                               'uri_stream_name': 'test-stream',
                               'ignore_missing': False
                           },
                           expected_args=['test-dump-task'])

    def test_dump_task_get(self):
        self.verify_get(self.proxy.get_dump_task,
                        dump_task.DumpTask,
                        method_args=['test-stream', 'test-dump-task'],
                        expected_kwargs={'uri_stream_name': 'test-stream'},
                        expected_args=['test-dump-task'])

    def test_dump_tasks(self):
        self.verify_list(self.proxy.dump_tasks,
                         dump_task.DumpTask,
                         method_kwargs={'stream_name': 'test-stream'},
                         expected_kwargs={
                             'uri_stream_name': 'test-stream'
                         })

    def test_dump_task_start(self):
        self._verify(
            'otcextensions.sdk.dis.v2.dump_task.DumpTask._action',
            self.proxy.start_dump_task,
            method_args=['test-stream'],
            expected_args=[self.proxy, 'test-stream', 'start']
        )

    def test_dump_task_pause(self):
        self._verify(
            'otcextensions.sdk.dis.v2.dump_task.DumpTask._action',
            self.proxy.pause_dump_task,
            method_args=['test-stream'],
            expected_args=[self.proxy, 'test-stream', 'stop']
        )
