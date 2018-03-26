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
    list_path = '/scaling_group_instance/%(scaling_group_id)s/list'
    query_marker_key = 'start_number'

    # capabilities
    allow_create = False
    allow_list = True
    allow_get = False
    allow_delete = True

    _query_mapping = resource.QueryParameters(
        'health_status', 'limit',
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
    def list(cls, session, paginated=False,
             endpoint_override=None, headers=None, **params):
        return super(Instance, cls).list_ext(
            session, paginated,
            endpoint_override, headers,
            **params)

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
            msg = (_('Action type %s is not supported %s') %
                   (action, self.ACTION_TYPES))
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
