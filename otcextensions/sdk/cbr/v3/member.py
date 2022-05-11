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
from openstack import resource, exceptions


class Member(resource.Resource):
    """CBR Member Resource"""
    resource_key = 'member'
    resources_key = 'members'
    base_path = '/backups/%(backup_id)s/members'

    # capabilities
    allow_create = True
    allow_list = True
    allow_fetch = True
    allow_delete = True
    allow_commit = True

    _query_mapping = resource.QueryParameters(
        'created_at', 'dest_project_id', 'id', 'image_id',
        'status', 'updated_at', 'vault_id')

    #: Properties
    #: Backup ID
    backup_id = resource.URI('backup_id')
    #: Backup sharing time
    #: Example: 2020-02-05T10:38:34.209782
    created_at = resource.Body('created_at')
    #: Destination project ID which the backup is shared
    dest_project_id = resource.Body('dest_project_id')
    #: ID of the image created by using the accepted shared backup_id
    image_id = resource.Body('image_id')
    #: Backup sharing values
    #: values: pending, accepted, rejected
    status = resource.Body('status')
    #: Update time
    #: Example: 2020-02-05T10:38:34.209782
    updated_at = resource.Body('updated_at')
    #: ID of the vault where the shared backup is stored
    vault_id = resource.Body('vault_id')

    #: Updating the resource does not allow the resource key
    def commit(
        self, session, prepend_key=False, has_body=True,
            retry_on_conflict=None, base_path=None, **kwargs):
        return super(Member, self).commit(
            session,
            prepend_key=prepend_key,
            has_body=has_body,
            retry_on_conflict=retry_on_conflict,
            base_path=base_path,
            **kwargs)

    def add_members(self, session, backup_id, members):
        """Method to add several share members to a backup

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param list members: List of target project IDs to which the backup
            is shared
        """
        url = self.base_path % backup_id
        body = {
            'members': members
        }
        response = session.post(url, json=body)
