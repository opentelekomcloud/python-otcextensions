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


class OperationDefinition(resource.Resource):
    #: Properties
    #: Specifies the number of retained daily backups
    #: The latest backup of each day is saved in the long term. This parameter
    #: can be effective together with the max number of retained backups
    #: specified by 'max_backups'.
    #: value: 0 to 100
    #: If this property is configured, 'timezone' is mandatory.
    day_backups = resource.Body('day_backups', type=int)
    #: Maximum number of retained backups.
    #: value: -1 or ranges from 0 to 99999
    #: If -1 is set, the backups will not be cleared even though the
    #: configured retained backup quantity is exceeded.
    #: If this parameter and 'retention_duration_days' are both left blank,
    #: the backups will be retained permanently
    max_backups = resource.Body('max_backups', type=int)
    #: Specifies the number of retained monthly backups.
    #: The latest backup of each month is saved in the long term. This
    #: parameter can be effective together with the max number of  retained
    #: backups specified by 'max_backups'.
    #: value: ranges from 0 to 100
    #: If this parameter is configured 'timezone' is mandatory.
    month_backups = resource.Body('month_backups', type=int)
    #: Duration of retaining a backup in days
    #: value: -1 or ranges from 0 to 99999
    #: -1 indicates that the backups will not be cleared bassed on the
    #: retention duration. if this parameter and 'max_backups' are left blank
    #: at the same time, the backups will be retained permanently.
    retention_duration_days = resource.Body('retention_duration_days',
                                            type=int)
    #: Time where the user is located, e.g.: UTC+08:00
    #: This paramter is only configurable if 'day_backups, 'week_backups',
    #: 'month_backups' or 'year_backups' are set.
    timezone = resource.Body('timezone')
    #: Specifies the number or retained weekly backups.
    #: The latest backup of each week is saved in the long term. This
    #: param can be effective together with the max number of retained
    #: backups specified by 'max_backups'. If this param is configured,
    #: 'timezone' is mandatory.
    #: value: ranges from 0 to 100
    week_backups = resource.Body('week_backups', type=int)
    #: Specifies the number or retained yearly backups.
    #: The latest backup of each year is saved in the long term. This
    #: param can be effective together with the max number of retained
    #: backups specified by 'max_backups'. If this param is configured,
    #: 'timezone' is mandatory.
    #: value: ranges from 0 to 100
    year_backups = resource.Body('year_backups', type=int)


class Properties(resource.Resource):
    #: Properties
    #: Scheduling rule.
    #: In the replication policy, you are advised  to set one time point
    #: for one day. A max number of 24 rules can be configured.
    #: The scheduling rule complies with iCalender RFC 2445, but ita supports
    #: only the following params: 'FREQ', 'BYDAY', 'BYHOUR', 'BYMINUTE', and
    #: 'INTERVAL.
    #: 'FREQ' can be set to 'WEEKLY' and 'DAILY'.
    #: 'BYDAY' can bne set to: MO, TU, WE, TH, FR, SA, SU
    #: 'BYHOUR' ranges from 0 to 23 hours
    #: 'BYMINUTE' ranges from 0 to 59
    #: The scheduling interval must not be less than 1 hour.
    #: A max of 24 time points are allowed in a day, e.g. If scheduling time
    #: is 14:00 from Monday to Sunday, set the scheduling rule as follows:
    #: 'FREQ=WEEKLY;BYDAY=MO;TU;WE;TH;FR;SA;SU;BYHOUR=14;BYMINUTE=00'
    #: If the scheduling time is 14:00 every day:
    #: FREQ=DAILY;INTERVAL=1;BYHOUR=14;BYMINUTE=00
    pattern = resource.Body('pattern', type=list)


class Trigger(resource.Resource):
    #: Properties
    #: Scheduler attributes
    properties = resource.Body('properties', type=Properties)


class Vault(resource.Resource):
    #: Properties
    #: ID of the associated remote vault
    destination_vault_id = resource.Body('destination_vault_id')
    #: Vault ID
    vault_id = resource.Body('vault_id')


class Policy(resource.Resource):
    """CBR Policy Resource"""
    resource_key = 'policy'
    resources_key = 'policies'
    base_path = '/policies'

    # capabilities
    allow_create = True
    allow_list = True
    allow_fetch = True
    allow_delete = True
    allow_commit = True

    _query_mapping = resource.QueryParameters(
        'operation_type', 'vault_id')

    #: Properties
    #: associated vault
    associated_vaults = resource.Body('associated_vaults', type=list,
                                      list_type=Vault)
    #: Whether to enable the policy
    enabled = resource.Body('enabled', type=bool)
    #: Policy ID
    id = resource.Body('id')
    #: Policy Name
    #: Max: 64 chars
    name = resource.Body('name')
    #: Scheduling parameter
    operation_definition = resource.Body('operation_definition',
                                         type=OperationDefinition)
    #: Policy type
    #: values: backup, replication
    operation_type = resource.Body('operation_type')
    #: Time rule for the policy execution
    trigger = resource.Body('trigger', type=Trigger)
