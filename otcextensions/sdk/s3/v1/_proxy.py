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
import os
from urllib.parse import urlsplit

from otcextensions.sdk import sdk_proxy
from otcextensions.sdk.s3.v1.container import Container


class Proxy(sdk_proxy.Proxy):
    skip_discovery = True

    def get_container_endpoint(self, region):
        """Override to return mapped endpoint if override and region are set

        """
        split_url = urlsplit(self.get_endpoint())

        return (f'{split_url.scheme}://{split_url.netloc}'
                % {'region_name': region})

    def get_boto3_client(self, region_name):
        endpoint = self.get_container_endpoint(region_name)
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

    def create_container(self, container_name, region, **kwargs):
        """Create a new container from attributes

        :param container_name: Bucket to create
        :param region: String region to create bucket in, e.g., 'eu-de'
        :param kwargs: Could be ACL, GrantFullControl, GrantRead,
            GrantReadACP, GrantWrite, GrantWrite, ObjectLockEnabledForBucket,
            ObjectOwnership
        :returns: The results of container creation
        """
        s3_client = self.get_boto3_client(region)
        location = {'LocationConstraint': region}
        response = s3_client.create_bucket(Bucket=container_name,
                                           CreateBucketConfiguration=location,
                                           **kwargs)
        if response.get('ResponseMetadata'):
            if response.get('ResponseMetadata').get('HTTPStatusCode', None) == 200:
                container = Container.new()
                return container._translate_response(response)
        return response

    def get_container(self, container_name, region, **kwargs):
        """Get container

        :param container_name: Bucket to get
        :param region: Region , e.g., 'eu-de'
        :param kwargs: Additional params
        :returns: The result of container get
        """
        s3_client = self.get_boto3_client(region)
        response = s3_client.head_bucket(Bucket=container_name,
                                         **kwargs)
        if response.get('ResponseMetadata'):
            if response.get('ResponseMetadata').get('HTTPStatusCode', None) == 200:
                container = Container.new()
                return container._translate_response(response)
        return response

    def delete_container(self, container_name, region):
        """Delete a container

        :returns: ``None``
        """
        s3_client = self.get_boto3_client(region)
        response = s3_client.delete_bucket(Bucket=container_name)
        if response.get('ResponseMetadata'):
            if response.get('ResponseMetadata').get('HTTPStatusCode', None) == 204:
                container = Container.new()
                return container._translate_response(response)
        return response

    def get_container_acl(self, container_name, region, **kwargs):
        """Get bucket acl

        :param container_name: Bucket to create
        :param kwargs: Could be ExpectedBucketOwner- the account ID of the
            expected bucket owner.
        :param region: String region to create bucket in, e.g., 'eu-de'
        :returns: The results of container creation
        """
        s3_client = self.get_boto3_client(region)
        response = s3_client.get_bucket_acl(Bucket=container_name, **kwargs)
        if response.get('ResponseMetadata'):
            if response.get('ResponseMetadata').get('HTTPStatusCode', None) == 200:
                container = Container.new()
                return container._translate_response(response)
        return response

    def put_container_acl(self, container_name, region,
                          **kwargs):
        """Put acl to bucket

        :param container_name: Bucket to create
        :param acl: The canned ACL to apply to the bucket
        :param access_control_policy: Contains the elements that set the ACL
            permissions for an object per grantee.
        :param region: String region to create bucket in, e.g., 'eu-de'
        :param kwargs: Could be ACL, AccessControlPolicy, ChecksumAlgorithm,
            GrantFullControl, GrantRead, GrantReadACP, GrantWrite,
            GrantWriteACP, ExpectedBucketOwner
        :returns: The results of container creation
        """
        s3_client = self.get_boto3_client(region)
        bucket = s3_client.put_bucket_acl(Bucket=container_name,
                                          **kwargs)
        return bucket

    def put_container_policy(self, container_name, policy, region, **kwargs):
        """Apply policy to container

        :param container_name: Bucket name
        :param region: String region to create bucket in, e.g., 'eu-de'
        :param policy: The bucket policy as a JSON document.
        :param kwargs: Can be ChecksumAlgorithm, ConfirmRemoveSelfBucketAccess,
            ExpectedBucketOwner
        :returns: The results of operation
        """
        s3_client = self.get_boto3_client(region)
        response = s3_client.put_bucket_policy(Bucket=container_name,
                                               Policy=policy,
                                               **kwargs)
        if response.get('ResponseMetadata'):
            if response.get('ResponseMetadata').get('HTTPStatusCode', None) == 200:
                container = Container.new()
                return container._translate_response(response)
        return response

    def get_container_policy(self, container_name, region, **kwargs):
        """Get policy to container

        :param container_name: Bucket name
        :param region: String region to create bucket in, e.g., 'eu-de'
        :param kwargs: Can only be ExpectedBucketOwner
        :returns: The results of operation
        """
        s3_client = self.get_boto3_client(region)
        response = s3_client.get_bucket_policy(Bucket=container_name,
                                               **kwargs)
        if response.get('ResponseMetadata'):
            if response.get('ResponseMetadata').get('HTTPStatusCode', None) == 200:
                container = Container.new()
                return container._translate_response(response)
        return response

    def delete_container_policy(self, container_name, region, **kwargs):
        """Delete policy to container

        :param container_name: Bucket name
        :param region: String region to create bucket in, e.g., 'eu-de'
        :param kwargs: Can only be ExpectedBucketOwner
        :returns: The results of operation
        """
        s3_client = self.get_boto3_client(region)
        response = s3_client.delete_bucket_policy(Bucket=container_name,
                                               **kwargs)
        if response.get('ResponseMetadata'):
            if response.get('ResponseMetadata').get('HTTPStatusCode', None) == 204:
                container = Container.new()
                return container._translate_response(response)
        return response
