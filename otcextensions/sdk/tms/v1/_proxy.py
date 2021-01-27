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
from otcextensions.sdk.tms.v1 import predefined_tag as _tag

from openstack import proxy


class Proxy(proxy.Proxy):

    skip_discovery = True

    # ======== Predefined Tag ========
    def predefined_tags(self, **query):
        """Return a generator of predefined tags

        :param dict query: Optional query parameters to be sent to limit
            the resources being returned.

        :returns: A generator of predefined tag objects.
        """
        return self._list(_tag.PredefinedTag, **query)

    def create_predefined_tags(self, action='create', **attrs):
        """Create new predefined tags from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.tms.v1.predefined_tag.PredefinedTag`,
            comprised of the properties on the PredefinedTag class.

        :returns: The results of the tags creation

        :rtype: :class:`~otcextensions.sdk.tms.v1.predefined_tag.PredefinedTag`
        """
        return self._create(_tag.PredefinedTag, **attrs)

    def delete_predefined_tags(self, action='delete', **attrs):
        """Delete predefined tags from attributes

        :param dict attrs: Keyword arguments which will be used to delete
            :class:`~otcextensions.sdk.tms.v1.predefined_tag.PredefinedTag`
            instances.

        :returns: None

        """
        return self._create(_tag.PredefinedTag, **attrs)

    def update_predefined_tags(self, **attrs):
        """Update predefined tags from attributes

        :param dict attrs: Keyword arguments which will be used to modify
            :class:`~otcextensions.sdk.tms.v1.predefined_tag.PredefinedTag`
            instances.

        :returns: None

        """
        return self._update(_tag.PredefinedTag, **attrs)
