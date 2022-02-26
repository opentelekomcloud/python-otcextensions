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
from openstack import proxy

from otcextensions.sdk.sdrs.v1 import job as _job
from otcextensions.sdk.sdrs.v1 import active_domains as _active_domains

class Proxy(proxy.Proxy):

    skip_discovery = True

    # ======== Job ========
    def get_job(self, job):
        """ Get single SDRS job by UUID.

        :param job: The id or and instance of
            :class:'~otcextensions.sdk.sdrs.v1.job.Job'

        :returns: instance of
            :class: '~class:'otcextensions.sdk.sdrs.v1.job.Job'
        """
        return self._get(_job.Job, job)

    # ======== Active-active domain ========
    def get_domains(self):
        """Retrieve a generator of Active-active domains

        :returns: A generator of active-active domains
            :class: '~otcextensions.sdk.sdrs.v1.active_domains.ActiveDomain'
        """
        return self._list(_active_domains.ActiveDomain)
