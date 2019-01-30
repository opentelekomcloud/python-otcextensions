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
List host_types from the DeH service.

For a full guide see
http://developer.openstack.org/sdks/python/openstacksdk/user/guides/deh.html
"""


def list_host_types(conn, az):
    print("List Host types in AZ %s:" % az)

    for host_type in conn.deh.host_types(az):
        print(host_type)
