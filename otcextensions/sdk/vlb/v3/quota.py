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


class Quota(resource.Resource):
    base_path = '/elb/quotas'

    # capabilities
    allow_fetch = True

    # Properties
    #: Specifies the certificate quota.
    certificate = resource.Body('certificate', type=int)
    #: Specifies the health check quota.
    healthmonitor = resource.Body('healthmonitor', type=int)
    #: Specifies the IP address group quota.
    ipgroup = resource.Body('ipgroup', type=int)
    #: Specifies the forwarding policy quota.
    l7policy = resource.Body('l7policy', type=int)
    #: Specifies the listener quota.
    listener = resource.Body('listener', type=int)
    #: Specifies the loadbalancer quota.
    loadbalancer = resource.Body('loadbalancer', type=int)
    #: Specifies the backend server quota.
    member = resource.Body('member', type=int)
    #: Specifies the quota of backend servers in a backend server group.
    members_per_pool = resource.Body('members_per_pool', type=int)
    #: Specifies the backend server group quota.
    pool = resource.Body('pool', type=int)
    #: Specifies the IP address group quota.
    project_id = resource.Body('project_id', type=str)

    @classmethod
    def get(cls, session):
        session = cls._get_session(session)
        url = cls.base_path
        response = session.get(url)
        resp = response.json()
        if 'error' in resp:
            return
        value = cls.existing(
            connection=session._get_connection(),
            **resp['quota'])
        return value
