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
Create an multipart upload of a large object
"""

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')
sdk.register_otc_extensions(conn)
sdk.get_ak_sk(conn)

container = conn.obs.create_container(
    name='test-multipart',
    storage_acl='private',
    storage_class='STANDARD'
)

obj = conn.obs.upload_object(
    name='pdfs/book.pdf',
    filename='my-book.pdf',
    container=container,
    segment_size=1400000
)
