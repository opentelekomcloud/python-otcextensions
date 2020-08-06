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


# class MetaDataSpec(resource.Resource):

# Properties
# Number of returned results / alarms
# count = resource.Body('count')
# Indicates pagination marker
# marker = resource.Body('marker')
# Number of total queried results / alarms
# total = resource.Body('total')


class AlarmActionsSpec(resource.Resource):

    # Properties
    # notification list ID
    notificationList = resource.Body('notificationList')
    # Indicates the type of action triggered by an alarm.
    # Value can be notication or autoscaling
    type = resource.Body('type')


class OkActionsSpec(resource.Resource):

    # Properties
    # notification list ID
    notificationList = resource.Body('notificationList')
    # Indicates the type of action triggered by an alarm.
    # Value can be notication or autoscaling
    type = resource.Body('type')


class ConditionSpec(resource.Resource):

    # Properties
    # indicates the comparison operator
    # values can be <,=,>,>= or <=
    comparison_operator = resource.Body('comparison_operator')
    # Indicates how many consecutive times an alarm has
    # been generated
    count = resource.Body('count', type=int)
    # indicates the data rollup method
    # values: max, min, average, sum, variance
    filter = resource.Body('filter')
    # Indicates the interval (in seconds) for checking
    # whether the configured alarm rules are met
    period = resource.Body('period', type=int)
    # Data unit
    unit = resource.Body('unit')
    # Alarm threshold
    value = resource.Body('value', type=int)


class DimensionsSpec(resource.Resource):

    # Properties
    #: dimension.name: object type e.g. ECS (instance_id)
    name = resource.Body('name')
    #: dimension.value: object id e.g. ECS ID
    value = resource.Body('value')


class MetricSpec(resource.Resource):

    # Properties
    # List of metric dimensions
    dimensions = resource.Body('dimensions', type=DimensionsSpec)
    # Specifies the metric name
    metric_name = resource.Body('metric_name')
    # Metric Namespace
    namespace = resource.Body('namespace')


class Alarm(resource.Resource):

    resources_key = 'metric_alarms'
    base_path = '/alarms'

    # capabilities
    allow_commit = True
    allow_create = True
    allow_fetch = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'limit', 'order', 'start'
    )

    # Properties
    # Specifies the action triggered by an alarm.
    alarm_actions = resource.Body('alarm_actions', type=AlarmActionsSpec)
    # Indicates whether an action will be triggered by an alarm
    # True: action will be triggered
    # False: action will not be triggered
    alarm_action_enabled = resource.Body('alarm_action_enabled', type=bool)
    # Description of the alarm
    alarm_description = resource.Body('alarm_description')
    # Alarm is enabled (True) or disabled (False)
    alarm_enabled = resource.Body('alarm_enabled', type=bool)
    # alarm rule ID
    alarm_id = resource.Body('alarm_id', alternate_id=True)
    # alarm severity
    # values: 1: critical, 2: major, 3: minor, 4: informational alarm
    alarm_level = resource.Body('alarm_level', type=int)
    # Alarm status
    # ok: alarm status is normal
    # alarm: an alarm is generated
    # insufficient_data: required data is insufficient
    alarm_state = resource.Body('alarm_state')
    # Name of the alarm
    name = resource.Body('alarm_name')
    # Indicates the action triggered by clearing an alarm
    ok_actions = resource.Body('ok_actions', type=OkActionsSpec)
    # Describes alarm triggering condititon
    condition = resource.Body('condition', type=ConditionSpec)
    # Specification of specific alarm
    metric = resource.Body('metric', type=MetricSpec)
    # Time when alarm status changed
    # UNIX timestamp in ms
    update_time = resource.Body('update_time')

    def _translate_response(self, response, has_body=None, error_message=None):
        """Given a KSA response, inflate this instance with its data

        DELETE operations don't return a body, so only try to work
        with a body when has_body is True.

        This method updates attributes that correspond to headers
        and body on this instance and clears the dirty set.
        """
        if has_body is None:
            has_body = self.has_body
        exceptions.raise_from_response(response, error_message=error_message)
        if has_body:
            try:
                body = response.json()
                if self.resources_key and self.resources_key in body:
                    body = body[self.resources_key][0]
                body_attrs = self._consume_body_attrs(body)
                self._body.attributes.update(body_attrs)
                self._body.clean()

            except ValueError:
                # Server returned not parse-able response (202, 204, etc)
                # Do simply nothing
                pass

        headers = self._consume_header_attrs(response.headers)
        self._header.attributes.update(headers)
        self._header.clean()
        self._update_location()
        dict.update(self, self.to_dict())

    def _action(self, session, body):
        """Perform actions given the message body.

        """
        url = utils.urljoin(self.base_path, self.id, "action")
        response = session.put(
            url,
            json=body)
        exceptions.raise_from_response(response)
        return response

    def change_alarm_status(self, session):
        body = {
            "alarm_enabled": True
        }
        current_status = self.get('alarm_enabled')
        if current_status is True:
            body.update({'alarm_enabled': False})
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
            return result

        if ignore_missing:
            return None
        raise exceptions.ResourceNotFound(
            "No %s found for %s" % (cls.__name__, name_or_id))
