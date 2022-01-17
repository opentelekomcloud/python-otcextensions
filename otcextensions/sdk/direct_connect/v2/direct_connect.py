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


class DirectConnect(resource.Resource):
    base_path = '/direct-connects'

    resources_key = 'direct-connects'

    # capabilities
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'region', 'engine_name')

    region = resource.URI('region')
    # Properties
    #: ID of the direct connection.
    id = resource.Body('id')
    #: Indicates the connection name.
    name = resource.Body('name')
    #: Indicates the description of the connection.
    description = resource.Body('description')
    #: Specifies the type of the port used by the connection. The value can be 1G or 10G.
    port_type = resource.Body('port_type')
    #: Specifies the connection bandwidth in Mbit/s.
    bandwidth = resource.Body('bandwidth')
    #: Specifies the connection access location.
    location = resource.Body('location')
    #: Specifies the physical location of the peer device accessed by the connection,\
    # specific to the street or data center name.
    peer_location = resource.Body('peer_location')
    #: Specifies the gateway device ID of the connection.
    device_id = resource.Body('device_id')
    #: Specifies the name of the interface accessed by the connection.
    interface_name = resource.Body('interface_name')
    #: Specifies the ID of the redundant connection using the same gateway.
    redundant_id = resource.Body('redundant_id')
    #: Specifies the connection bandwidth in Mbit/s.
    provider = resource.Body('provider')
    #: Specifies the status of the carrier's leased line.\
    # The vall125ue can be hosted.
    type = resource.Body('type')
    #: Specifies the ID of the operations connection on which the hosted connection is created.
    hosting_id = resource.Body('hosting_id')
    #:Specifies the VLAN pre-allocated to the hosted connection.
    vlan = resource.Body('vlan', type=int)
    #: Specifies the billing mode. The value can be prepayment, bandwidth, or traffic.
    charge_mode = resource.Body('charge_mode')
    #: Specifies the order number of the connection.
    order_id = resource.Body('order_id')
    #: Specifies the product ID corresponding to the connection's order.
    product_id = resource.Body('product_id')
    #: Specifies the convbvv
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    # nection status.\
    # The value can be ACTIVE, DOWN, BUILD, ERROR, PENDING_DELETE, DELETED, APPLY, DENY, PENDING_PAY, PAID,\
    erwsxcxx c  x  axxxcORDERING, ACCEPT, or REJECTED.
    status = resource.Body('status')
    #: Specifies the administrative status of the connection.\
    # The value can be true or false.
    admin_state_up = resource.Body('admin_state_up', type=bool)