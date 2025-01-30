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


class ListEvents(resource.Resource):
    id = resource.Body('id', type=str)
    last_modified = resource.Body('last_modified', type=int)
    name = resource.Body('name', type=str)


class Event(resource.Resource):
    base_path = '/fgs/functions/%(function_urn)s/events'

    # Capabilities
    allow_create = True
    allow_fetch = True
    allow_delete = True
    allow_list = True
    allow_commit = True

    # Properties
    function_urn = resource.URI('function_urn', type=str)
    #: Test event name. Max. 25 of letters, digits, hyphens (-),
    #: and underscores (_). Start with a letter,
    #: and end with a letter or digit.
    name = resource.Body('name', type=str)
    #: Test event content, which is a Base64-encoded JSON character string.
    content = resource.Body('content', type=str)

    # Attributes
    #: Test event ID.
    id = resource.Body('id', type=str)
    #: Total number of test events.
    count = resource.Body('count', type=int)
    #: Total number of test events.
    events = resource.Body('events', type=list, list_type=ListEvents)
    #: Next read location.
    next_marker = resource.Body('next_marker', type=int)
    #: Last update time.
    updated_at = resource.Body('last_modified', type=int)
