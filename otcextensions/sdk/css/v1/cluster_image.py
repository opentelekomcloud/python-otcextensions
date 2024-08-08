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


class ImageInfoListSpec(resource.Resource):
    #: Image engine type.
    datastore_type = resource.Body('datastoreType')
    #: Image engine version.
    datastore_version = resource.Body('datastoreVersion')
    #: Name of an image that can be upgraded.
    display_name = resource.Body('displayName')
    #: ID of an image that can be upgraded.
    id = resource.Body('id')
    #: Image description.
    image_desc = resource.Body('imageDesc')
    #: Priority.
    priority = resource.Body('priority', type=int)


class ClusterImage(resource.Resource):
    base_path = '/clusters/%(cluster_id)s/target/%(upgrade_type)s/images'
    allow_fetch = True
    #: Cluster ID.
    cluster_id = resource.URI('cluster_id')
    #: Version type. The value can be:
    #: \nsame: upgrade to the same version.
    #: \ncross: upgrade to a different version.
    #: \ncrossEngine: cross-engine upgrade.
    upgrade_type = resource.URI('upgrade_type')
    #: Indicates whether to upload the plug-in of the target version.
    need_upload_upgrade_plugin = resource.Body(
        'needUploadUpgradePlugin', type=bool
    )
    #: Image details.
    image_info_list = resource.Body(
        'imageInfoList', type=list, list_type=ImageInfoListSpec
    )
