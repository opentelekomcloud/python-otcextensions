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
from openstack import exceptions


from otcextensions.sdk.auto_scaling.v1 import _base


class ScheduledPolicy(resource.Resource):
    #: schedule time,
    #:  ** if policy type is ``SCHEDULED``, launch time should be
    #:          ``YYYY-MM-DDThh:mmZ``,
    #:  ** if policy type is ``RECURRENCE``, launch time should be ``hh:mm``
    launch_time = resource.Body('launch_time')
    #: Recurrence Type,
    #: valid values include: ``Daily``, ``Weekly``, ``Monthly``
    recurrence_type = resource.Body('recurrence_type')
    #: Used in concert with ``recurrence_type``,
    #:  ** if recurrence_type is Daily, recurrence_value has no meaning
    #:  ** if recurrence_type is Weekly, recurrence_value means days of week,
    #:       1,3,5 means scheduled at monday, Wednesday, Friday of every week
    #:  ** if recurrence_type is Monthly, recurrence_value means days of month
    #:       1,10,30 means scheduled at first, 10th, 30th day of every month
    recurrence_value = resource.Body('recurrence_value')
    #: policy effect start time (UTC)
    start_time = resource.Body('start_time')
    #: policy effect end time (UTC)
    end_time = resource.Body('end_time')


class Action(resource.Resource):
    #: Scaling trigger action type
    #: valid values include: ``ADD``, ``REMOVE``, ``SET``
    operation = resource.Body('operation')
    #: Number of instances which will be operated by the action
    #: Values from 0 to 200 are possible.
    #: Note: Use either instance_number or instance_percentage
    #: If nothing of instance_number or instance_percentage is set, the default
    #: value is 1.
    instance_number = resource.Body('instance_number', type=int)
    #: Percentage of instances which are currently there to be operated by the action
    #: Values from 0 to 20000 are possible.
    #: Note: Use either instance_number or instance_percentage
    #: If nothing of instance_number or instance_percentage is set, the default
    #: value is 1.
    instance_percentage = resource.Body('instance_percentage', type=int)



class Policy(_base.Resource):
    """AutoScaling Policy Resource"""
    resource_key = 'scaling_policy'
    resources_key = 'scaling_policies'
    base_path = '/scaling_policy'
    query_marker_key = 'start_number'

    # capabilities
    allow_create = True
    allow_list = True
    allow_fetch = True
    allow_delete = True
    allow_commit = True

    _query_mapping = resource.QueryParameters(
        'limit', 'name', 'type', 'marker',
        name='scaling_policy_name',
        type='scaling_policy_type',
        marker=query_marker_key,
    )

    #: Properties
    #: AutoScaling policy ID
    id = resource.Body('scaling_policy_id', alternate_id=True)
    #: AutoScaling policy name
    name = resource.Body('scaling_policy_name')
    #: AutoScaling policy trigger type
    #: valid values include: ``ALARM``, ``SCHEDULED``, ``RECURRENCE``
    type = resource.Body('scaling_policy_type')
    #: AutoScaling group reference the policy apply to
    scaling_group_id = resource.URI('scaling_group_id')

    alarm_id = resource.Body('alarm_id')
    scheduled_policy = resource.Body('scheduled_policy',
                                     type=ScheduledPolicy)
    scaling_policy_action = resource.Body('scaling_policy_action',
                                          type=Action)
    cool_down_time = resource.Body('cool_down_time', type=int)
    create_time = resource.Body('create_time')
    #: valid values include: ``INSERVICE``, ``PAUSED``
    status = resource.Body('policy_status')

    def execute(self, session):
        """execute policy"""
        body = {"action": "execute"}
        self._action(session, body)

    def pause(self, session):
        """pause policy"""
        body = {"action": "pause"}
        self._action(session, body)

    def resume(self, session):
        """resume policy"""
        body = {"action": "resume"}
        self._action(session, body)

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
        group_id = params.pop('group_id', None)
        try:
            match = cls.existing(
                id=name_or_id,
                connection=session._get_connection(),
                **params)
            return match.fetch(session, **params)
        except exceptions.NotFoundException:
            pass

        # if ('name' in cls._query_mapping._mapping.keys()
        #       and 'name' not in params):
        params['name'] = name_or_id

        data = cls.list(session, base_path='/scaling_policy/{id}/list'.format(id=group_id), **params)

        result = cls._get_one_match(name_or_id, data)
        if result is not None:
            return result

        if ignore_missing:
            return None
        raise exceptions.ResourceNotFound(
            "No %s found for %s" % (cls.__name__, name_or_id))