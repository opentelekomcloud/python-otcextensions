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
from openstack.dns.v2 import recordset
from otcextensions.sdk import dnsmixin


class Recordset(dnsmixin.DNSProxyMixin, recordset.Recordset):
    """DNS Recordset Resource"""

    _query_mapping = resource.QueryParameters(
        'name', 'type', 'ttl', 'data', 'status', 'description',
        'limit', 'marker', 'offset', 'tags')

    #: Properties
    #: Is the recordset created by system.
    is_default = resource.Body('default', type=bool)
    #: Timestamp when the zone was last updated.
    updated_at = resource.Body('update_at')
