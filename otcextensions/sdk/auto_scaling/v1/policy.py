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
    #: The instance number action for
    instance_number = resource.Body('instance_number')


class Policy(_base.Resource):
    """AutoScaling Policy Resource"""
    resource_key = 'scaling_policy'
    resources_key = 'scaling_policies'
    base_path = '/scaling_policy'
    list_path = '/scaling_policy/%(scaling_group_id)s/list'
    query_marker_key = 'start_number'

    # capabilities
    allow_create = True
    allow_list = True
    allow_get = True
    allow_delete = True
    allow_update = True

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
    cool_down_time = resource.Body('cool_down_time')
    create_time = resource.Body('create_time')
    #: valid values include: ``INSERVICE``, ``PAUSED``
    status = resource.Body('policy_status')

    # Due to the other LIST url need to override
    # It is not efficient (as of implementation) to extend general list
    # with support of other url just for one service
    @classmethod
    def list(cls, session, paginated=False,
             endpoint_override=None, headers=None, **params):
        """Override default list to incorporate endpoint overriding
        and custom headers

        Since SDK Resource.list method is passing hardcoded headers
        do override the function

        This resource object list generator handles pagination and takes query
        params for response filtering.

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param bool paginated: ``True`` if a GET to this resource returns
                               a paginated series of responses, or ``False``
                               if a GET returns only one page of data.
                               **When paginated is False only one
                               page of data will be returned regardless
                               of the API's support of pagination.**
        :param dict params: These keyword arguments are passed through the
            :meth:`~openstack.resource.QueryParamter._transpose` method
            to find if any of them match expected query parameters to be
            sent in the *params* argument to
            :meth:`~keystoneauth1.adapter.Adapter.get`. They are additionally
            checked against the
            :data:`~openstack.resource.Resource.base_path` format string
            to see if any path fragments need to be filled in by the contents
            of this argument.

        :return: A generator of :class:`Resource` objects.
        :raises: :exc:`~openstack.exceptions.MethodNotSupported` if
                 :data:`Resource.allow_list` is not set to ``True``.
        :raises: :exc:`~openstack.exceptions.InvalidResourceQuery` if query
                 contains invalid params.

        """
        if not cls.allow_list:
            raise exceptions.MethodNotSupported(cls, "list")

        session = cls._get_session(session)

        # pop scaling_group_id, as it should not be also present in the query
        scaling_group_id = params.pop('scaling_group_id', None)
        uri_params = {
            'scaling_group_id': scaling_group_id
        }

        cls._query_mapping._validate(params, base_path=cls.base_path)
        query_params = cls._query_mapping._transpose(params)
        uri = cls.list_path % uri_params

        limit = query_params.get('limit')

        # Build additional arguments to the GET call
        get_args = cls._prepare_override_args(
            endpoint_override=endpoint_override,
            # request_headers=request.headers,
            additional_headers=headers)

        total_yielded = 0
        while uri:
            response = session.get(
                uri,
                params=query_params.copy(),
                **get_args
            )
            exceptions.raise_from_response(response)
            data = response.json()

            # Discard any existing pagination keys
            query_params.pop('marker', None)
            query_params.pop('limit', None)

            if cls.resources_key:
                resources = data[cls.resources_key]
            else:
                resources = data

            if not isinstance(resources, list):
                resources = [resources]

            marker = None
            for raw_resource in resources:
                # Do not allow keys called "self" through. Glance chose
                # to name a key "self", so we need to pop it out because
                # we can't send it through cls.existing and into the
                # Resource initializer. "self" is already the first
                # argument and is practically a reserved word.
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
                query_params.update(next_params)
            else:
                return

    def _action(self, session, body):
        """Preform alarm actions given the message body."""
        # if getattr(self, 'endpoint_override', None):
        #     # If we have internal endpoint_override - use it
        #     endpoint_override = self.endpoint_override
        url = utils.urljoin(self.base_path, self.id, 'action')
        return session.post(
            url,
            # endpoint_override=endpoint_override,
            json=body)

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
