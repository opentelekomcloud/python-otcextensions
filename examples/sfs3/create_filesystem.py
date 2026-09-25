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
import openstack
from otcextensions import sdk

"""
Create a SFS General Purpose File System (SFS3).

Works with a plain password-auth connection: when no AK/SK is configured,
the SDK transparently creates a temporary AK/SK via the identity service.
"""

openstack.enable_logging(True)
conn = openstack.connect(cloud="otc")
sdk.register_otc_extensions(conn)

fs = conn.sfs3.create_filesystem(name="test-sfs3-fs")
