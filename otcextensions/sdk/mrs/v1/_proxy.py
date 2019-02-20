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
from otcextensions.sdk.mrs.v1 import cluster as _cluster


class Proxy(sdk_proxy.Proxy):

    skip_discovery = True

    # ======== clusters ========
    def clusters(self, **query):
        """Retrieve a generator of hosts

        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.

            * `marker`:  pagination marker
            * `limit`: pagination limit
            * `id`: Specifies MRS ID.
            * `name`: Specifies the MRS name.
            * `cluster_type`: Specifes the DeH type.
            * `host_type_name`: Specifes the DeH name of type.
            * `flavor`: Specifies flavor ID of master.
            * `status`: Specifies the MRS status.
                The value can be TERMINATED, fault or AVALIABLE.
            * `availability_host`:  Specifies the AZ to which the DeH belongs.
            * `changes_since`: Filters the response by a date and time
                stamp when the DeH last changed status
                (CCYY-MM-DDThh:mm:ss+hh:mm)

        :returns: A generator of host
            :class:`~otcextensions.sdk.mrs.v1.cluster.Cluster` instances
        """
        return self._list(_cluster.Cluster, paginated=True, **query)

