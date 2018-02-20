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

from openstack import _log
from openstack import proxy

import boto3
from botocore.exceptions import ClientError

from openstack import exceptions

from otcextensions.i18n import _

from otcextensions.sdk.obs.v1.bucket import Bucket
from otcextensions.sdk.obs.v1.object import Object

_logger = _log.setup_logging('openstack')

# TODO(agoncharov) regulate use of exceptions


def _normalize_obs_keys(obj):
    return {k.lower(): v for k, v in obj.items()}


class Proxy(proxy.BaseProxy):

    SESSION_ATTR_NAME = '_boto_session'

    def _set_ak(self, ak, sk):
        """Inject AK/SK into the proxy for use

        """
        _logger.debug('injecting ak/sk')
        setattr(self, 'AK', ak)
        setattr(self, 'SK', sk)

        pass

    def get_endpoint(self, **kwargs):
        """Override to return mapped endpoint if override and region are set

        """
        region = getattr(self, 'region_name', 'eu-de')
        if not region:
            # region_name attr might be set to empty
            region = 'eu-de'
        override = getattr(self, 'endpoint_override',
                           'https://obs.%(region_name)s.otc.t-systems.com')
        if region and override:
            return override % {'region_name': region}
        else:
            return super(Proxy, self).get_endpoint(**kwargs)

    def _establish_session(self):
        _logger.debug('establishing session')
        region = getattr(self, 'region_name', None)
        ak = getattr(self, 'AK', None)
        sk = getattr(self, 'SK', None)

        if not region:
            _logger.debug('region is not set in the connection. '
                          'Default is used')
        if ak and sk:
            _logger.debug('SK/AK available, establish connection')
            otcsession = boto3.session.Session()

            s3client = otcsession.client(
                's3',
                region,
                # config=boto3.session.Config(signature_version='s3v4'),
                endpoint_url=self.get_endpoint(),
                aws_access_key_id=ak,
                aws_secret_access_key=sk
            )
            setattr(self, Proxy.SESSION_ATTR_NAME, s3client)
            return s3client
        else:
            _logger.error('Some of AK/SK/Region is not set, abort')
            return False

    def _get_session(self):
        """Retrieve internal session

        """
        s3session = getattr(self, Proxy.SESSION_ATTR_NAME, None)
        if not s3session:
            s3session = self._establish_session()
        return s3session

    def buckets(self, **attrs):
        """Get all buckets

        """
        _logger.debug('OBS.buckets')
        s3 = self._get_session()
        if not s3:
            _logger.error('session is not there. Please retry')
            raise exceptions.SDKException(
                _('OBS internal connection does not exist. Please retry'))
        else:
            try:
                result = (
                    # convert keys to lower case for further use
                    Bucket(**{k.lower(): v for k, v in bucket.items()})
                    for bucket in s3.list_buckets()["Buckets"])
                return result
            except ClientError as e:
                print(str(e))

    def get_bucket(self, bucket, **attrs):
        """Get the bucket

        Fetches the bucket from OBS (ensures it's existence).
        Important is only the bucket name

        :param Bucket bucket: the bucket (i.e. created) to fetch

        """
        _logger.debug('OBS.bucket')
        # ensure bucket HEAD request is ok
        result = self.get_bucket_by_name(bucket.name)

        return result

    def create_bucket(self, name, **attrs):
        """Creates the bucket (container)

        :param string name: Bucket name
        :param **dict attrs: Additional attributes (not supported ATM)

        Returns created bucket
        """
        _logger.debug('OBS.create_bucket')
        s3 = self._get_session()

        if not s3:
            _logger.error('session is not there. Please retry')
            raise exceptions.SDKException(
                _('OBS internal connection does not exist. Please retry'))

        s3.create_bucket(
            Bucket=name
        )

        return Bucket(**{'name': name})

    def get_bucket_by_name(self, bucket_name, **attrs):
        """Get the bucket

        """
        _logger.debug('OBS.bucket')

        s3 = self._get_session()

        if not s3:
            _logger.error('session is not there. Please retry')
            raise exceptions.SDKException(
                _('OBS internal connection does not exist. Please retry'))

        result = None
        if True:
            # Since no bucket GET is present in OBS - list buckets
            for bckt in self.buckets():
                if bckt.name == bucket_name:
                    result = bckt
            if not result:
                _logger.error('bucket head succedded, '
                              'but it is not present in ls')
                raise exceptions.SDKException(
                    _('Bucket HEAD was ok, but in the list it was not found'))

        return result

    def objects(self, bucket, **attrs):
        """List objects in the bucket

        """
        _logger.debug('OBS.objects')
        s3 = self._get_session()

        if not s3:
            _logger.error('session is not there. Please retry')
            raise exceptions.SDKException(
                _('OBS internal connection does not exist. Please retry'))

        result = None
        try:
            # convert keys to lower case for further use
            objects = (
                _normalize_obs_keys(obj)
                for obj in s3.list_objects(
                    Bucket=bucket.name,
                    **attrs
                )["Contents"]
            )
            result = (Object(**obj) for obj in objects)
        except ClientError as e:
            print(str(e))

        return result

    def get_object_by_key(self, bucket, key, **attrs):
        """Get object from the bucket by name

        """
        _logger.debug('OBS.get_object_by_key')
        s3 = self._get_session()

        if not s3:
            _logger.error('session is not there. Please retry')
            raise exceptions.SDKException(
                _('OBS internal connection does not exist. Please retry'))

        result = None
        try:
            object_head = _normalize_obs_keys(
                s3.head_object(Bucket=bucket.name, Key=key, **attrs))
            _logger.debug('object data is %s' % object_head)
            object_head['size'] = object_head['contentlength']
            object_head['key'] = key
            object_head['bucket'] = bucket.name
            result = Object(**object_head)
        except ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if 404 == error_code:
                raise exceptions.ResourceNotFound(
                    _('Object is not present'))
            print(str(e))

        return result

    def get_object(self, bucket, obj, **attrs):
        """HEAD object

        refetch the Object

        :param Bucket bucket: bucket
        :param Object obj: Object to fetch (key should be set)

        """
        _logger.debug('OBS.get_object')

        return self.get_object_by_key(bucket, obj.key)

    def create_object(self, bucket, name, filename, **attrs):
        """Upload a new object from attributes

        :param bucket: The value can be the name of a bucket or a
               :class:`~otcextensions.sdk.obs.v1.Bucket`
               instance.
        :param name: Name (key) of the object to create.
        :param file: File ptr
        :param dict attrs: Keyword arguments which will be used to create
               a :class:`~openstack.object_store.v1.obj.Object`,
               comprised of the properties on the Object class.

        :returns: The results of object creation
        :rtype: :class:`~openstack.object_store.v1.container.Container`
        """
        _logger.debug('OBS.create_object')
        s3 = self._get_session()

        if not s3:
            _logger.error('session is not there. Please retry')
            raise exceptions.SDKException(
                _('OBS internal connection does not exist. Please retry'))

        # Ensure bucket exists
        self._head_bucket(bucket_name=bucket.name)

        if os.path.isfile(filename) and os.access(filename, os.R_OK):
            _logger.debug('uploading file %s to OBS' % filename)
            s3.upload_file(
                filename,
                bucket.name,
                name
            )
        else:
            _logger.error('given file is not accessible')
            raise exceptions.SDKException(
                _('File %s is not accessible') % filename)

    def download_object(self, obj, filename, **attrs):
        """Download the data contained inside an object into the file

        :param obj: The value can be the name of an object or a
                       :class:`~openstack.object_store.v1.obj.Object` instance.
        :param filename: Filename to which object content will be saved

        :raises: :class:`~openstack.exceptions.ResourceNotFound`
                 when no resource can be found.
        """
        _logger.debug('OBS.download_object')
        s3 = self._get_session()

        if not s3:
            _logger.error('session is not there. Please retry')
            raise exceptions.SDKException(
                _('OBS internal connection does not exist. Please retry'))

        if not obj or not isinstance(obj, Object):
            raise exceptions.ResourceNotFound(_('Object is not present'))

        try:
            s3.download_file(
                Bucket=obj.bucket,
                Key=obj.key,
                Filename=filename
            )
        except ClientError as e:
            raise exceptions.SDKException(
                _('OBS internal error occured '
                  'while downloading object (%s)') % str(e))

    def _head_bucket(self, bucket_name, **kwargs):
        """Head bucket - ensure bucket existence

        """
        s3 = self._get_session()
        try:
            return s3.head_bucket(Bucket=bucket_name, **kwargs)
        except ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if 404 == error_code:
                raise exceptions.ResourceNotFound(
                    _('Bucket is not present'))

            raise exceptions.SDKException(
                _('OBS internal error (%s)') % str(e)
            )

    def _head_object(self, bucket, object_name, **kwargs):
        """Head object - ensure object existence

        """
        s3 = self._get_session()
        try:
            return s3.head_object(
                Bucket=bucket.name,
                Key=object_name,
                **kwargs)
        except ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if 404 == error_code:
                raise exceptions.ResourceNotFound(
                    _('Object is not present'))

            raise exceptions.SDKException(
                _('OBS internal error (%s)') % str(e)
            )
