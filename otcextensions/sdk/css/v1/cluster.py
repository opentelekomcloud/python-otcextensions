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
# import six
from openstack import exceptions
from openstack import resource
from openstack import utils

from otcextensions.common import format as otc_format


class DatastoreSpec(resource.Resource):
    #: Datastore version
    version = resource.Body('version', default='6.2.3')
    #: Engine type
    type = resource.Body('type', default='elasticsearch')


class NetworkSpec(resource.Resource):
    #: Router ID (VPC id)
    router_id = resource.Body('vpcId')
    #: Network ID
    network_id = resource.Body('netId')
    #: Security group ID
    security_group_id = resource.Body('securityGroupId')


class InstanceSpec(resource.Resource):
    #: Instance flavor name
    flavor = resource.Body('flavorRef')
    #: Volume object {volume_type:[COMMON, HIGH, ULTRAHIGH], size:int}
    volume = resource.Body('volume', type=dict)
    #: Network information
    nics = resource.Body('nics', type=NetworkSpec)
    #: Availability zone
    availability_zone = resource.Body('availability_zone')


class DiskEncryption(resource.Resource):
    #: Disk encryption flag
    is_disk_encrypted = resource.Body('systemEncrypted',
                                      type=otc_format.Bool_10)
    #: KMS Key ID
    cms_id = resource.Body('systemCmkid')


class Cluster(resource.Resource):
    base_path = '/clusters'

    resources_key = 'clusters'
    resource_key = 'cluster'

    allow_create = True
    allow_list = True
    allow_commit = True
    allow_delete = True
    allow_fetch = True
    allow_patch = True

    # Properties
    #: Current actions
    actions = resource.Body('actions', type=list)
    #: KMS Key ID (read only)
    cmk_id = resource.Body('cmkId')
    #: Cluster creation time
    created_at = resource.Body('created')
    #: Type of the data search engine
    datastore = resource.Body('datastore', type=DatastoreSpec)
    #: Disk encryption specification
    disk_encryption = resource.Body('diskEncryption', type=DiskEncryption)
    #: Error object
    error = resource.Body('failed_reasons', type=dict)
    #: Cluster endpoint
    endpoint = resource.Body('endpoint')
    #: Instance object
    instance = resource.Body('instance', type=InstanceSpec)
    #: Cluster nodes (read only)
    nodes = resource.Body('instances', type=list, list_type=dict)
    #: Number of cluster instances (1..32)
    instance_count = resource.Body('instanceNum', type=int)
    #: Disk encryption flag (read only)
    is_disk_encrypted = resource.Body('diskEncrypted', type=bool)
    #: Whether communication encyption is performed on the cluster
    is_https_enabled = resource.Body('httpsEnable', type=otc_format.BoolStr_1)
    #: Operation progress
    progress = resource.Body('actionProgress', type=dict)
    #: Router ID (read only)
    router_id = resource.Body('vpcId')
    #: Security group ID (read only)
    security_group_id = resource.Body('securityGroupId')
    #: Cluster status:
    #:  - 100: Cluster is being created
    #:  - 200: Available
    #:  - 300: Unavailable
    status = resource.Body('status')
    #: Subnetwork ID (read only)
    subnet_id = resource.Body('subnetId')
    #: Cluster update time
    updated_at = resource.Body('updated')

    def _action(self, session, action, body=None):
        """Preform actions given the message body.
        """
        url = utils.urljoin(self.base_path, self.id, action)
        return session.post(url, json=body)

    def restart(self, session):
        """Restart the cluster.
        """
        res = self._action(session, 'restart')
        self._translate_response(res)
        return self

    def expand(self, session, new_size):
        """Expand cluster capacity.
        """
        if not 1 < new_size <= 32:
            raise exceptions.SDKException('CSS Cluster size can be [1..32]')
        res = self._action(session, 'extend',
                           {'grow': {'modifySize': new_size}})
        self._translate_response(res)
        return self
