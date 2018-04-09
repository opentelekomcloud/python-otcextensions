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

from otcextensions.sdk.kms.v1 import _base


class Key(_base.Resource):
    list_path = '/kms/list-keys'
    get_path = '/kms/describe-key'
    create_path = '/kms/create-key'

    resources_key = 'key_details'
    resource_key = 'key_info'

    allow_list = True
    allow_get = True
    allow_create = True

    # Properties
    #: Secret key ID
    key_id = resource.Body('key_id', alternate_id=True)
    #: User domain name
    domain_name = resource.Body('domain_name')
    #: User domain id
    domain_id = resource.Body('domain_id')
    #: Secret key alias
    key_alias = resource.Body('key_alias')
    #: Secret area
    realm = resource.Body('realm')
    #: Secret key description
    key_description = resource.Body('key_description')
    #: Secret key creation date
    creation_date = resource.Body('creation_date')
    #: Scheduled deletion time
    scheduled_deletion_date = resource.Body('scheduled_deletion_date')
    #: Key state. (2, enabled; 3, disabled; 4: sheduled deleted)
    key_state = resource.Body('key_state')
    #: Default key flag. (default 1 else 0)
    default_key_flag = resource.Body('default_key_flag')
    #: Secret key type.
    key_type = resource.Body('key_type')
    #: Error code when create a secret key
    error_code = resource.Body('error_code')
    #: Error message when create a secret key
    error_msg = resource.Body('error_msg')

    def get(self, session, error_message=None, requires_id=True,
            endpoint_override=None, headers=None):
        if not self.allow_get:
            raise exceptions.MethodNotSupported(self, "get")
        url = self.get_path
        body = {
            'key_id': self.id
        }
        session = self._get_session(session)
        response = session.post(url, json=body)
        self._translate_response(response, has_body=True)

        return self

    def enable(self, session):
        session = self._get_session(session)
        return self._action(session, 'enable-key', {'key_id': self.id})

    def disable(self, session):
        session = self._get_session(session)
        return self._action(session, 'disable-key', {'key_id': self.id})

    def schedule_deletion(self, session, pending_days=7):
        session = self._get_session(session)
        body = {
            'key_id': self.id,
            'pending_days': pending_days
        }
        return self._action(session, 'schedule-key-deletion', body)

    def cancel_deletion(self, session):
        session = self._get_session(session)
        return self._action(
            session, 'cancel-key-deletion',
            {'key_id': self.id}
        )

    @classmethod
    def list(cls, session, paginated=True,
             endpoint_override=None, headers=None, **kwargs):

        if not cls.allow_list:
            raise exceptions.MethodNotSupported(cls, "list")

        uri = None
        if not hasattr(cls, 'list_path'):
            uri = cls.base_path
        else:
            uri = cls.list_path

        body = {}
        limit = None
        if 'limit' in kwargs:
            limit = kwargs['limit']
            body['limit'] = limit
        if 'marker' in kwargs:
            body['marker'] = kwargs['marker']
        if 'key_state' in kwargs:
            body['key_state'] = kwargs['key_state']
        if 'sequence' in kwargs:
            body['sequence'] = kwargs['sequence']

        total_yielded = 0
        while uri:

            session = cls._get_session(session)

            args = cls._prepare_override_args(
                endpoint_override=endpoint_override,
                additional_headers=headers)

            response = session.post(uri, json=body, **args)

            data = response.json()

            if cls.resources_key:
                resources = data[cls.resources_key]
            else:
                resources = data

            if not isinstance(resources, list):
                resources = [resources]

            marker = None
            for raw_resource in resources:
                raw_resource.pop("self", None)

                if cls.resource_key and cls.resource_key in raw_resource:
                    raw_resource = raw_resource[cls.resource_key]

                value = cls.existing(**raw_resource)

                marker = value.id
                yield value
                total_yielded += 1

            if resources and paginated:
                uri, next_params = cls._get_next_link(
                    uri, response, data, marker, limit, total_yielded)
                body.update(next_params)
            else:
                return

    @classmethod
    def _get_next_link(cls, uri, response, data, marker, limit, total_yielded):
        # service pagination. Returns query for the next page
        next_link = None
        params = {}
        truncated = data.get('truncated', None)
        if truncated:
            next_marker = data.get('next_marker', None)
            if next_marker:
                next_link = uri
                params['marker'] = next_marker
        else:
            next_link = None
        return next_link, params

    @classmethod
    def _get_one_match(cls, search_filter, results):
        """Given a list of results, return the match"""
        the_result = None
        for maybe_result in results:
            id_value = cls._get_id(maybe_result)
            name_value = maybe_result.name
            alias_value = maybe_result.key_alias

            if (id_value == search_filter) or (name_value == search_filter) \
                    or (alias_value == search_filter):
                # Only allow one resource to be found. If we already
                # found a match, raise an exception to show it.
                if the_result is None:
                    the_result = maybe_result
                else:
                    msg = "More than one %s exists with the name '%s'."
                    msg = (msg % (cls.__name__, search_filter))
                    raise exceptions.DuplicateResource(msg)

        return the_result
