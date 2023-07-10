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
from openstack import proxy
from otcextensions.sdk.dis.v2 import app as _app
from otcextensions.sdk.dis.v2 import checkpoint as _checkpoint
from otcextensions.sdk.dis.v2 import data as _data
from otcextensions.sdk.dis.v2 import dump_task as _dump_task
from otcextensions.sdk.dis.v2 import stream as _stream


class Proxy(proxy.Proxy):

    skip_discovery = True

    def __init__(self, session, *args, **kwargs):
        super(Proxy, self).__init__(session=session, *args, **kwargs)
        self.additional_headers = {"Accept": "application/json",
                                   "Content-type": "application/json"}

    # ======== Stream ========
    def streams(self, **params):
        """List all Streams.

        :param dict params: Optional query parameters to be sent to limit
            the streams being returned.

        :returns: a generator of
            (:class:`~otcextensions.sdk.dis.v2.stream.Stream`) instances
        """
        if params.get('limit'):
            params.update(paginated=False)
        return self._list(_stream.Stream, **params)

    def get_stream(self, stream):
        """Query details of a DIS stream

        :param stream: The value can be the name of a DIS Stream.
        :returns: One :class:`~otcextensions.sdk.dis.v2.stream.Stream`
        :raises: :class:`~openstack.exceptions.ResourceNotFound`
            when no resource can be found.
        """
        return self._get(_stream.Stream, stream)

    def create_stream(self, **attrs):
        """Create a stream from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.dis.v2.stream.Stream`,
            comprised of the properties on the Streams class.
        :returns: The results of stream creation
        :rtype: :class:`~otcextensions.sdk.dis.v2.stream.Stream`
        """
        return self._create(_stream.Stream, **attrs)

    def delete_stream(self, stream, ignore_missing=False):
        """Delete a DIS stream.

        :param stream: The value can be the name of a DIS stream.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the stream does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent stream.

        :returns: ``None``
        """
        return self._delete(_stream.Stream, stream,
                            ignore_missing=ignore_missing)

    def update_stream_partition(self, stream, **attrs):
        """Update a DIS stream

        :param stream: The value can be the name of a DIS stream.
        :param dict attrs: The attributes to update on the stream represented
            by ``stream``.

        :returns: ``None``
        """
        return self._update(_stream.Stream, stream, **attrs)

    # ======== App ========
    def create_app(self, **attrs):
        """Create an App from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.dis.v2.app.App`,
            comprised of the properties on the App class.
        :returns: The results of app creation
        :rtype: :class:`~otcextensions.sdk.dis.v2.app.App`
        """
        return self._create(_app.App, **attrs)

    def apps(self, **params):
        """List all Apps.

        :param dict params: Optional query parameters to be sent to limit
            the apps being returned.

        :returns: a generator of
            (:class:`~otcextensions.sdk.dis.v2.app.App`) instances
        """
        if params.get('limit'):
            params.update(paginated=False)
        return self._list(_app.App, **params)

    def get_app(self, app):
        """Query details of a DIS App.

        :param app: Name of the app to be queried.
        :returns: One :class:`~otcextensions.sdk.dis.v2.app.App`
        :raises: :class:`~openstack.exceptions.ResourceNotFound`
            when no resource can be found.
        """
        return self._get(_app.App, app)

    def app_consumptions(self, stream_name, app_name, **params):
        """List all Streams.

        :param stream_name: Name of the stream.
        :param app_name: Name of the app to be queried.
        :param dict params: Optional query parameters to be sent to limit
            the app consumptions being returned.

        :returns: a generator of
            (:class:`~otcextensions.sdk.dis.v2.app.App`) instances
        """
        params.setdefault('checkpoint_type', 'LAST_READ')
        if params.get('limit'):
            params.update(paginated=False)
        return self._list(_app.AppConsumption, app_name=app_name,
                          stream_name=stream_name, **params)

    def delete_app(self, app, ignore_missing=False):
        """Delete a DIS App.

        :param app: The value can be the name of a DIS app.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the app does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent app.

        :returns: ``None``
        """
        return self._delete(_app.App, app, ignore_missing=ignore_missing)

    # ======== Stream ========
    def add_checkpoint(self, **attrs):
        """Add a Checkpoint from attributes

        :param dict attrs: Keyword arguments which will be used to submit
            a :class:`~otcextensions.sdk.dis.v2.checkpoint.Checkpoint`,
            comprised of the properties on the Checkpoint class.
        :returns: The results of stream creation
        :rtype: :class:`~otcextensions.sdk.dis.v2.checkpoint.Checkpoint`
        """
        attrs.update(checkpoint_type='LAST_READ')
        return self._create(_checkpoint.Checkpoint, **attrs)

    def get_checkpoint(self, stream_name, app_name,
                       partition_id, checkpoint_type='LAST_READ'):
        """Query details of a DIS stream

        :param stream_name: Name of the stream to which the checkpoint belongs.
        :param app_name: Name of the app associated with the checkpoint.
        :param partition_id: Identifier of the stream partition.
        :param checkpoint_type: Type of the checkpoint (Default: LAST_READ).
        :returns: One :class:`~otcextensions.sdk.dis.v2.checkpoint.Checkpoint`
        :raises: :class:`~openstack.exceptions.ResourceNotFound`
            when no resource can be found.
        """
        params = {
            'stream_name': stream_name,
            'app_name': app_name,
            'partition_id': partition_id,
            'checkpoint_type': checkpoint_type
        }
        # return self._get(
        #    _checkpoint.Checkpoint, requires_id=False, params=params)
        obj = self._get_resource(_checkpoint.Checkpoint, None)
        return obj.get_checkpoint(self, **params)

    def delete_checkpoint(self, stream_name, app_name,
                          partition_id=None, checkpoint_type='LAST_READ'):
        """Delete a CheckPoint Checkpoint

        :param stream_name: Name of the stream to which the checkpoint belongs.
        :param app_name: Name of the app associated with the checkpoint.
        :param partition_id: Identifier of the stream partition (Default: None)
        :param checkpoint_type: Type of the checkpoint (Default: LAST_READ).

        :returns: ``None``
        """
        params = {
            'stream_name': stream_name,
            'app_name': app_name,
            'checkpoint_type': checkpoint_type
        }
        if partition_id:
            params.update(partition_id=partition_id)

        # return self._delete(
        #    _checkpoint.Checkpoint, requires_id=False, params=params)

        obj = self._get_resource(_checkpoint.Checkpoint, None)
        return obj.delete_checkpoint(self, **params)

    # ======== Data Management ========
    def upload_data(self, **attrs):
        return self._create(_data.Data, **attrs)

    def download_data(self, **params):
        return self._list(_data.Data, **params)

    def get_data_cursor(self, **params):
        obj = _data.Data('')
        return obj.get_data_cursor(self, **params)

    # ======== Stream ========
    def create_dump_task(self, stream_name, **attrs):
        """Add OBS dump tasks.

        :param stream_name: Name of the stream.

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.dis.v2.dump_task.DumpTask`,
            comprised of the properties on the DumpTask class.
        :returns: The results of adding DumpTask.
        :rtype: :class:`~otcextensions.sdk.dis.v2.dump_task.DumpTask`
        """
        return self._create(
            _dump_task.DumpTask, uri_stream_name=stream_name, **attrs
        )

    def dump_tasks(self, stream_name):
        """List Dump Tasks.

        :param stream_name: Name of the stream.
        :returns: a generator of
            (:class:`~otcextensions.sdk.dis.v2.dump_task.DumpTask`) instances
        """
        return self._list(_dump_task.DumpTask, uri_stream_name=stream_name)

    def delete_dump_task(self, stream_name, task_name):
        """Delete Dump Task.

        :param stream_name: Name of the stream.
        :param task_name: Name of the dump task to be deleted.

        :returns: ``None``
        """
        return self._delete(_dump_task.DumpTask, task_name,
                            uri_stream_name=stream_name)

    def get_dump_task(self, stream_name, task_name):
        """Query Dump Task details.

        :param stream_name: Name of the stream..
        :param task_name: Name of the dump task to be deleted.
        :returns: One :class:`~otcextensions.sdk.dis.v2.dump_task.DumpTask`
        :raises: :class:`~openstack.exceptions.ResourceNotFound`
            when no resource can be found.
        """
        return self._get(_dump_task.DumpTask, task_name,
                         uri_stream_name=stream_name)

    def start_dump_task(self, stream_name, *task_id):
        obj = _dump_task.DumpTask()
        return obj._action(self, stream_name, 'start', *task_id)

    def pause_dump_task(self, stream_name, *task_id):
        obj = _dump_task.DumpTask()
        return obj._action(self, stream_name, 'stop', *task_id)
