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
from otcextensions.sdk.vpc.v1 import vpc as _vpc
from openstack import proxy


class Proxy(proxy.Proxy):

    def _override_endpoint(self):
        endpoint = self.get_endpoint(service_type='network')
        setattr(self, 'endpoint_override', endpoint)

    # ======== VPC ========
    def create_vpc(self, **attrs):
        """Create a new vpc from attributes

            :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.vpc.v1.vpc.VPC`
        """
        self._override_endpoint()
        return self._create(_vpc.VPC, **attrs)

    def delete_vpc(self, vpc, ignore_missing=True):
        """Delete a VPC
            :param vpc: Specifies the VPC ID, which uniquely identifies the VPC
            :param bool ignore_missing: When set to ``False``
                :class:`~openstack.exceptions.ResourceNotFound` will be raised
                 when the VPC does not exist.
                When set to ``True``, no exception will be set when
                attempting to delete a nonexistent VPC.
            :returns: ``None``
        """
        # self._override_endpoint()
        return self._delete(_vpc.VPC, vpc,
                            ignore_missing=ignore_missing)

    def update_vpc(self, vpc, **attrs):
        """ Modify a VPC
            :param vpc: Specifies the VPC ID, which uniquely identifies the VPC
            :param dict attrs: Keyword arguments which will be used to modify
            a :class:`~otcextensions.sdk.vpc.v1.vpc.VPC`
        """
        return self._update(_vpc.VPC, vpc, **attrs)
