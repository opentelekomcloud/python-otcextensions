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
# from openstack import exceptions
from openstack import resource
from openstack import _log

from otcextensions.sdk import sdk_resource
from otcextensions.sdk.dns import dns_service

_logger = _log.setup_logging('openstack')


class ZoneRecordset(sdk_resource.Resource):
    """ZoneRecordset Resource"""
    resource_key = 'recordset'
    resources_key = 'recordsets'
    base_path = '/zones/%(zone_id)s/recordsets'
    # list_all_base_path = '/recordsets'
    service = dns_service.DnsService()

    # capabilities
    allow_create = True
    allow_list = True
    allow_get = True
    allow_delete = True
    allow_update = True

    _query_mapping = resource.QueryParameters(
        'zone_type', 'limit', 'marker', 'offset', 'tags')

    #: Properties
    #: The id of the Zone which this recordset belongs to
    zone_id = resource.URI('zone_id')
    #: Timestamp when the zone was created
    created_at = resource.Body('create_at')
    #: Recordset description
    description = resource.Body('description')
    #: Is the recordset created by system.
    is_default = resource.Body('default', type=bool)
    #: Links contains a `self` pertaining to this zone or a `next` pertaining
    #: to next page
    links = resource.Body('links', type=dict)
    #: Recordset name
    name = resource.Body('name')
    #: ID of the project which the recordset belongs to
    project_id = resource.Body('project_id')
    #: DNS record value list
    records = resource.Body('records', type=list)
    #: Recordset status
    #: Valid values include `PENDING_CREATE`, `ACTIVE`,
    #:                      `PENDING_DELETE`, `ERROR`
    status = resource.Body('status')
    #: Time to live, default 300, available value 300-2147483647 (seconds)
    ttl = resource.Body('ttl', type=int)
    #: DNS type of the recordset
    #: Valid values include `A`, `AAA`, `MX`, `CNAME`, `TXT`, `NS`
    #: In private zones `SOA`, `SRV`, `PTR`
    type = resource.Body('type')
    #: Timestamp when the zone was last updated
    updated_at = resource.Body('update_at')
    #: The name of the Zone which this recordset belongs to
    zone_name = resource.Body('zone_name')

    # @classmethod
    # def list(cls, session, paginated=False, **params):
    #
    #     if not cls.allow_list:
    #         raise exceptions.MethodNotSupported(cls, "list")
    #
    #     session = cls._get_session(session)
    #
    #     cls._query_mapping._validate(params, base_path=cls.base_path)
    #     query_params = cls._query_mapping._transpose(params)
    #
    #     # decide the correct URI for the request based on the query
    #     base_uri = cls.base_path if 'zone_id' in params \
    #         else cls.list_all_base_path
    #     uri = base_uri % params
    #
    #     limit = query_params.get('limit')
    #
    #     # Build additional arguments to the GET call
    #     get_args = cls._prepare_override_args()
    #
    #     total_yielded = 0
    #     while uri:
    #         response = session.get(
    #             uri,
    #             params=query_params.copy(),
    #             **get_args
    #         )
    #         exceptions.raise_from_response(response)
    #         if response.status_code == 204:
    #             # Some bad APIs (i.e. DCS.Backup.List) return emptiness
    #             return
    #         data = response.json()
    #
    #         # Discard any existing pagination keys
    #         query_params.pop('marker', None)
    #         query_params.pop('limit', None)
    #
    #         if cls.resources_key:
    #             resources = data[cls.resources_key]
    #         else:
    #             resources = data
    #
    #         if not isinstance(resources, list):
    #             resources = [resources]
    #
    #         marker = None
    #         for raw_resource in resources:
    #             raw_resource.pop("self", None)
    #
    #             if cls.resource_key and cls.resource_key in raw_resource:
    #                 raw_resource = raw_resource[cls.resource_key]
    #
    #             value = cls.existing(**raw_resource)
    #
    #             marker = value.id
    #             yield value
    #             total_yielded += 1
    #
    #         if resources and paginated:
    #             uri, next_params = cls._get_next_link(
    #                 uri, response, data, marker, limit, total_yielded)
    #             query_params.update(next_params)
    #         else:
    #             return


class Recordset(ZoneRecordset):
    """Recordsets resource represent list all recordset API response"""
    base_path = '/recordsets'
