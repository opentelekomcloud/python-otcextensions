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

from openstack import resource


class ImageExport(resource.Resource):
    base_path = '/cloudimages/%(image_id)s/file'

    allow_create = True
    requires_id = False

    image_id = resource.URI('image_id')
    bucket_url = resource.Body('bucket_url')
    file_format = resource.Body('file_format')
    is_quick_export = resource.Body('is_quick_export', type=bool)
    job_id = resource.Body('job_id')

    def create(self, session, prepend_key=False, base_path=None):
        # Overriden here to override prepend_key default value
        return super(ImageExport, self).create(session, prepend_key, base_path)
