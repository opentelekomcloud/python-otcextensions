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
Manage tags of SFS General Purpose File Systems (SFS3).

Per-file-system tag operations are addressed by file system name. The
project-level queries (``get_project_tags``, ``filter_resources_by_tags``,
``count_resources_by_tags``) operate on the whole project and do not
require a specific file system.
"""

openstack.enable_logging(True)
conn = openstack.connect(cloud="otc")
sdk.register_otc_extensions(conn)

fs_name = "test-sfs3-fs"

# Add tags to a file system
conn.sfs3.add_tags(fs_name, [{"key": "env", "value": "production"}])

# Get the tags of a file system
print(conn.sfs3.get_tags(fs_name))

# Delete tags from a file system
conn.sfs3.delete_tags(fs_name, [{"key": "env", "value": "production"}])

# Query the tags of all file systems in the project
print(conn.sfs3.get_project_tags())

# Query file systems by tag
print(
    conn.sfs3.filter_resources_by_tags(
        tags=[{"key": "env", "values": ["production"]}], limit=100
    )
)

# Count file systems by tag
print(
    conn.sfs3.count_resources_by_tags(tags=[{"key": "env", "values": ["production"]}])
)
