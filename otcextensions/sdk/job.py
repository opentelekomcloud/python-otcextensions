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


class Job(resource.Resource):

    base_path = '/jobs'

    # capabilities
    allow_fetch = True

    # Properties
    #: Created (RDS)
    created = resource.Body('created')
    #: id
    id = resource.Body('job_id', alternate_id=True)
    #: Additional sub information
    entities = resource.Body('entities', type=dict)
    #: Error code
    error_code = resource.Body('error_code')
    #: Fail reason
    fail_reason = resource.Body('fail_reason')
    #: Job finish time
    finish_time = resource.Body('end_time')
    #: Job start time
    start_time = resource.Body('begin_time', alias='created')
    #: Status
    status = resource.Body('status')
    #: Job type
    #: *Type:str*
    type = resource.Body('job_type')

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

        request = self._prepare_request(requires_id=requires_id,
                                        base_path=base_path)
        if session.service_type == 'rdsv3':
            request.url = self.base_path + '?id=' + self.id
        session = self._get_session(session)
        microversion = self._get_microversion_for(session, 'fetch')
        response = session.get(request.url, microversion=microversion,
                               params=params)
        kwargs = {}
        if error_message:
            kwargs['error_message'] = error_message

        self.microversion = microversion
        self._translate_response(response, **kwargs)
        return self


class JobProxyMixin(object):

    def wait_for_job(self, job_id, status='success',
                     failures=None, interval=5, wait=3600,
                     attribute='status'):
        if self.service_type == 'rdsv3':
            status = 'completed'
            failures = ['failed']
        else:
            failures = ['FAIL'] if failures is None else failures

        job = Job.existing(id=job_id).fetch(self)
        return resource.wait_for_status(
            self, job, status, failures, interval, wait, attribute='status'
        )
