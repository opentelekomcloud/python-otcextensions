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
from otcextensions.sdk.imsv1.v1 import async_job as _async_job
from otcextensions.sdk.imsv1.v1 import image_export as _image_export


class Proxy(proxy.Proxy):
    skip_discovery = True

    def get_async_job(self, job_id):
        """Get an asynchronous job

        :returns: One
             :class:`~otcextensions.sdk.imsv2.v1.async_job.AsyncJob`
        """
        attrs = {
            'id': job_id
        }
        base_path = '{project_id}/jobs'.format(
            project_id=self.session.get_project_id()
        )
        return self._get(_async_job.AsyncJob, base_path=base_path, **attrs)

    def export_image(self, **attrs):
        """Export an image

        :returns: One
             :class:`~otcextensions.sdk.imsv1.v1.image_export.ImageExport`
        """
        return self._create(_image_export.ImageExport, **attrs)
