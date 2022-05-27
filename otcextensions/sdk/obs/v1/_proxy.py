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
import os
from urllib import parse

from openstack import exceptions
from urllib3.exceptions import LocationParseError

from otcextensions.common import utils
from otcextensions.sdk import ak_auth
from otcextensions.sdk import sdk_proxy
from otcextensions.sdk.obs.v1 import container as _container
from otcextensions.sdk.obs.v1 import obj as _obj

DEFAULT_OBJECT_SEGMENT_SIZE = 1073741824  # 1GB
DEFAULT_MAX_FILE_SIZE = (5 * 1024 * 1024 * 1024 + 2) / 2
EXPIRES_ISO8601_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
SHORT_EXPIRES_ISO8601_FORMAT = '%Y-%m-%d'


def _normalize_obs_keys(obj):
    return {k.lower(): v for k, v in obj.items()}


class Proxy(sdk_proxy.Proxy):
    skip_discovery = True

    CONTAINER_ENDPOINT = \
        'https://%(container)s.obs.%(region_name)s.otc.t-systems.com'

    def _extract_name(self, url, service_type=None, project_id=None):
        url_path = parse.urlparse(url).path.strip()
        # Remove / from the beginning to keep the list indexes of interesting
        # things consistent
        if url_path.startswith('/'):
            url_path = url_path[1:]

        # Split url into parts and exclude potential project_id in some urls
        url_parts = url_path.split('/')

        # Strip out anything that's empty or None
        parts = [part for part in url_parts if part]

        # Getting the root of an endpoint is a bucket operation
        if not parts:
            return ['bucket']
        else:
            return ['object']

    def get_container_endpoint(self, container):
        """Override to return mapped endpoint if override and region are set

        """
        region_name = getattr(self, 'region_name', 'eu-de')
        if not region_name:
            region_name = 'eu-de'
        endpoint = self.CONTAINER_ENDPOINT % {
            'container': container,
            'region_name': region_name
        }
        return endpoint

    def _get_req_auth(self, host=None):
        auth = getattr(self, '_ak_auth', None)
        if not auth:
            ak = None
            sk = None
            conn = self.session._sdk_connection
            if hasattr(conn, 'get_ak_sk'):
                (ak, sk) = conn.get_ak_sk(conn)
            if not (ak and sk):
                self.log.error('Cannot obtain AK/SK from config')
                return None
            region = getattr(self, 'region_name', 'eu-de')
            if not region:
                region = 'eu-de'
            if not host:
                host = self.get_endpoint()

            auth = ak_auth.AKRequestsAuth(
                access_key=ak,
                secret_access_key=sk,
                host=host,
                region=region,
                service='s3'
            )
            setattr(self, '_ak_auth', auth)
        return auth

    # ======== Containers ========

    def containers(self, **query):
        """Obtain Container objects for this account.

        :param kwargs query: Optional query parameters to be sent to limit
                                 the resources being returned.

        :rtype: A generator of
            :class:`~otcextensions.sdk.obs.v1.container.Container` objects.
        """
        return self._list(_container.Container,
                          requests_auth=self._get_req_auth(),
                          **query)

    def get_container(self, container):
        """Get the detail of a container

        :param container: Container name or an object of class
                   :class:`~otcextensions.sdk.obs.v1.container.Container`
        :returns: Detail of container
        :rtype: :class:`~otcextensions.sdk.obs.v1.container.Container`
        """
        container = self._get_container_name(container=container)
        endpoint = self.get_container_endpoint(container)
        return self._head(
            _container.Container,
            container,
            endpoint_override=endpoint,
            requests_auth=self._get_req_auth(endpoint))

    def create_container(self, **attrs):
        """Create a new container from attributes

        :param container: Name of the container to create.
        :param dict attrs: Keyword arguments which will be used to create
               a :class:`~otcextensions.sdk.obs.v1.container.Container`,
               comprised of the properties on the Container class.

        :returns: The results of container creation
        :rtype: :class:`~otcextensions.sdk.obs.v1.container.Container`
        """
        container = attrs.get('name', None)
        endpoint = self.get_container_endpoint(container)
        return self._create(
            _container.Container,
            endpoint_override=endpoint,
            requests_auth=self._get_req_auth(endpoint),
            # prepend_key=False,
            **attrs)

    def delete_container(self, container, ignore_missing=True):
        """Delete a container

        :param container: The value can be either the name of a container or a
                      :class:`~otcextensions.sdk.obs.v1.container.Container`
                      instance.
        :param bool ignore_missing: When set to ``False``
                    :class:`~openstack.exceptions.ResourceNotFound` will be
                    raised when the container does not exist.
                    When set to ``True``, no exception will be set when
                    attempting to delete a nonexistent server.

        :returns: ``None``
        """
        container = self._get_container_name(container=container)
        endpoint = self.get_container_endpoint(container)
        self._delete(_container.Container, container,
                     endpoint_override=endpoint,
                     requests_auth=self._get_req_auth(endpoint),
                     ignore_missing=ignore_missing)

    def get_container_metadata(self, container):
        """Get metadata for a container

        :param container: The value can be the name of a container or a
               :class:`~otcextensions.sdk.obs.v1.container.Container`
               instance.

        :returns: One :class:`~otcextensions.sdk.obs.v1.container.Container`
        :raises: :class:`~openstack.exceptions.ResourceNotFound`
                 when no resource can be found.
        """
        raise NotImplementedError
        return self._head(_container.Container, container)

    def set_container_metadata(self, container, **metadata):
        """Set metadata for a container.

        :param container: The value can be the name of a container or a
               :class:`~otcextensions.sdk.obs.v1.container.Container`
               instance.
        :param kwargs metadata: Key/value pairs to be set as metadata
                                on the container. Both custom and system
                                metadata can be set. Custom metadata are keys
                                and values defined by the user. System
                                metadata are keys defined by the Object Store
                                and values defined by the user. The system
                                metadata keys are:

                                - `content_type`
                                - `is_content_type_detected`
                                - `versions_location`
                                - `read_ACL`
                                - `write_ACL`
                                - `sync_to`
                                - `sync_key`
        """
        raise NotImplementedError
        res = self._get_resource(_container.Container, container)
        res.set_metadata(self, metadata)
        return res

    def delete_container_metadata(self, container, keys):
        """Delete metadata for a container.

        :param container: The value can be the ID of a container or a
               :class:`~otcextensions.sdk.obs.v1.container.Container`
               instance.
        :param keys: The keys of metadata to be deleted.
        """
        raise NotImplementedError
        res = self._get_resource(_container.Container, container)
        res.delete_metadata(self, keys)
        return res

    # ======== Objects ========

    def objects(self, container, **query):
        """Return a generator that yields the Container's objects.

        :param container: A container object or the name of a container
            that you want to retrieve objects from.
        :type container:
            :class:`~otcextensions.sdk.obs.v1.container.Container`
        :param kwargs query: Optional query parameters to be sent to limit
                               the resources being returned.

        :rtype: A generator of
            :class:`~otcextensions.sdk.obs.v1.obj.Object` objects.
        """
        container = self._get_container_name(container=container)
        endpoint = self.get_container_endpoint(container)
        return self._list(
            _obj.Object,
            endpoint_override=endpoint,
            requests_auth=self._get_req_auth(endpoint), **query)

    def _get_container_name(self, obj=None, container=None):
        if obj is not None:
            obj = self._get_resource(_obj.Object, obj)
            if obj.container is not None:
                return obj.container
        if container is not None:
            container = self._get_resource(_container.Container, container)
            return container.name

        raise ValueError("container must be specified")

    def get_object(self, obj, container=None):
        """Get the data associated with an object

        :param obj: The value can be the name of an object or a
                       :class:`~otcextensions.sdk.obs.v1.obj.Object` instance.
        :param container: The value can be the name of a container or a
               :class:`~otcextensions.sdk.obs.v1.container.Container`
               instance.

        :returns: The contents of the object.  Use the
                  :func:`~get_object_metadata`
                  method if you want an object resource.
        :raises: :class:`~openstack.exceptions.ResourceNotFound`
                 when no resource can be found.
        """
        container_name = self._get_container_name(
            obj=obj, container=container)
        endpoint = self.get_container_endpoint(container_name)
        return self._get(_obj.Object, obj, container=container_name,
                         endpoint_override=endpoint,
                         requests_auth=self._get_req_auth(endpoint))

    def download_object(self, obj, container=None, **attrs):
        """Download the data contained inside an object.

        :param obj: The value can be the name of an object or a
                       :class:`~otcextensions.sdk.obs.v1.obj.Object` instance.
        :param container: The value can be the name of a container or a
               :class:`~otcextensions.sdk.obs.v1.container.Container`
               instance.

        :raises: :class:`~openstack.exceptions.ResourceNotFound`
                 when no resource can be found.
        """
        container_name = self._get_container_name(
            obj=obj, container=container)
        endpoint = self.get_container_endpoint(container_name)
        obj = self._get_resource(
            _obj.Object, obj, container=container_name, **attrs)
        return obj.download(
            self,
            endpoint_override=endpoint,
            requests_auth=self._get_req_auth(endpoint),
            filename=attrs.pop('file', '-'))

    def stream_object(self, obj, container=None, chunk_size=1024, **attrs):
        """Stream the data contained inside an object.

        :param obj: The value can be the name of an object or a
                       :class:`~otcextensions.sdk.obs.v1.obj.Object` instance.
        :param container: The value can be the name of a container or a
               :class:`~otcextensions.sdk.obs.v1.container.Container`
               instance.

        :raises: :class:`~openstack.exceptions.ResourceNotFound`
                 when no resource can be found.
        :returns: An iterator that iterates over chunk_size bytes
        """
        raise NotImplementedError
        # container_name = self._get_container_name(
        #     obj=obj, container=container)
        container_name = self._get_container_name(container=container)
        endpoint = self.get_container_endpoint(container_name)
        obj = self._get_resource(
            _obj.Object, obj, container=container_name,
            endpoint_override=endpoint,
            requests_auth=self._get_req_auth(endpoint),
            **attrs)
        return obj.stream(self, chunk_size=chunk_size)

    def create_object(self, container, name, filename=None, data=None,
                      segment_size=None, md5=None,
                      generate_checksums=None,
                      **headers):
        """Upload a new object from attributes

        :param generate_checksums: Whether to generate checksums on the client
            side that get added to headers for later prevention of double
            uploads of identical data. (optional, defaults to True)
        :param md5: A hexadecimal md5 of the file. (Optional), if it is known
            and can be passed here, it will save repeating the expensive md5
            process. It is assumed to be accurate.
        :param segment_size: Break the uploaded object into segments of this
            many bytes. (Optional) SDK will attempt to discover the maximum
            value for this from the server if it is not specified, or will use
            a reasonable default.
        :param container: The value can be the name of a container or a
               :class:`~otcextensions.sdk.obs.v1.container.Container`
               instance.
        :param name: Name of the object to create.
        :param data: The content to upload to the object. Mutually exclusive
            with filename.
        :param filename: The path to the local file whose contents will be
            uploaded. Mutually exclusive with data.
        :param dict attrs: Keyword arguments which will be used to create
               a :class:`~otcextensions.sdk.obs.v1.obj.Object`,
               comprised of the properties on the Object class.

        :returns: The results of object creation
        :rtype: :class:`~otcextensions.sdk.obs.v1.container.Container`
        """
        if data is not None and filename:
            raise ValueError(
                "Both filename and data given. Please choose one.")

        if not filename and data is None:
            filename = name

        container = self._get_container_name(container=container)
        endpoint = self.get_container_endpoint(container)

        if data is not None:
            self.log.debug(
                "uploading data to %(endpoint)s",
                {'endpoint': endpoint})
            return self._create(
                _obj.Object, container=container,
                name=name, data=data,
                endpoint_override=endpoint,
                requests_auth=self._get_req_auth(endpoint),
                **headers)

        if segment_size:
            segment_size = int(segment_size)
        segment_size = self.get_object_segment_size(segment_size)
        file_size = os.path.getsize(filename)

        if generate_checksums and md5 is None:
            md5 = utils._get_file_hashes(filename)

        if self.is_object_stale(container, name, filename, md5):

            self.log.debug(
                "uploading %(filename)s to %(endpoint)s",
                {'filename': filename, 'endpoint': endpoint})

            if file_size <= segment_size:
                self._upload_object(endpoint, filename, headers, name)
            else:
                self._upload_large_object(
                    endpoint, filename, headers,
                    file_size, segment_size)

    # Backwards compat
    upload_object = create_object

    def _upload_object(self, endpoint, filename, headers, name=None):
        if not name:
            name = os.path.basename(filename)
        with open(filename, 'rb') as dt:
            return self._create(
                _obj.Object,
                name=name, data=dt,
                endpoint_override=endpoint,
                requests_auth=self._get_req_auth(endpoint),
                **headers)

    def _upload_large_object(self, endpoint, filename, headers,
                             file_size, segment_size):
        """
        If the object is big, we need to break it up into segments that
        are no larger than segment_size, upload each of them individually
        and then upload a manifest object. The segments can be uploaded in
        parallel, so we'll use the async feature of the TaskManager.
        """

        segment_futures = []
        segment_results = []
        retry_results = []
        retry_futures = []
        manifest = []

        object_name = os.path.basename(filename)
        requests_auth = self._get_req_auth(endpoint)
        segments = utils._get_file_segments(
            endpoint, filename, file_size, segment_size)

        upload_id = _obj.Object.initiate_multipart_upload(
            self, endpoint, object_name,
            requests_auth=requests_auth
        )
        url = f'{endpoint}/{object_name}'
        # Schedule the segments for upload
        for name, segment in segments.items():
            # Async call to put - schedules execution and returns a future
            segment_future = self._connection._pool_executor.submit(
                self.put,
                f'{url}?partNumber={name[-1]}&uploadId={upload_id}',
                headers=headers, data=segment,
                requests_auth=requests_auth,
                raise_exc=False)
            segment_futures.append(segment_future)
            # dict. Then sort the list of dicts by path.
            manifest.append(dict(
                path='/{name}'.format(name=name),
                size_bytes=segment.length))

        segment_results, retry_results = self._connection._wait_for_futures(
            segment_futures, raise_on_error=False)

        for result in retry_results:
            # Grab the FileSegment for the failed upload so we can retry
            name = self._object_name_from_url(result.url)
            segment = segments[name]
            segment.seek(0)
            # Async call to put - schedules execution and returns a future
            segment_future = self._connection._pool_executor.submit(
                self.put,
                f'{url}?partNumber={name[-1]}&uploadId={upload_id}',
                headers=headers, data=segment,
                requests_auth=requests_auth
            )
            # dict. Then sort the list of dicts by path.
            retry_futures.append(segment_future)

        # If any segments fail the second time, just throw the error
        segment_results, retry_results = self._connection._wait_for_futures(
            retry_futures, raise_on_error=True)

        try:
            return self._finish_large_object_upload(
                url, headers, upload_id)
        except Exception:
            try:
                self.log.debug(
                    "Failed to upload large object for %s. "
                    "Aborting uploads.", upload_id)
                self._abort_multipart_upload(endpoint=url,
                                             upload_id=upload_id)
            except Exception:
                self.log.exception(
                    "Failed to cleanup image objects for %s:",
                    upload_id)
            raise

    def parts(self, endpoint, upload_id, requests_auth):
        return _obj.Object.get_parts(
            self, f'{endpoint}?uploadId={upload_id}', requests_auth)

    def _finish_large_object_upload(self, endpoint, headers, upload_id):
        requests_auth = self._get_req_auth(endpoint)
        parts = self.parts(endpoint, upload_id, requests_auth)
        retries = 3
        while True:
            try:
                return exceptions.raise_from_response(
                    _obj.Object.complete_multipart_upload(
                        self, endpoint, upload_id,
                        parts['Parts'], headers,
                        requests_auth=requests_auth
                    ))
            except Exception:
                retries -= 1
                if retries == 0:
                    raise

    def _object_name_from_url(self, url):
        '''Get container_name/object_name from the full URL called.
        Remove the Swift endpoint from the front of the URL, and remove
        the leaving / that will leave behind.'''
        endpoint = self.get_endpoint()
        object_name = url.replace(endpoint, '')
        if object_name.startswith('/'):
            object_name = object_name[1:]
        return object_name

    def is_object_stale(
            self, container, name, filename, file_md5=None):
        """Check to see if an object matches the hashes of a file.
        :param container: Name of the container.
        :param name: Name of the object.
        :param filename: Path to the file.
        :param file_md5: Pre-calculated md5 of the file contents. Defaults to
            None which means calculate locally.
        """
        try:
            metadata = self.get_object_metadata(name, container)
        except (exceptions.NotFoundException, LocationParseError):
            self.log.debug(
                "swift stale check, no object: {container}/{name}".format(
                    container=container, name=name))
            return True

        if not file_md5:
            file_md5 = utils._get_file_hashes(filename)
        if file_md5 == metadata.etag.strip('\"'):
            self.log.debug(
                "swift object up to date: %(container)s/%(name)s",
                {'container': container, 'name': name})
            return False
        self.log.debug(
            "swift checksum mismatch: "
            " %(filename)s!=%(container)s/%(name)s",
            {'filename': filename, 'container': container, 'name': name})
        return True

    def get_object_segment_size(self, segment_size):
        """Get a segment size that will work given capabilities"""
        if segment_size is None:
            segment_size = DEFAULT_OBJECT_SEGMENT_SIZE
        min_segment_size = 0
        server_max_file_size = DEFAULT_MAX_FILE_SIZE

        if segment_size > server_max_file_size:
            return server_max_file_size
        if segment_size < min_segment_size:
            return min_segment_size
        return segment_size

    def copy_object(self):
        """Copy an object."""
        raise NotImplementedError

    def delete_object(self, obj, ignore_missing=True, container=None):
        """Delete an object

        :param obj: The value can be either the name of an object or a
                       :class:`~otcextensions.sdk.obs.v1.container.Container`
                       instance.
        :param container: The value can be the ID of a container or a
               :class:`~otcextensions.sdk.obs.v1.container.Container`
               instance.
        :param bool ignore_missing: When set to ``False``
                    :class:`~openstack.exceptions.ResourceNotFound` will be
                    raised when the object does not exist.
                    When set to ``True``, no exception will be set when
                    attempting to delete a nonexistent server.

        :returns: ``None``
        """
        container_name = self._get_container_name(obj, container)
        endpoint = self.get_container_endpoint(container_name)
        self._delete(_obj.Object, obj, ignore_missing=ignore_missing,
                     container=container_name,
                     endpoint_override=endpoint,
                     requests_auth=self._get_req_auth(endpoint),
                     )

    def get_object_metadata(self, obj, container=None):
        """Get metadata for an object.

        :param obj: The value can be the name of an object or a
                    :class:`~otcextensions.sdk.obs.v1.obj.Object` instance.
        :param container: The value can be the ID of a container or a
               :class:`~otcextensions.sdk.obs.v1.container.Container`
               instance.

        :returns: One :class:`~otcextensions.sdk.obs.v1.obj.Object`
        :raises: :class:`~openstack.exceptions.ResourceNotFound`
                 when no resource can be found.
        """
        container_name = self._get_container_name(obj, container)
        endpoint = self.get_container_endpoint(container_name)

        return self._head(_obj.Object, obj, container=container_name,
                          endpoint_override=endpoint,
                          requests_auth=self._get_req_auth(endpoint))

    def set_object_metadata(self, obj, container=None, **metadata):
        """Set metadata for an object.

        Note: This method will do an extra HEAD call.

        :param obj: The value can be the name of an object or a
                    :class:`~otcextensions.sdk.obs.v1.obj.Object` instance.
        :param container: The value can be the name of a container or a
               :class:`~otcextensions.sdk.obs.v1.container.Container`
               instance.
        :param kwargs metadata: Key/value pairs to be set as metadata
                                on the container. Both custom and system
                                metadata can be set. Custom metadata are keys
                                and values defined by the user. System
                                metadata are keys defined by the Object Store
                                and values defined by the user. The system
                                metadata keys are:

                                - `content_type`
                                - `content_encoding`
                                - `content_disposition`
                                - `delete_after`
                                - `delete_at`
                                - `is_content_type_detected`
        """
        raise NotImplementedError
        container_name = self._get_container_name(obj, container)
        res = self._get_resource(_obj.Object, obj, container=container_name)
        res.set_metadata(self, metadata)
        return res

    def delete_object_metadata(self, obj, container=None, keys=None):
        """Delete metadata for an object.

        :param obj: The value can be the name of an object or a
                    :class:`~otcextensions.sdk.obs.v1.obj.Object` instance.
        :param container: The value can be the ID of a container or a
               :class:`~otcextensions.sdk.obs.v1.container.Container`
               instance.
        :param keys: The keys of metadata to be deleted.
        """
        raise NotImplementedError
        container_name = self._get_container_name(obj, container)
        res = self._get_resource(_obj.Object, obj, container=container_name)
        res.delete_metadata(self, keys)
        return res

    def _abort_multipart_upload(
            self, endpoint, upload_id
    ):
        """Aborts all multipart upload objects.
        :param endpoint: Container endpoint
        :param upload_id: ID of the multipart upload to be aborted.
        :return:
        """
        url = f'{endpoint}?uploadId={upload_id}'
        return self.delete(url, requests_auth=self._get_req_auth(endpoint))
