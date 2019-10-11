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

from otcextensions.sdk.rds.v3 import _base


class Configuration(_base.Resource):

    base_path = '/configurations'
    resources_key = 'configurations'
    resource_key = 'configuration'

    # capabilities
    allow_create = True
    allow_delete = True
    allow_commit = True
    allow_fetch = True
    allow_list = True

    #: Id of the configuration group
    configuration_id = resource.Body('configuration_id')
    configuration_name = resource.Body('configuration_name')
    #: *Type:str*
    id = resource.Body('id', alias='configuration_id')
    #: Name of the configuration group
    #: *Type:str*
    name = resource.Body('name', alias='configuration_name')
    #: Data store information
    #: *Type: dict*
    datastore = resource.Body('datastore', type=dict)
    #: Description of the configuration group
    #: *Type:str*
    description = resource.Body('description')
    #: Name of Datastore version
    #: *Type:str*
    datastore_version_name = resource.Body('datastore_version_name')
    #: Name of Datastore
    #: *Type:str*
    datastore_name = resource.Body('datastore_name')
    #: Individual Configuration values
    #: *Type:dict*
    configuration_parameters = resource.Body('configuration_parameters',
                                             type=list)
    #: Date of created
    #: *Type:str*
    created_at = resource.Body('created')
    #: Date of updated
    #: *Type:str*
    updated_at = resource.Body('updated')
    #: Indicates whether the parameter group is created by users.
    #: *Type:bool*
    is_user_defined = resource.Body('user_defined', type=bool)
    #: parameter group values defined by users
    #: *Type: dict*
    values = resource.Body('values', type=dict)

    #: Results of the configuration apply per instance
    #: *Type:list*
    apply_results = resource.Body('apply_results', type=list)

    @classmethod
    def find(cls, session, name_or_id, ignore_missing=True, **params):
        """Find a resource by its name or id.

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param name_or_id: This resource's identifier, if needed by
                           the request. The default is ``None``.
        :param bool ignore_missing: When set to ``False``
                    :class:`~openstack.exceptions.ResourceNotFound` will be
                    raised when the resource does not exist.
                    When set to ``True``, None will be returned when
                    attempting to find a nonexistent resource.
        :param dict params: Any additional parameters to be passed into
                            underlying methods, such as to
                            :meth:`~openstack.resource.Resource.existing`
                            in order to pass on URI parameters.

        :return: The :class:`Resource` object matching the given name or id
                 or None if nothing matches.
        :raises: :class:`openstack.exceptions.DuplicateResource` if more
                 than one resource is found for this request.
        :raises: :class:`openstack.exceptions.ResourceNotFound` if nothing
                 is found and ignore_missing is ``False``.
        """
        session = cls._get_session(session)
        # Try to short-circuit by looking directly for a matching ID.
        try:
            match = cls.existing(
                id=name_or_id,
                connection=session._get_connection(),
                **params)
            return match.fetch(session, **params)
        except exceptions.SDKException:
            pass

        data = cls.list(session, **params)

        result = cls._get_one_match(name_or_id, data)
        if result is not None:
            # Re-fetch configuration, since default list doesn't include
            # individual values
            result = result.fetch(session)
            if result is not None:
                return result

        if ignore_missing:
            return None
        raise exceptions.ResourceNotFound(
            "No %s found for %s" % (cls.__name__, name_or_id))

    def create(self, session, prepend_key=False, base_path=None):
        return super(Configuration, self).create(session,
                                                 prepend_key=prepend_key,
                                                 base_path=base_path)

    def commit(self, session, prepend_key=False, **further_attrs):
        return super(Configuration, self).commit(
            session,
            prepend_key=prepend_key,
            **further_attrs)

    def apply(self, session, instances):
        """Apply configuration to the given instances
        """
        url = utils.urljoin(self.base_path, self.id, 'apply')
        body = {'instance_ids': instances}
        response = session.put(
            url,
            json=body)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self
