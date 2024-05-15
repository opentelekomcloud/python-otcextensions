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
from otcextensions.sdk.tms.v1 import resource_tag as _resource_tag
from urllib.parse import urlparse


class Proxy(proxy.Proxy):
    skip_discovery = True

    def _get_endpoint_with_api_version(self, api_version):
        url_parts = urlparse(self.get_endpoint())
        alternate_endpoint = '{scheme}://{netloc}/{api_version}'.format(
            scheme=url_parts.scheme,
            netloc=url_parts.netloc,
            api_version=api_version
        )
        return alternate_endpoint

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
            :class:`~otcextensions.sdk.tms.v1.predefined_tag.PredefinedTag`
            instances
        """
        return self._list(_predefined_tag.PredefinedTag, **query)

    def create_predefined_tag(self, **attrs):
        """Create a new predefined tag with attrs

        :param dict attrs: Keyword arguments which will be used to create a
            :class:`~otcextensions.sdk.tms.v1.predefined_tag.PredefinedTag`
        """
        tag = _predefined_tag.PredefinedTag()
        return tag.add_tag(self, **attrs)

    def delete_predefined_tag(self, **attrs):
        """Delete a new predefined tag with attrs

        :param dict attrs: Keyword arguments which will be used to delete a
            :class:`~otcextensions.sdk.tms.v1.predefined_tag.PredefinedTag`
        """
        tag = _predefined_tag.PredefinedTag()
        return tag.delete_tag(self, **attrs)

    def update_predefined_tag(self, **attrs):
        """Update a predefined tag

        :param dict attrs: The attributes to update on the predefined tag

        :returns: The updated tag.

        :rtype: :class:`~otcextensions.sdk.tms.v1.predefined_tag.PredefinedTag`
        """
        return self._update(_predefined_tag.PredefinedTag,
                            **attrs)

    # ======== Resource Tag ========
    def resource_tags(self, resource_id, resource_type, project_id=None):
        """Retrieve a generator of ResourceTags
        'project_id', 'resource_id', 'resource_type'
                :param project_id: Optional ID of the project
                :param resource_type: Mandatory type of the resource
                :param resource_id: Mandatory id of the resource

                :returns: A generator of backup
                    :class:`~otcextensions.sdk.tms.v1.resource_tag.ResourceTag`
                    instances
        """
        base = self._get_endpoint_with_api_version('v2.0')
        base_path = (f"{base}/resources/{resource_id}/tags?project_id="
                     f"{project_id}&resource_type={resource_type}")
        return self._list(_resource_tag.ResourceTag, base_path=base_path)

    def create_resource_tag(self, **attrs):
        """Create a new resource tag with attrs

        :param dict attrs: Keyword arguments which will be used to create a
            :class:`~otcextensions.sdk.tms.v1.predefined_tag.PredefinedTag`
        """
        return self._create(_resource_tag.ResourceTag, **attrs)

    def delete_resource_tag(self, **attrs):
        """Delete a new resource tag with attrs

        :param dict attrs: Keyword arguments which will be used to delete a
            :class:`~otcextensions.sdk.tms.v1.predefined_tag.PredefinedTag`
        """
        return self._delete(_resource_tag.ResourceTag, **attrs)
