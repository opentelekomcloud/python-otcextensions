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

from openstack.tests.unit import base

from otcextensions.sdk.imsv2.v2 import image

EXAMPLE = {
    "name": "ims_test_file",
    "description": "Create an image from a file in an OBS bucket",
    "image_url": "imsv2-image:centos70.qcow2",
    "os_version": "CentOS 7.0 64bit",
    "min_disk": 40,
    "image_tags": [{"key": "key2", "value": "value2"},
                   {"key": "key1", "value": "value1"}]
}


class TestImage(base.TestCase):

    def test_basic(self):
        sot = image.Image()
        path = '/cloudimages'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_create)

    def test_make_it(self):
        sot = image.Image(**EXAMPLE)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['description'], sot.description)
        self.assertEqual(EXAMPLE['image_url'], sot.image_url)
        self.assertEqual(EXAMPLE['os_version'], sot.os_version)
        self.assertEqual(EXAMPLE['min_disk'], sot.min_disk)
        self.assertEqual(EXAMPLE['image_tags'], sot.image_tags)
