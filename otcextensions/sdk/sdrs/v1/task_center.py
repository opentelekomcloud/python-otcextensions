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


class FailedTask(resource.Resource):
    """SDRS Failed task Resource"""
    resource_key = ''
    resources_key = 'failure_jobs'
    base_path = '/task-center/failure-jobs'

    # capabilities
    allow_create = False
    allow_list = True
    allow_fetch = False
    allow_delete = True

    _query_mapping = resource.QueryParameters(
        'failure_status', 'limit', 'marker', 'offset',
        'resource_name', 'resource_type', 'server_group_id')

    #: Properties
    #: Task operation time
    begin_time = resource.Body('begin_time')
    #: Failed task error code
    error_code = resource.Body('error_code')
    #: Failed task cause
    fail_reason = resource.Body('fail_reason')
    #: Failed task status
    failure_status = resource.Body('failure_status')
    #: Task ID
    job_id = resource.Body('job_id')
    #: Task name
    job_type = resource.Body('job_type')
    #: Task status
    #: Only 'fail' status available in current
    #: version
    job_status = resource.Body('job_status')
    #: Resource ID
    resource_id = resource.Body('resource_id')
    #: Resource name
    resource_name = resource.Body('resource_name')
    #: Resource type
    resource_type = resource.Body('resource_type')

    @classmethod
    def delete_all_tasks(cls, session, endpoint):
        """Method to delete all tasks of all protection groups

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param endpoint: SDRS service endpoint
        """
        url = utils.urljoin(endpoint, cls.base_path,
                            '/batch')
        return session.delete(url)

    @classmethod
    def delete_protection_tasks(cls, session,
                                endpoint, protection_group):
        """Method to delete all tasks of a signle protection group

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param endpoint: SDRS service endpoint
        :param protection_group: Protection group ID
        """
        url = utils.urljoin(endpoint, '/task-center', protection_group,
                            '/failure-jobs/batch')
        return session.delete(url)
