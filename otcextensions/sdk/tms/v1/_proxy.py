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
from otcextensions.sdk.tms.v1 import predefined_tag as _predefined_tag


class Proxy(proxy.Proxy):
    skip_discovery = True

    # ======== Predefined Tag ========
    def predefined_tags(self, **query):
        """Retrieve a generator of PredefinedTags

        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.
            * `key`: Tag key
            * `value`: Tag value
            * `limit`: Number of query records
            * `marker`: Paging location identifier
            * `order_field`: Field for sorting
            * `order_method`: Sorting will be asc or desc


        :returns: A generator of backup
            :class:`~otcextensions.sdk.tms.v1.predefined_tag.PredefinedTag` instances
        """
        return self._list(_predefined_tag.PredefinedTag, **query)
