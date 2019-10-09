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


class Backup(resource.Resource):

    base_path = '/backups'
    resources_key = 'backups'

    # capabilities
    allow_create = True
    allow_delete = True
    allow_list = True
    allow_fetch = False

    _query_mapping = resource.QueryParameters(
        'offset', 'begin_time', 'instance_id', 'id',
        'type', 'begin_time', 'end_time',
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

    @classmethod
    def find(cls, session, name_or_id, ignore_missing=True, **params):
        """Find a resource by its name or id.

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param name_or_id: This resource's identifier, if needed by
                           the request. The default is ``None``.
        :param bool ignore_missing: When set to ``False``
                    :class:`~openstack.exceptions.ResourceNotFound` will be
                    raised when the resource does not exist.
                    When set to ``True``, None will be returned when
                    attempting to find a nonexistent resource.
        :param dict params: Any additional parameters to be passed into
                            underlying methods, such as to
                            :meth:`~openstack.resource.Resource.existing`
                            in order to pass on URI parameters.

        :return: The :class:`Resource` object matching the given name or id
                 or None if nothing matches.
        :raises: :class:`openstack.exceptions.DuplicateResource` if more
                 than one resource is found for this request.
        :raises: :class:`openstack.exceptions.ResourceNotFound` if nothing
                 is found and ignore_missing is ``False``.
        """
        session = cls._get_session(session)
        # Try to short-circuit by looking directly for a matching ID.
        try:
            match = cls.existing(
                id=name_or_id,
                connection=session._get_connection(),
                **params)
            return match.fetch(session, **params)
        except exceptions.SDKException:
            pass

        data = cls.list(session, **params)

        result = cls._get_one_match(name_or_id, data)
        if result is not None:
            return result

        if ignore_missing:
            return None
        raise exceptions.ResourceNotFound(
            "No %s found for %s" % (cls.__name__, name_or_id))


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
