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

    def images(self, **attrs):
        """Retrieve a generator of images

        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.

        :returns: A generator of zone
            :class:`~otcextensions.sdk.imsv2.v2.image.Image` instances
        """
        return self._list(_image.Image, paginated=False, **attrs)
    
    def update_image(self, image_id, **attrs):
        """Update an image

        :param image: The value can be either the ID of a image or a
            :class:`~otcextensions.sdk.imsv2.v2.image.Image` instance.
        :param dict attrs: The attributes to update of the image represented
            by ``image``.

        :returns: The updated image.

        :rtype: :class:`~otcextensions.sdk.imsv2.v2.image.Image`
        """
        image = _image.Image()
        return image.update_image_details(self, image_id=image_id, **attrs)

    def delete_image(self, image, ignore_missing=True):
        """Delete a gateway

        :param image: The value can be either the ID of a image or a
            :class:`~otcextensions.sdk.imsv2.v2.image.Image` instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the image does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent image.

        :returns: ``None``
        """
        return self._delete(_image.Image, image,
                            ignore_missing=ignore_missing)
