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
from openstack import exceptions
from openstack import resource
from openstack import utils

from otcextensions.sdk.rds.v3 import _base


class Backup(_base.Resource):

    base_path = '/backups'
    resources_key = 'backups'
    resource_key = 'backup'

    # capabilities
    allow_create = True
    allow_delete = True
    allow_list = True
    allow_fetch = True

    _query_mapping = resource.QueryParameters(
        'offset', 'begin_time', 'instance_id', 'id',
        'type', 'begin_time', 'end_time', 'offset', 'limit',
        id='backup_id', type='backup_type')

    #: Backup id
    #: Type: uuid*
    id = resource.Body('id')
    #: Begin time
    begin_time = resource.Body('begin_time')
    #: Create back of specific dbs
    #: *Type:list*
    databases = resource.Body('databases', type=list)
    #: Datastore
    #: *Type:dict*
    datastore = resource.Body('datastore', type=dict)
    #: Data backup description
    description = resource.Body('description')
    #: Instance id
    instance_id = resource.Body('instance_id')
    #: Back file size in GB
    #: *Type:int*
    size = resource.Body('size', type=int)
    #: Backup status
    status = resource.Body('status')
    #: Finished time
    end_time = resource.Body('end_time')
    #: Backup type
    #:  `auto`: automated full backup
    #:  `manual`: manual full backup
    #:  `fragment`: differential full backup
    #:  `incremental`: automated incremental backup
    type = resource.Body('type')

    def create(self, session, prepend_key=False, base_path=None):
        return super(Backup, self).create(session,
                                          prepend_key=prepend_key,
                                          base_path=base_path)

    def commit(self, session, prepend_key=False, **further_attrs):
        return super(Backup, self).commit(
            session,
            prepend_key=prepend_key,
            **further_attrs)

    def fetch(self, session, requires_id=True,
              base_path=None, error_message=None, **params):
        """Get a remote resource based on this instance.

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param boolean requires_id: A boolean indicating whether resource ID
                                    should be part of the requested URI.
        :param str base_path: Base part of the URI for fetching resources, if
                              different from
                              :data:`~openstack.resource.Resource.base_path`.
        :param str error_message: An Error message to be returned if
                                  requested object does not exist.
        :param dict params: Additional parameters that can be consumed.
        :return: This :class:`Resource` instance.
        :raises: :exc:`~openstack.exceptions.MethodNotSupported` if
                 :data:`Resource.allow_fetch` is not set to ``True``.
        :raises: :exc:`~openstack.exceptions.ResourceNotFound` if
                 the resource was not found.
        """
        if not self.allow_fetch:
            raise exceptions.MethodNotSupported(self, "fetch")
            
        # Create request parameters
        request_params = {
            'instance_id': self.instance_id,
            'backup_id': self.id
        }
        
        # Merge with additional params if provided
        request_params.update(params)

        query_params = self._query_mapping._transpose(request_params, self)
        url = utils.urljoin(self.base_path) % request_params

        session = self._get_session(session)
        microversion = self._get_microversion(session, action='fetch')
        response = session.get(
            url, microversion=microversion,
            headers={"Accept": "application/json"},
            params=query_params.copy())

        exceptions.raise_from_response(response)

        try:
            body = response.json()
            if self.resources_key in body:
                body = body[self.resources_key]

            if not len(body) == 1:
                raise exceptions.SDKException('Not a single result returned')

            body = body[0]
            body_attrs = self._consume_body_attrs(body)
            self._body.attributes.update(body_attrs)
            self._body.clean()

        except ValueError:
            # Server returned not parse-able response (202, 204, etc)
            # Do simply nothing
            pass

        dict.update(self, self.to_dict())

        return self


class BackupFile(resource.Resource):

    base_path = '/backup-files'
    resources_key = 'files'

    # capabilities
    allow_list = True

    _query_mapping = resource.QueryParameters('backup_id')

    #:  Indicates the file name
    #:  *Type: string*
    name = resource.Body('name')
    #:  Indicates the file size in KB.
    #:  *Type: long*
    size = resource.Body('size', type=int)
    #:  Indicates the link for downloading the backup file.
    #:  *Type: string*
    download_link = resource.Body('download_link')
    #:  Indicates the link expiration time.
    #:  The format is "yyyy-mmddThh:mm:ssZ".
    #:  *Type: string*
    expires_at = resource.Body('link_expired_time')
