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
import copy
from urllib.parse import urljoin
from urllib.parse import urlsplit

from keystoneauth1.identity import v3 as identity_v3
from openstack import proxy
from otcextensions.sdk.ccn.v3 import quota as _quota


class Proxy(proxy.Proxy):

    skip_discovery = True

    @staticmethod
    def _domain_id(access):
        return access.domain_id or access.project_domain_id or access.user_domain_id

    def _domain_proxy(self, domain_id=None):
        auth = self.auth or self.session.auth
        current_domain_id = self._domain_id(auth.get_access(self.session))
        if domain_id is None:
            domain_id = current_domain_id
        if not domain_id:
            raise ValueError("A domain ID is required for CCN requests.")
        if domain_id == current_domain_id:
            return self, domain_id
        scoped_proxy = copy.copy(self)
        scoped_proxy._domain_scope_id = domain_id
        return scoped_proxy, domain_id

    def request(self, url, method, *args, **kwargs):
        auth = kwargs.get("auth") or self.auth or self.session.auth
        access = auth.get_access(self.session)
        domain_id = getattr(self, "_domain_scope_id", None) or self._domain_id(access)
        if not access.domain_scoped:
            if not domain_id:
                raise ValueError("A domain ID is required for CCN requests.")
            cached = getattr(self, "_domain_auth_cache", None)
            if (
                cached is None
                or cached[0] != access.auth_token
                or cached[1] != domain_id
            ):
                domain_auth = identity_v3.Token(
                    auth_url=auth.auth_url,
                    token=access.auth_token,
                    domain_id=domain_id,
                )
                cached = (access.auth_token, domain_id, domain_auth)
                self._domain_auth_cache = cached
            kwargs["auth"] = cached[2]
        if not urlsplit(url).netloc:
            endpoint = kwargs.get("endpoint_override") or self.get_endpoint()
            if urlsplit(url).path.startswith("/v3/"):
                url = urljoin(endpoint, url)
            else:
                if not domain_id:
                    raise ValueError("A domain ID is required for CCN requests.")
                url = urljoin(endpoint, f"/v3/{domain_id}/{url.lstrip('/')}")
        return super().request(url, method, *args, **kwargs)

    def central_network_quotas(self, domain_id=None, **query):
        """List central network resource quotas.

        :param domain_id: Account domain ID. If omitted, the current
            authentication domain is used.
        :param query: Optional API query parameters: ``quota_type``,
            ``limit``, and ``marker``.
        The API requires a domain-scoped token. Project-scoped Keystone tokens
        are exchanged for a domain-scoped token without changing the session.
        :returns: A generator of quota resources.
        :rtype: :class:`~otcextensions.sdk.ccn.v3.quota.Quota`
        """
        scoped_proxy, domain_id = self._domain_proxy(domain_id)
        base_path = urljoin(self.get_endpoint(), _quota.Quota.base_path)
        return scoped_proxy._list(
            _quota.Quota, base_path=base_path, domain_id=domain_id, **query
        )
