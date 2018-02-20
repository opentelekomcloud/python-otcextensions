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

from openstack import _log
from openstack import resource

from otcextensions.sdk.obs import obs_service


_logger = _log.setup_logging('openstack')


class Object(resource.Resource):

    base_path = '/'
    resource_key = ''
    resources_key = ''
    service = obs_service.ObsService()

    # capabilities
    allow_get = True
    allow_list = True

    #: Bucket name
    # *Type:str*
    bucket = resource.Body('bucket')
    #: LastModified
    # *Type:datetime*
    lastmodified = resource.Body('lastmodified')
    #: Key
    # *Type:str*
    key = resource.Body('key')
    #: Size in bytes
    # *Type:int*
    size = resource.Body('size')
    #: ETag
    # *Type:str*
    etag = resource.Body('etag')
    #: Storage class
    # *Type:str*
    storageclass = resource.Body('storageclass')
    #: Version
    # *Type:int*
    versionid = resource.Body('versionid')
    #: Owner
    # *Type:dict*
    owner = resource.Body('owner', type=dict)
    #: Content type
    # *Type:str*
    contenttype = resource.Body('contenttype')
    #: Parts count
    # *Type:str*
    partscount = resource.Body('partscount')
