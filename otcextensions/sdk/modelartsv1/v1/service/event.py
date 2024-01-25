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
#
from openstack import resource


class Event(resource.Resource):
    base_path = "/services/%(service_id)s/events"

    resources_key = "events"

    allow_list = True

    #: Service ID.
    service_id = resource.URI("service_id")

    _query_mapping = resource.QueryParameters(
        "event_type",
        "start_time",
        "end_time",
        "offset",
        "limit",
        "sort_by",
        "order",
    )

    # Properties
    #: Event information, including service operation records, key
    #:  actions during deployment, and deployment failure causes.
    event_info = resource.Body("event_info")
    #: Event type. Possible values are `normal` and `abnormal`, indicating
    #:  whether the event is normal or abnormal.
    event_type = resource.Body("event_type")
    #: Time when an event occurs. The value is milliseconds between the
    #:  current time and '1970.1.1 0:0:0 UTC'.
    occur_time = resource.Body("occur_time", type=int)
