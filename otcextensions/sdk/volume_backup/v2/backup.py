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

from otcextensions.sdk import sdk_resource
from otcextensions.sdk.volume_backup import volume_backup_service


class Backup(sdk_resource.Resource):
    """Volume Backup"""
    resource_key = "backup"
    resources_key = "backups"
    base_path = "/backups"
    details_list_path = "/backups/detail"
    service = volume_backup_service.VolumeBackupService()

    _query_mapping = resource.QueryParameters(
        'all_tenants', 'name', 'status', 'project_id')

    # capabilities
    allow_create = True
    allow_delete = True
    allow_list = True
    allow_get = True

    #: Properties
    #: The volume to be backup
    volume_id = resource.Body("volume_id")
    #: The snapshot of volume which will be backup
    snapshot_id = resource.Body("snapshot_id")
    #: Indicates whether the backup mode is incremental.
    #: If this value is true, the backup mode is incremental.
    #: If this value is false, the backup mode is full.
    is_incremental = resource.Body("is_incremental", type=bool)
    #: Force backup
    force = resource.Body("force", type=bool)
    #: backup name
    name = resource.Body("name")
    #: backup description
    description = resource.Body("description")
    #: backup status
    #: values: creating, available, deleting, error, restoring, error_restoring
    status = resource.Body("status")
    #: backup availability zone
    availability_zone = resource.Body("availability_zone")
    #: backup size
    size = resource.Body("size", type=int)
    #: backup object count
    object_count = resource.Body("object_count", type=int)
    #: Backup fail reason
    fail_reason = resource.Body("fail_reason")
    #: The container backup in
    container = resource.Body("container")
    #: The container created at
    created_at = resource.Body("created_at")
    #: The container updated at
    updated_at = resource.Body("updated_at")
    #: has_dependent_backups
    #: If this value is true, there are other backups depending on this backup.
    has_dependent_backups = resource.Body('has_dependent_backups', type=bool)
    #: data timestamp
    #: The time when the data on the volume was first saved.
    #: If it is a backup from volume, it will be the same as created_at
    #: for a backup. If it is a backup from a snapshot,
    #: it will be the same as created_at for the snapshot.
    data_timestamp = resource.Body('data_timestamp')
    #: OTC extensions
    #: The tenant which backup belongs to
    tenant_id = resource.Body("os-bak-tenant-attr:tenant_id")
    #: Backup metadata
    service_metadata = resource.Body("service_metadata")

    @classmethod
    def list(cls, session, paginated=False, details=False,
             endpoint_override=None, headers=None, **params):

        if not cls.allow_list:
            raise exceptions.MethodNotSupported(cls, "list")

        session = cls._get_session(session)

        cls._query_mapping._validate(params, base_path=cls.base_path)
        query_params = cls._query_mapping._transpose(params)
        # Check, which uri should we go to
        uri = (cls.base_path if not details else cls.details_list_path) \
            % params

        limit = query_params.get('limit')

        # Build additional arguments to the GET call
        get_args = cls._prepare_override_args(
            endpoint_override=endpoint_override,
            # request_headers=request.headers,
            additional_headers=headers)

        total_yielded = 0
        while uri:
            response = session.get(
                uri,
                params=query_params.copy(),
                **get_args
            )
            exceptions.raise_from_response(response)
            data = response.json()

            # Discard any existing pagination keys
            query_params.pop('marker', None)
            query_params.pop('limit', None)

            if cls.resources_key:
                resources = data[cls.resources_key]
            else:
                resources = data

            if not isinstance(resources, list):
                resources = [resources]

            marker = None
            for raw_resource in resources:
                # Do not allow keys called "self" through. Glance chose
                # to name a key "self", so we need to pop it out because
                # we can't send it through cls.existing and into the
                # Resource initializer. "self" is already the first
                # argument and is practically a reserved word.
                raw_resource.pop("self", None)

                if cls.resource_key and cls.resource_key in raw_resource:
                    raw_resource = raw_resource[cls.resource_key]

                value = cls.existing(**raw_resource)

                marker = value.id
                yield value
                total_yielded += 1

            if resources and paginated:
                uri, next_params = cls._get_next_link(
                    uri, response, data, marker, limit, total_yielded)
                query_params.update(next_params)
            else:
                return

    def restore(self, session, volume_id):
        """Restore current backup to volume

        :param session: openstack session
        :param volume_id: the volume be restored
        :return:
        """
        url = utils.urljoin(self.base_path, self.id, "restore")
        body = {"restore": {"volume_id": volume_id}}
        response = session.post(url,
                                json=body)
        self._translate_response(response)
        return self
