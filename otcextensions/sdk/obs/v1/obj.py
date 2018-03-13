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

from openstack import _log
from openstack import exceptions
from openstack import resource

from openstack.object_store.v1 import obj

from otcextensions.sdk.obs.v1 import _base

from otcextensions.i18n import _

from botocore.exceptions import ClientError

_logger = _log.setup_logging('openstack')


class Object(obj.Object, _base.BaseResource):
    # It should be redefined here again
    #: The unique name for the object.
    name = resource.Body("name", alternate_id=True)

    _query_mapping = resource.QueryParameters(
        'container', 'prefix', 'delimiter', 'id', 'data', 'name',
        container='Bucket',
        prefix='Prefix',
        delimiter='Delimiter',
        id='Key',
        data='Fileobj',
        name='Key'
    )

    resources_key = 'Contents'

    def download(self, session, filename=None):
        _logger.debug('download object into %s' % filename)

        request = self._prepare_request()
        session = self._get_boto_session(session)

        f = open(filename, 'wb')
        request.body['Fileobj'] = f

        response = None
        try:
            response = session.download_fileobj(**request.body)
        except ClientError as e:
            raise exceptions.SDKException(_(str(e)))

        # _logger.debug('response=%s' % response)
        # kwargs = {}
        # if error_message:
        #     kwargs['error_message'] = error_message
        #
        # self._translate_response(response, **kwargs)
        return
        pass

    @classmethod
    def new(cls, **kwargs):
        # Object uses name as id. Proxy._get_resource calls
        # Resource.new(id=name) but then we need to do container.name
        # It's the same thing for Container - make it be the same.
        obj = kwargs.pop('object', None)
        name = kwargs.pop('name', None)
        if not name and obj:
            kwargs['name'] = obj
        else:
            kwargs['name'] = name
        if obj:
            # Only in the create object the data is passed
            kwargs['data'] = open(obj, 'rb')

        return Object(_synchronized=True, **kwargs)

    @classmethod
    def _normalize_obs_keys(cls, entity):
        resource = {}

        resource['last-modified'] = \
            entity.get('LastModified', None)

        name = entity.get('Key', None)
        if name:
            resource['name'] = name

        resource['content-type'] = \
            entity.get('ContentType', None)

        size = entity.get('ContentLength', None)
        if not size:
            # in list mode
            size = entity.get('Size', None)
        if size:
            resource['content-length'] = size

        etag = entity.get('ETag', None)
        if not etag:
            etag = entity.get('etag', None)
        resource['etag'] = etag

        resource['accept-ranges'] = entity.get('AcceptRanges', None)

        _logger.debug('mapped resources = %s' % resource)

        return resource

    def _translate_response(self, response, has_body=True, error_message=None):
        """Given a KSA response, inflate this instance with its data

        This method updates attributes that correspond to headers
        and body on this instance and clears the dirty set.
        """
        if response:
            # if has_body:

            resource = self._normalize_obs_keys(response)
            resource['name'] = self.id

            self._update(**resource)

    def _prepare_request(self, requires_id=None, prepend_key=False):
        """Prepare a request to be sent to the server

        Create operations don't require an ID, but all others do,
        so only try to append an ID when it's needed with
        requires_id. Create and update operations sometimes require
        their bodies to be contained within an dict -- if the
        instance contains a resource_key and prepend_key=True,
        the body will be wrapped in a dict with that key.

        Return a _Request object that contains the constructed URI
        as well a body and headers that are ready to send.
        Only dirty body and header contents will be returned.
        """
        if requires_id is None:
            requires_id = self.requires_id

        _logger.debug('self=%s' % self)
        params = {
            'id': self.id,
            'container': self.container,
        }
        if self.data and prepend_key:
            params['data'] = self.data

        self._query_mapping._validate(params, base_path=self.base_path)
        query_params = self._query_mapping._transpose(params)
        _logger.debug('params=%s' % query_params)

        body = query_params.copy()

        return resource._Request(None, body, None)

    @classmethod
    def list(cls, session, paginated=False, **params):
        """Override default list to incorporate endpoint overriding
        and custom headers

        Since SDK Resource.list method is passing hardcoded headers
        do override the function

        This resource object list generator handles pagination and takes query
        params for response filtering.

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
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
        return super(Object, cls).list(
            session, 'list_objects_v2', '_normalize_obs_keys',
            paginated, **params
        )

    def get(self, session, error_message=None, requires_id=True):
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
        return super(Object, self).get(
            session, 'head_object', error_message, requires_id
        )

    def create(self, session, prepend_key=True):
        super(Object, self)._create(
            session, 'upload_fileobj', prepend_key
        )
        # refetch the object, since boto does not return
        # any useful data upon create
        return self.get(session)

    def delete(self, session, error_message=None):
        """Delete the remote resource based on this instance.

        This function overrides default Resource.delete to enable headers

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`

        :return: This :class:`Resource` instance.
        :raises: :exc:`~openstack.exceptions.MethodNotSupported` if
                 :data:`Resource.allow_update` is not set to ``True``.
        """
        return super(Object, self).delete(
            session, 'delete_object', error_message
        )
