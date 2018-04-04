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
from otcextensions.sdk import sdk_proxy

from otcextensions.sdk.cce.v1 import cluster as _cluster


class Proxy(sdk_proxy.Proxy):

    def get_os_headers(self, language=None):
        """Get headers for request

        Unfortunatels RDS requires 'Content-Type: application/json'
        header even for GET and LIST operations with empty body
        We need to deel with it

        :param language: whether language should be added to headers
            can be either bool (then self.get_language is used)
            or a language code directly (i.e. "en-us")
        :returns dict: dictionary with headers
        """
        headers = {
            'Content-Type': 'application/json',
        }
        if language:
            if isinstance(language, bool):
                headers['X-Language'] = self.get_language()
            elif isinstance(language, str):
                headers['X-Language'] = language
        return headers

    # ======== Cluster ========
    def clusters(self):
        """List all Clusters.



        :returns: a generator of
            (:class:`~otcextensions.sdk.cce.v1.cluster.Cluster`) instances
        """
        return self._list(
            _cluster.Cluster, paginated=True,
            headers=self.get_os_headers())

    def get_cluster(self, cluster):
        """Get the cluster by UUID

        :param cluster: key id or an instance of
            :class:`~otcextensions.sdk.cce.v1.cluster.Cluster`

        :returns: instance of
            :class:`~otcextensions.sdk.cce.v1.cluster.Cluster`
        """
        return self._get(
            _cluster.Cluster, cluster,
            headers=self.get_os_headers()
        )
