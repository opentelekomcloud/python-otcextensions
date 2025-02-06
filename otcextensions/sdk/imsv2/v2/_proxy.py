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
from otcextensions.sdk.imsv2.v2 import image as _image


class Proxy(proxy.Proxy):
    skip_discovery = True

    def create_image(self, **attrs):
        """Create a new image with attrs

        :param dict attrs: Keyword arguments which will be used to create a
            :class:`~otcextensions.sdk.imsv2.v2.image.Image`
        """
        return self._create(_image.Image, **attrs)

    def images(self, **query):
        """Retrieve a generator of images

        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.

        :returns: A generator of zone
            :class:`~otcextensions.sdk.imsv2.v2.image.Image` instances
        """
        return self._list(_image.Image, **query)
