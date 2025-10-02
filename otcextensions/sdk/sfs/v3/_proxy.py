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
from openstack import proxy
from otcextensions.common.utils import extract_region_from_url
from otcextensions.sdk import ak_auth
from otcextensions.sdk.sfs.v3 import file_system as _file_system
from urllib.parse import urlsplit


class Proxy(proxy.Proxy):
    skip_discovery = True

    def _get_request_auth(self, host=None):
        auth = getattr(self, '_ak_auth', None)
        if not auth:
            ak = None
            sk = None
            token = None
            conn = self.session._sdk_connection
            if hasattr(conn, 'get_ak_sk'):
                aksk = conn.get_ak_sk(conn)
                if len(aksk) == 2:
                    (ak, sk) = aksk
                elif len(aksk) == 3:
                    (ak, sk, token) = aksk
            if not (ak and sk):
                self.log.error('Cannot obtain AK/SK from config')
                return None
            region = extract_region_from_url(self.get_endpoint())
            if not host:
                host = self.get_endpoint()
            auth_params = {
                "access_key": ak,
                "secret_access_key": sk,
                "host": host,
                "region": region,
                "service": "s3"
            }
            if token:
                auth_params["token"] = token
            auth = ak_auth.AKRequestsAuth(**auth_params)
            setattr(self, '_ak_auth', auth)
        return auth

    # def get_container_endpoint(self, container):
    #     """Override to return mapped endpoint if override and region are set
    #
    #     """
    #     split_url = urlsplit(self.get_endpoint())
    #
    #     return f'{split_url.scheme}://%(container)s.{split_url.netloc}' % \
    #         {'container': container}

    def file_systems(self, **query):
        """List all file systems

        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.

        :returns: A generator of file system instances.
        :rtype: :class:`~otcextensions.sdk.sfs.v3.file_system.FileSystem`
        """
        return self._list(_file_system.FileSystem,
                          requests_auth=self._get_request_auth(),
                          **query
                          )