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
from openstack import _log
from openstack import exceptions
from openstack import resource
from openstack import utils

from otcextensions.i18n import _

_logger = _log.setup_logging('openstack')


class Resource(resource.Resource):
    base_path = '/kms'

    #: Error code when create a secret key
    error_code = resource.Body('error_code')
    #: Error message when create a secret key
    error_msg = resource.Body('error_msg')

    def create(self, session, prepend_key=False, uri=None,
               requires_id=True, **params):
        if not self.allow_create:
            raise exceptions.MethodNotSupported(self, "create")

        session = self._get_session(session)

        request = self._prepare_request(requires_id=False,
                                        prepend_key=prepend_key
                                        )
        # PATH is different
        if uri:
            request.url = uri
        elif self.create_path:
            request.url = self.create_path

        response = session.post(request.url,
                                json=request.body, headers=request.headers,
                                params=params)

        if response.status_code == 400:
            body = response.json()
            error = body.get('error', None)
            if error:
                if error['error_code'] == 'KMS.1104':
                    msg = (_('Key with given alias %s already exist')
                           % self.key_alias)
                    raise exceptions.DuplicateResource(msg)
                else:
                    msg = (_('Service returned an error with code=%s')
                           % error['error_code'])
                    raise exceptions.SDKException(msg)

        self._translate_response(response)

        return self

    def _action(self, session, url_part, body):
        """Perform actions given the message body.
        """
        url = utils.urljoin(self.base_path, url_part)
        response = session.post(
            url,
            json=body)
        self._translate_response(response)
        return self

    def _translate_response(
            self, response, has_body=None, error_message=None,
            resource_response_key=None
    ):
        """Given a KSA response, inflate this instance with its data

        'DELETE' operations don't return a body, so only try to work
        with a body when has_body is True.

        This method updates attributes that correspond to headers
        and body on this instance and clears the dirty set.
        """
        if has_body is None:
            has_body = self.has_body
        if response.status_code == 400 and not error_message:
            if has_body:
                body = response.json()
                error = body.get('error', None)
                if error:
                    error_code = error.get('error_code', None)
                    if error_code == 'KMS.0205':
                        raise exceptions.NotFoundException
                    else:
                        msg = (_('Service returned an error with code = %s')
                               % error_code)
                        raise exceptions.SDKException(msg)
        return super(Resource, self)._translate_response(
            response, has_body, error_message)
