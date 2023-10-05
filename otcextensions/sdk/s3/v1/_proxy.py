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

    # ======== Objects ========

    def objects(self, container, region):
        """Copy an object.

        :param container: Container name
        :param key: Key of the object to get.
        """

        s3_client = self.get_boto3_client(region)
        response = s3_client.list_objects(
            Bucket=container
        )
        return response

    def upload_object(self, container, file_name, region, object_name=None):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param container: container to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        if object_name is None:
            object_name = os.path.basename(file_name)

        s3_client = self.get_boto3_client(region)
        response = s3_client.upload_file(file_name, container, object_name)
        return response

    def download_object(self, file_name, container, region, object_name=None):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param container: container to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        s3_client = self.get_boto3_client(region)
        with open('FILE_NAME', 'wb') as f:
            s3_client.download_fileobj('BUCKET_NAME', 'OBJECT_NAME', f)
        return

    def copy_object(self, container, copy_source, key, region):
        """Copy an object.

        :param container: Container name
        :param copy_source: The name of the source bucket.
        :param key: The key of the destination object.
        """

        s3_client = self.get_boto3_client(region)
        response = s3_client.copy_object(
            Bucket=container,
            CopySource=copy_source,
            Key=key,
        )
        return response

    def objects(self, **query):
        """Obtain Container objects for this account.

        :param kwargs query: Optional query parameters to be sent to limit
                                 the resources being returned.

        :returns: List of containers
        """
        region_name = 'eu-ch2'
        s3_client = self.get_boto3_client(region_name)
        buckets = s3_client.list_buckets()
        return buckets

    def get_object(self, container, key, region):
        """Copy an object.

        :param container: Container name
        :param key: Key of the object to get.
        """

        s3_client = self.get_boto3_client(region)
        response = s3_client.get_object(
            Bucket=container,
            Key=key,
        )
        return response

    def delete_container(self, name, region):
        """Delete a container

        :returns: ``None``
        """
        s3_client = self.get_boto3_client(region)
        response = s3_client.delete_bucket(Bucket=name)
        return response
