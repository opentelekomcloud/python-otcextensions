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
import boto3
from otcextensions.sdk import sdk_proxy


class Proxy(sdk_proxy.Proxy):
    skip_discovery = True

    CONTAINER_ENDPOINT_EU_DE = \
        'https://obs.%(region_name)s.otc.t-systems.com'

    CONTAINER_ENDPOINT_EU_CH2 = \
        'https://obs.%(region_name)s.sc.otc.t-systems.com'

    def get_boto3_client(self, region_name):
        if region_name == 'eu-ch2':
            endpoint = self.CONTAINER_ENDPOINT_EU_CH2 % {
                'region_name': region_name
            }
        if region_name == 'eu-de':
            endpoint = self.CONTAINER_ENDPOINT_EU_DE % {
                'region_name': region_name
            }
            ak, sk = self._set_ak_sk_keys()
        s3_client = boto3.client(
            service_name='s3',
            endpoint_url=endpoint,
            aws_access_key_id=ak,
            aws_secret_access_key=sk,

        )
        return s3_client

    def _set_ak_sk_keys(self):
        conn = self.session._sdk_connection
        if hasattr(conn, 'get_ak_sk'):
            (ak, sk) = conn.get_ak_sk(conn)
        if not (ak and sk):
            self.log.error('Cannot obtain AK/SK from config')
            return None
        return ak, sk

    # ======== Containers ========

    def containers(self, **query):
        """Obtain Container objects for this account.

        :param kwargs query: Optional query parameters to be sent to limit
                                 the resources being returned.

        :returns: List of containers
        """
        region_name = 'eu-ch2'
        s3_client = self.get_boto3_client(region_name)
        buckets = s3_client.list_buckets()
        return buckets

    def create_container(self, name, region_name):
        """Create a new container from attributes

        :param name: Bucket to create
        :param region: String region to create bucket in, e.g., 'eu-de'
        :returns: The results of container creation
        """
        s3_client = self.get_boto3_client(region_name)
        location = {'LocationConstraint': region_name}
        bucket = s3_client.create_bucket(Bucket=name,
                                         CreateBucketConfiguration=location)
        return bucket

    def delete_container(self, name, region):
        """Delete a container

        :returns: ``None``
        """
        s3_client = self.get_boto3_client(region)
        response = s3_client.delete_bucket(Bucket=name)
        return response
