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

# from xml.etree import ElementTree

from openstack import _log

from otcextensions.i18n import _

from openstack import exceptions

from otcextensions.sdk.obs import obs_service

from otcextensions.sdk import sdk_resource
from otcextensions.sdk import ak_auth

import boto3
from botocore.exceptions import ClientError

_logger = _log.setup_logging('openstack')


class BaseResource(sdk_resource.Resource):
    SESSION_ATTR_NAME = '_boto_session'
    service = obs_service.ObsService()

    @classmethod
    def _get_endpoint(cls, session):
        """Return a proper endpoint

        """
        session = cls._get_session(session)
        region = getattr(session, 'region_name', None)
        endpoint = session.get_endpoint(
            service_type='object',
            service_name='objectstorage',
            region_name=region)

        if not endpoint:
            raise exceptions.SDKException(
                _('Can\'t get endpoint from the catalogue for the '
                  'service_type = %(type)s, service_name = %(name)s') %
                {'type': 'object', 'name': 'objectstoage'}
            )
        else:
            _logger.debug('endpoint for OBS is %s' % endpoint)

        return endpoint

    @classmethod
    def _establish_session(cls, session):
        """Establish BOTO3 (AWS) session to the server

        """
        _logger.debug('establishing session')
        region = getattr(session, 'region_name', None)
        ak = getattr(session, 'AK', None)
        sk = getattr(session, 'SK', None)
        endpoint = cls._get_endpoint(session)

        # if not region:
        #     _logger.debug('region is not set in the connection. '
        #                   'Default is used')
        if ak and sk:
            _logger.debug('SK/AK available, establish connection')
            otcsession = boto3.session.Session()

            s3client = otcsession.client(
                's3',
                region,
                # config=boto3.session.Config(signature_version='s3v4'),
                endpoint_url=endpoint,
                aws_access_key_id=ak,
                aws_secret_access_key=sk
            )
            setattr(session, BaseResource.SESSION_ATTR_NAME, s3client)
            return s3client
        else:
            _logger.error('Some of AK/SK/Region is not set, abort')
            return False

    @classmethod
    def _get_req_auth(cls, session):
        auth = getattr(session, '_ak_auth', None)
        if not auth:
            region = getattr(session, 'region_name', None)
            ak = getattr(session, 'AK', None)
            sk = getattr(session, 'SK', None)
            endpoint = cls._get_endpoint(session)

            auth = ak_auth.AKRequestsAuth(
                access_key=ak,
                secret_access_key=sk,
                host=endpoint,
                region=region,
                service='s3'
            )
            setattr(session, '_ak_auth', auth)
        return auth

    @classmethod
    def _get_boto_session(cls, session):
        """Retrieve internal session

        """
        s3session = getattr(session, BaseResource.SESSION_ATTR_NAME, None)
        if not s3session:
            s3session = cls._establish_session(session)
        return s3session

    def _create(self, session, remote_method, prepend_key=True):
        """Create a remote resource based on this instance.

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param prepend_key: A boolean indicating whether the resource_key
                            should be prepended in a resource creation
                            request. Default to True.

        :return: This :class:`Resource` instance.
        :raises: :exc:`~openstack.exceptions.MethodNotSupported` if
                 :data:`Resource.allow_create` is not set to ``True``.
        """
        request = self._prepare_request(
            requires_id=True, prepend_key=prepend_key)

        session = self._get_boto_session(session)
        response = None
        try:
            func = getattr(session, remote_method)
            response = func(**request.body)
        except ClientError as e:
            raise exceptions.SDKException(_(str(e)))

        self._translate_response(response, has_body=False)
        return self

    def delete(self, session, remote_method, error_message=None):
        """Delete the remote resource based on this instance.

        This function overrides default Resource.delete to enable headers

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`

        :return: This :class:`Resource` instance.
        :raises: :exc:`~openstack.exceptions.MethodNotSupported` if
                 :data:`Resource.allow_update` is not set to ``True``.
        """
        if not self.allow_delete:
            raise exceptions.MethodNotSupported(self, "delete")

        request = self._prepare_request()
        session = self._get_boto_session(session)

        response = None
        try:
            func = getattr(session, remote_method)
            response = func(**request.body)
        except ClientError as e:
            raise exceptions.SDKException(_(str(e)))

        kwargs = {}
        if error_message:
            kwargs['error_message'] = error_message

        self._translate_response(response, has_body=False, **kwargs)
        return self

    def get(self, session, remote_method,
            error_message=None, requires_id=True):
        """Get a remote resource based on this instance.

        This function overrides default Resource.get to enable GET headers

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param boolean requires_id: A boolean indicating whether resource ID
                                    should be part of the requested URI.
        :return: This :class:`Resource` instance.
        :raises: :exc:`~openstack.exceptions.MethodNotSupported` if
                 :data:`Resource.allow_get` is not set to ``True``.
        """
        if not self.allow_get:
            raise exceptions.MethodNotSupported(self, "get")

        request = self._prepare_request(requires_id=requires_id)
        session = self._get_boto_session(session)
        # sess = self._get_session(session)
        # req_auth = self._get_req_auth(session)

        response = None
        try:
            func = getattr(session, remote_method)
            response = func(**request.body)
        except ClientError as e:
            raise exceptions.SDKException(_(str(e)))

        kwargs = {}
        if error_message:
            kwargs['error_message'] = error_message

        self._translate_response(response, **kwargs)

        return self

    @classmethod
    def _list(cls, session, remote_func, normalize_func,
              paginated=False, **params):
        """Override default list to incorporate endpoint overriding
        and custom headers

        Since SDK Resource.list method is passing hardcoded headers
        do override the function

        This resource object list generator handles pagination and takes query
        params for response filtering.

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param remote_func: session function to be invoked
        :param normalize_func: class function to translate response keys
        :param bool paginated: ``True`` if a GET to this resource returns
                               a paginated series of responses, or ``False``
                               if a GET returns only one page of data.
                               **When paginated is False only one
                               page of data will be returned regardless
                               of the API's support of pagination.**
        :param dict params: These keyword arguments are passed through the
            :meth:`~openstack.resource.QueryParamter._transpose` method
            to find if any of them match expected query parameters to be
            sent in the *params* argument to
            :meth:`~keystoneauth1.adapter.Adapter.get`. They are additionally
            checked against the
            :data:`~openstack.resource.Resource.base_path` format string
            to see if any path fragments need to be filled in by the contents
            of this argument.

        :return: A generator of :class:`Resource` objects.
        :raises: :exc:`~openstack.exceptions.MethodNotSupported` if
                 :data:`Resource.allow_list` is not set to ``True``.
        :raises: :exc:`~openstack.exceptions.InvalidResourceQuery` if query
                 contains invalid params.

        """

        if not cls.allow_list:
            raise exceptions.MethodNotSupported(cls, "list")

        session = cls._get_boto_session(session)

        cls._query_mapping._validate(params, base_path=cls.base_path)
        query_params = cls._query_mapping._transpose(params)
        uri = cls.base_path % params

        # limit = query_params.get('limit')

        total_yielded = 0
        while uri:
            func = getattr(session, remote_func)
            response = func(**query_params.copy())
            # exceptions.raise_from_response(response_mock)
            # data = response

            if cls.resources_key:
                resources = response[cls.resources_key]
            else:
                resources = response

            if not isinstance(resources, list):
                resources = [resources]

            for raw_resource in resources:
                # Do not allow keys called "self" through. Glance chose
                # to name a key "self", so we need to pop it out because
                # we can't send it through cls.existing and into the
                # Resource initializer. "self" is already the first
                # argument and is practically a reserved word.
                raw_resource.pop("self", None)
                func = getattr(cls, normalize_func)
                resource = func(raw_resource)

                value = cls.existing(**resource)

                # marker = value.id
                yield value
                total_yielded += 1
            return
