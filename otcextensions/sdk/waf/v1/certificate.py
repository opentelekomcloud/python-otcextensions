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

from otcextensions.sdk.waf.v1 import _base


class Certificate(_base.Resource):
    """WAF Certificate Resource"""
    resources_key = 'items'
    base_path = '/waf/certificate'

    # capabilities
    allow_create = True
    allow_list = True
    allow_fetch = True
    allow_delete = True
    allow_commit = True

    _query_mapping = resource.QueryParameters(
        'limit', 'offset')

    #: Properties
    #: Specifies the certificate content.
    content = resource.Body('content')
    #: Certificate expiration time
    expire_time = resource.Body('expireTime')
    #: Specifies the private key content.
    key = resource.Body('key')
    #: Certificat uploading timestamp
    timestamp = resource.Body('timestamp')
