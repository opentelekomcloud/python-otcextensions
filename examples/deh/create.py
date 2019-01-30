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

"""
Create DeH instance.

For a full guide see
http://developer.openstack.org/sdks/python/openstacksdk/user/guides/deh.html
"""


def create_host(conn):
    print("Create Host:")

    host = conn.deh.create_host(
        name='my_new_host',
        # host_type can be retrieved with host_types() call
        host_type='general',
        availability_zone='eu-de-01',
        # amount of hosts to allocate
        quantity=1
    )

    # dedicated_host_ids is a list of allocated hosts (since multiple may
    # be requested)

    print(host.dedicated_host_ids)
