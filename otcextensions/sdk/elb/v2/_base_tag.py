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
from openstack import exceptions
from openstack import resource
from openstack import utils


class Resource(resource.Resource):

    def _raw_delete(self, session, **kwargs):
        if not self.allow_delete:
            raise exceptions.MethodNotSupported(self, "delete")

        session = self._get_session(session)
        session.get_project_id() + self.base_path
        base_path = session.get_project_id() + self.base_path

        uri = utils.urljoin(
            base_path % self._uri.attributes,
            self._body.dirty.get('id')
        )

        microversion = self._get_microversion_for(session, 'delete')

        return session.delete(
            uri,
            microversion=microversion,
        )
