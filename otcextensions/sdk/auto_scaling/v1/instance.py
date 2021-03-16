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

from otcextensions.i18n import _
from otcextensions.sdk.auto_scaling.v1 import _base


class Instance(_base.Resource):
    ACTION_TYPES = ['ADD', 'REMOVE', 'PROTECT', 'UNPROTECT']

    resource_key = 'scaling_group_instance'
    resources_key = 'scaling_group_instances'
    # ok, we just fix the base path to list because there are no common rules
    # for the operations for instance
    base_path = '/scaling_group_instance'
    query_marker_key = 'start_number'

    # capabilities
    allow_list = True
    allow_delete = True

    _query_mapping = resource.QueryParameters(
        'id', 'name',
        'health_status', 'limit',
        scaling_group_id='group_id',
        lifecycle_status='life_cycle_state',
        marker=query_marker_key
    )

    #: Properties
    #: AutoScaling instance id
    id = resource.Body('instance_id', alternate_id=True)
    #: AutoScaling instance name
    name = resource.Body('instance_name')
    #: Id of AutoScaling group the instance belongs to
    scaling_group_id = resource.URI('scaling_group_id')
    #: Name of AutoScaling group the instance belongs to
    scaling_group_name = resource.Body('scaling_group_name')
    #: Id of AutoScaling config the instance create with
    scaling_configuration_id = resource.Body('scaling_configuration_id')
    #: Name of AutoScaling config the instance create with
    scaling_configuration_name = resource.Body('scaling_configuration_name')
    #: AutoScaling instance lifecycle state, valid values include:
    #: ``INSERVICE``, ``PENDING``, ``REMOVING``
    lifecycle_state = resource.Body('life_cycle_state')
    #: AutoScaling instance health state, valid values include:
    #: ``INITIALIZING``, ``NORMAL``, ``ERROR``
    health_status = resource.Body('health_status')
    #: AutoScaling instance create time
    create_time = resource.Body('create_time')

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
        group_id = params.pop('group_id', None)

        base_path = '/scaling_group_instance/{id}/list'.format(id=group_id)
        data = cls.list(session, base_path=base_path, **params)
        result = cls._get_one_match(name_or_id, data)
        if result is not None:
            return result

        if ignore_missing:
            return None
        raise exceptions.ResourceNotFound(
            "No %s found for %s" % (cls.__name__, name_or_id))

    def remove(self, session, delete_instance=False, ignore_missing=True):
        """Remove an instance of auto scaling group

        :precondition:
            * the instance must in ``INSERVICE`` status.
            * after remove the instance number of auto scaling group should not
                be less than min instance number.
            * The owner auto scaling group should not in scaling status.

        :param session: openstack session
        :param bool delete_instance: When set to ``True``, instance will be
            deleted after removed.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the config does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent config.

        :returns: None
       """
        uri = utils.urljoin('/scaling_group_instance', self.id)
        delete_instance = 'yes' if delete_instance else 'no'
        return session.delete(uri,
                              params={'instance_delete': delete_instance})

    def _action(self, session, body):
        """Preform alarm actions given the message body.

        """
        url = utils.urljoin(self.base_path, self.scaling_group_id, 'action')
        return session.post(
            url,
            # endpoint_override=endpoint_override,
            json=body)

    def batch_action(self, session, instances, action, delete_instance=False):
        """batch action on auto-scaling instances

        make sure all configs should not been used by auto-scaling group

        :param session: openstack session
        :param instances: The list item value can be the ID of an instance
            or a :class:`~otcextensions.sdk.auto_scaling.v1.instance.Instance`
            instance
        :param action: Action to execute on instances:
            [``ADD``, ``REMOVE``, ``PROTECT``, ``UNPROTECT``]
        :param bool delete_instance: When set to ``True``, instance will be
            deleted after removed

        :returns: None
        """
        act = action.upper()
        if act not in self.ACTION_TYPES:
            msg = (_('Action type %(action)s is not supported %(types)s') %
                   {'action': action, 'types': self.ACTION_TYPES})
            raise exceptions.SDKException(msg)
        if delete_instance and act != 'REMOVE':
            msg = (_('Action type %s does not support delete_instance arg') %
                   (action))
            raise exceptions.SDKException(msg)
        ids = [instance.id if isinstance(instance, Instance) else instance
               for instance in instances]
        json_body = {
            'action': act,
            'instances_id': ids
        }
        if delete_instance:
            json_body['instance_delete'] = 'yes'
        return self._action(session, json_body)
