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
from openstack import resource
from openstack import utils


class SchedulePolicy(resource.Resource):
    #: whether keep the first backup of current month
    remain_first_backup_of_curMonth = resource.Body(
        "remain_first_backup_of_curMonth")
    #: the max backup amount, min value is 2
    rentention_num = resource.Body("rentention_num", type=int)
    #: backup period, valid values, 1..14 (days)
    frequency = resource.Body("frequency", type=int)
    #: backup start time of every day, example: 12:00
    start_time = resource.Body("start_time")
    #: backup policy status, ``ON``, ``OFF``
    status = resource.Body("status")


class BackupPolicy(resource.Resource):
    """Volume BackupPolicy"""
    resources_key = "backup_policies"
    base_path = "/backuppolicy"

    # capabilities
    allow_create = True
    allow_delete = True
    allow_list = True
    allow_commit = True

    #: Properties
    #: Backup Policy id
    id = resource.Body("backup_policy_id", alternate_id=True)
    #: Backup Policy name
    name = resource.Body("backup_policy_name")
    #: Backup Policy resource count
    policy_resource_count = resource.Body("policy_resource_count")
    #: Backup Policy schedule detail
    scheduled_policy = resource.Body("scheduled_policy", type=SchedulePolicy)
    #: tags
    tags = resource.Body("tags", type=list)

    def execute(self, session):
        """execute backup policy immediately

        :param session: openstack session
        :return: request response
        """
        url = utils.urljoin(self.base_path, self.id, "action")
        return session.post(url, json=None)


class BackupPolicyAssociatedResource(resource.Resource):
    #: Properties
    resource_id = resource.Body("resource_id")
    resource_type = resource.Body("resource_type")
    availability_zone = resource.Body("availability_zone")
    os_vol_host_attr = resource.Body("os_vol_host_attr")
    message = resource.Body("message")
    code = resource.Body("code")


class BackupPolicyResource(resource.Resource):
    base_path = "/backuppolicyresources"

    # capabilities
    allow_create = True

    #: Properties
    # backup_policy_id = resource.Body('backup_policy_id')
    resources = resource.Body(
        'resources', type=list, list_type=BackupPolicyAssociatedResource)
    fail_resources = resource.Body(
        "fail_resources",
        type=list, list_type=BackupPolicyAssociatedResource)
    success_resources = resource.Body(
        "success_resources",
        type=list, list_type=BackupPolicyAssociatedResource)

    def _process(self, session, backup_policy_id, link=True, resources=[]):
        """Link or unlink resources to/from BackupPolicy
        """
        _resources = [dict(resource_id=volume_id, resource_type="volume")
                      for volume_id in resources]
        body = {
            "resources": _resources
        }
        if link:
            body['backup_policy_id'] = backup_policy_id
            uri = self.base_path
        else:
            uri = utils.urljoin(
                self.base_path, backup_policy_id, "deleted_resources")

        response = session.post(uri, json=body)

        fail_resources = []
        success_resources = []

        response_json = response.json()
        for type in ['success_resources', 'fail_resources']:
            if type in response_json:
                for res in response_json[type]:
                    assocResource = \
                        BackupPolicyAssociatedResource.existing(**res)
                    if assocResource.code:
                        fail_resources.append(assocResource)
                    else:
                        success_resources.append(assocResource)
        self._update(
            success_resources=success_resources,
            fail_resources=fail_resources
        )

        return self

    def link(self, session, backup_policy_id, resources):
        """link resources to backup policy

        :param session: openstack session
        :param backup_policy_id: backup policy id
        :param resources: resources to bound, should be a list of volume id
        :return:
        """
        return self._process(session, backup_policy_id, True, resources)

    def unlink(self, session, backup_policy_id, resources):
        """unlink resources from backup policy

        :param session: openstack session
        :param backup_policy_id: backup policy id
        :param resources: resources to unbound, should be a list of volume id
        :return:
        """
        return self._process(session, backup_policy_id, False, resources)
