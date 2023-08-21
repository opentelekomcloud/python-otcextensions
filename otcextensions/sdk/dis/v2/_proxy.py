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

import csv
import base64
import binascii
from pathlib import Path

from openstack import proxy
# from openstack import exceptions
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

    def delete_stream(self, stream_name, ignore_missing=False):
        """Delete a DIS stream.

        :param stream_name: Name of a DIS stream.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the stream does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent stream.

        :returns: ``None``
        """
        return self._delete(_stream.Stream, stream_name,
                            ignore_missing=ignore_missing)

    def update_stream_partition(self, stream_name, count):
        """Update a DIS stream partition count.

        :param stream_name: Name of a DIS stream.
        :param count: Number of the target partitions.

        :returns: ``None``
        """
        attrs = {
            'stream_name': stream_name,
            'target_partition_count': count
        }

        return self._update(_stream.Stream, stream_name, **attrs)

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

    def get_app(self, app_name):
        """Query details of a DIS App.

        :param app_name: Name of the app to be queried.
        :returns: One :class:`~otcextensions.sdk.dis.v2.app.App`
        :raises: :class:`~openstack.exceptions.ResourceNotFound`
            when no resource can be found.
        """
        return self._get(_app.App, app_name)

    def app_consumptions(self, stream_name, app_name, **params):
        """List partition consuming state list.

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

    def delete_app(self, app_name, ignore_missing=False):
        """Delete a DIS App.

        :param app_name: The value can be the name of a DIS app.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the app does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent app.

        :returns: ``None``
        """
        return self._delete(_app.App, app_name, ignore_missing=ignore_missing)

    # ======== Stream ========
    def create_checkpoint(self, **attrs):
        """Add a Checkpoint from attributes.

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
        """Query details of a Checkpoint.

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
        obj = self._get_resource(_checkpoint.Checkpoint, None)
        return obj.get_checkpoint(self, **params)

    def delete_checkpoint(self, stream_name, app_name,
                          partition_id=None, checkpoint_type='LAST_READ'):
        """Delete a Checkpoint.

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

        obj = self._get_resource(_checkpoint.Checkpoint, None)
        return obj.delete_checkpoint(self, **params)

    # ======== Data Management ========
    def upload_data(self, stream_name, stream_id=None,
                    records=None, filename=None):
        """Upload data to DIS stream.

        :param stream_name: Name of the stream.
        :param stream_id: Optional stream ID.
        :param records: List of records (if filename is not used).
        :param filename: Path to the CSV file.

        :returns: The results of uploaded data.
        :rtype: :class:`~otcextensions.sdk.dis.v2.data.Data`
        """
        def encode_data(data):
            try:
                base64.b64decode(data, validate=True)
                return data
            except binascii.Error:
                return base64.b64encode(data.encode('ascii')).decode('ascii')

        records = records if records else []
        records_data = []
        if filename:
            with Path(filename).open('r') as csv_content:
                header = next(csv.reader(csv_content, delimiter=','))
                if 'data' not in header:
                    raise ValueError(
                        f'data column is missing in the header of {filename}'
                    )
                reader = csv.DictReader(csv_content, header, delimiter=',')
                for record in reader:
                    data = record.get('data')
                    if data and data != '':
                        record['data'] = encode_data(data)
                    else:
                        raise ValueError('Data File contains empty data!')
                    records_data.append(record)
        else:
            for record in records:
                data = record.get('data')
                if data and data != '':
                    record['data'] = encode_data(data)
                else:
                    raise ValueError('data is missing in the attributes')
                records_data.append(record)

        request_attrs = {
            'stream_name': stream_name,
            'records': records_data
        }
        if stream_id:
            request_attrs.append(stream_id=stream_id)
        return self._create(_data.Data, **request_attrs)

    def download_data(self, partititon_cursor,
                      max_fetch_bytes=None, filename=None):
        """Download data from a DIS stream.

        :param partititon_cursor: Data cursor, which needs to be
            obtained through the API for obtaining data cursors.
        :param max_fetch_bytes: Maximum number of bytes
            that can be obtained for each request.
        :param filename: Path to the CSV file.

        :returns: a generator of
            (:class:`~otcextensions.sdk.dis.v2.data.Data`) instances
        """
        params = {'partition-cursor': partititon_cursor}
        if max_fetch_bytes:
            params.update(max_fetch_bytes=max_fetch_bytes)
        data = self._list(_data.Data, **params)
        if filename:
            columns = (
                'sequence_number',
                'data',
                'timestamp',
                'timestamp_type',
            )
            with open(filename, 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                # write the header
                writer.writerow(columns)
                # write multiple rows
                writer.writerows(
                    (s.sequence_number, s.data, s.timestamp,
                        s.timestamp_type) for s in data
                )
        else:
            return data

    def get_data_cursor(self, stream_name, partition_id, **params):
        """Query data cursor.

        :param stream_name: Name of the stream.
        :param partititon_id: Partition ID of the stream.
        :param dict params: Optional query parameters.

        :returns: `partition_cursor`.
        :rtype: :class:`~otcextensions.sdk.dis.v2.data.Data`
        """
        params['stream-name'] = stream_name
        params['partition-id'] = partition_id
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
        """List Dump tasks.

        :param stream_name: Name of the stream.
        :returns: a generator of
            (:class:`~otcextensions.sdk.dis.v2.dump_task.DumpTask`) instances
        """
        return self._list(_dump_task.DumpTask, uri_stream_name=stream_name)

    def delete_dump_task(self, stream_name, task_name, ignore_missing=False):
        """Delete Dump Task.

        :param stream_name: Name of the stream.
        :param task_name: Name of the dump task to be deleted.

        :returns: ``None``
        """
        return self._delete(_dump_task.DumpTask, task_name,
                            uri_stream_name=stream_name,
                            ignore_missing=ignore_missing)

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
        """Start dump tasks in batches.

        :param stream_name: Name of the stream.
        :param task_id: Dump task ID(s).
        :returns: ``None``
        """
        obj = _dump_task.DumpTask()
        return obj._action(self, stream_name, 'start', *task_id)

    def pause_dump_task(self, stream_name, *task_id):
        """Pause dump tasks in batches.

        :param stream_name: Name of the stream.
        :param task_id: Dump task ID(s).
        :returns: ``None``
        """
        obj = _dump_task.DumpTask()
        return obj._action(self, stream_name, 'stop', *task_id)
