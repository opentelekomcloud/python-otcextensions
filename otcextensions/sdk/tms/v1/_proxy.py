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
from otcextensions.sdk.tms.v1 import tag as _tag

from openstack import proxy


class Proxy(proxy.Proxy):

    def create_predefine_tags(self,  **attrs):
        """Create new predefine tags
        :param
        :return
        """
        tag = self._get_resource(_tag.Tag, **attrs)
        return tag.create_tag(self)

    def delete_predefine_tags(self, ignore_missing=True, **attrs):
        """Delete tags
        :param DeletePredefineTagsRequest
        :return: DeletePredefineTagsResponse
        """
        tag = self._get_resource(_tag.Tag, ignore_missing, **attrs)
        return tag.delete_tag(self)

    def query_predefine_tag(self, **attrs):
        """Query tags by attributes
        :param
        :return
        """
        return self._list(_tag.Tag, **attrs)

    def get_predefine_tag(self, tag):
        """Get a tag
        :param
        :return
        """
        return self._get(_tag.Tag, tag)

    def modify_predefine_tag(self, **attrs):
        """Modify a tag
        :param
        :return
        """
        return self._update(_tag.Tag, **attrs)
