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
from openstack import exceptions
from email.utils import formatdate
import requests


class FileSystem(resource.Resource):
    allow_list = True
    allow_create = True
    allow_delete = True

    create_method = 'PUT'

    base_path = '/'

    az_redundancy = resource.Header("x-obs-az-redundancy")
    bucket_type = resource.Header("x-obs-bucket-type")

    @classmethod
    def list(cls, session, paginated=False,
             endpoint_override=None, headers=None, requests_auth=None,
             **params):
        if not cls.allow_list:
            raise exceptions.MethodNotSupported(cls, "list")
        # cls._query_mapping._validate(params, base_path=cls.base_path)
        query_params = cls._query_mapping._transpose(params, cls)
        ep = session.get_endpoint(service_type="sfs", interface="public")
        url = "https://sfs.eu-de.otc.t-systems.com/"
        headers = {
            "x-obs-bucket-type": "SFS"
        }
        requests_auth.aws_host = url
        session.endpoint_override = endpoint_override
        response = session.get(
            url,
            requests_auth=requests_auth,
            headers=headers,
            params=query_params
        )

        exceptions.raise_from_response(response)