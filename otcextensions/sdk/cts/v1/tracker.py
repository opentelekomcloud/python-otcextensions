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

from otcextensions.common import exc


class Smn(resource.Resource):
    #: Specifies whether SMN is supported.
    enabled = resource.Body('is_support_smn', type=bool)
    #: Specifies the theme of the SMN service.
    topic_id = resource.Body('topic_id')
    #: * Specifies trigger conditions for sending a notification when `Typical`
    #: is selected. You can select Delete, Create, or Login or at least one
    #: of them.
    #: * Specifies trigger conditions for sending a notification when `All`
    #: is selected. All conditions including Delete, Create, Change, and
    #: OpenStack API Event are selected by default. Modification is not
    #: allowed.
    operations = resource.Body('operations', type=list)
    #: You can select Typical or All for Trigger Condition.
    #: * When the value is `false`, operations cannot be left empty.
    #: * When the value is `true`, operations is not supported.
    is_send_all_key_operation = resource.Body(
        'is_send_all_key_operation', type=bool)
    #: In Typical scenario, you can specify the users using the login function.
    #: When these users log in, notifications will be sent.
    #: * After this function is enabled, the value is the list of the
    #: specified users. Separate them with commas (,). A maximum of 50
    #: users is supported.
    #: * If the value is null, the target objects are all users under the
    #: current tenant by default.
    notify_users = resource.Body('need_notify_user_list', type=list)


class Tracker(resource.Resource):

    base_path = '/tracker'

    _query_mapping = resource.QueryParameters('tracker_name')

    # capabilities
    allow_create = True
    allow_commit = True
    allow_fetch = True
    allow_delete = True

    # Properties
    #: tracker name
    name = resource.Body('tracker_name', alternate_id=True)
    #: bucket name
    bucket_name = resource.Body('bucket_name')
    #: file prefix name in a bucket
    file_prefix_name = resource.Body('file_prefix_name')
    #: Status of the tracker
    #: values: `enabled`, `disabled`, `error`
    status = resource.Body('status')
    #: Detail of the tracker, only validate if exception happens
    detail = resource.Body('detail')
    #: SMN
    smn = resource.Body('smn', type=Smn)

    def _translate_response(self, response, has_body=None, error_message=None):
        """Given a KSA response, inflate this instance with its data

        'DELETE' operations don't return a body, so only try to work
        with a body when has_body is True.

        This method updates attributes that correspond to headers
        and body on this instance and clears the dirty set.
        """
        if has_body is None:
            has_body = self.has_body
        exc.raise_from_response(response, error_message=error_message)
        if has_body:
            if response.status_code == 204:
                # Some bad APIs (i.e. DCS.Backup.List) return emptiness
                self.log.warn('API returned no content, while it was expected')
                return
            # NOTE: in difference to doc "GET" method return list with 1 item
            body = response.json()
            if isinstance(body, list):
                body = body[0]
            if self.resource_key and self.resource_key in body:
                body = body[self.resource_key]

            body = self._consume_body_attrs(body)
            self._body.attributes.update(body)
            self._body.clean()

        headers = self._consume_header_attrs(response.headers)
        self._header.attributes.update(headers)
        self._header.clean()
