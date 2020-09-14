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
from urllib.parse import urlparse

from openstack.utils import urljoin

from openstack.identity.v3 import _proxy

from otcextensions.sdk.identity.v3 import credential as _credential


class Proxy(_proxy.Proxy):

    def __init__(self, session, *args, **kwargs):
        super(Proxy, self).__init__(session=session, *args, **kwargs)
        self._credentials_base = None

    def _get_credentials_endpoint(self):
        if not self._credentials_base:
            identity_url = self.get_endpoint_data().url
            parsed_domain = urlparse(identity_url)
            self._credentials_base = '%s://%s' % (parsed_domain.scheme,
                                                  parsed_domain.netloc)
        return self._credentials_base

    # ========== Credentials ==========
    def credentials(self, **attrs):
        """Retrieve a generator of credentials

        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.
            * `user_id`: user_id

        :returns: A generator of credentials
            :class:`~otcextensions.sdk.identity.v3.credential.Credential`
            instances
        """
        # for list we need to pass corrected endpoint
        base = self._get_credentials_endpoint()
        base_path = urljoin(base, _credential.Credential.base_path)
        return self._list(_credential.Credential, base_path=base_path,
                          **attrs)

    def create_credential(self, **attrs):
        """Create a new credential from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.identity.v3.credential.Credential`,
            comprised of the properties on the Credential class.
        :returns: The results of credential creation
        :rtype: :class:`~otcextensions.sdk.identity.v3.credential.Credential`
        """
        return self._create(_credential.Credential, prepend_key=True,
                            **attrs)

    def get_credential(self, credential):
        """Get a credential

        :param credential: The value can be the ID of a credential
            or a :class:`~otcextensions.sdk.identity.v3.credential.Credential`
            instance.
        :returns: Credential instance
        :rtype: :class:`~otcextensions.sdk.identity.v3.credential.Credential`
        """
        return self._get(_credential.Credential, credential)

    def find_credential(self, name_or_id, ignore_missing=True, **attrs):
        """Find a single credential

        :param name_or_id: The name or ID of a credential
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the credential does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent credential.

        :returns: ``None``
        """
        return self._find(_credential.Credential, name_or_id,
                          ignore_missing=ignore_missing,
                          **attrs)

    def delete_credential(self, credential, ignore_missing=True):
        """Delete a credential

        :param credential: The value can be the ID of a credential
            or a :class:`~otcextensions.sdk.identity.v3.credential.Credential`
            instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the credential does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent credential.

        :returns: Credential been deleted
        :rtype: :class:`~otcextensions.sdk.identity.v3.credential.Credential`
        """
        return self._delete(_credential.Credential,
                            credential,
                            ignore_missing=ignore_missing)

    def update_credential(self, credential, **attrs):
        """Update credential attributes

        :param credential: The id or an instance of
            :class:`~otcextensions.sdk.identity.v3.credential.Credential`
        :param dict attrs: attributes for update on
            :class:`~otcextensions.sdk.identity.v3.credential.Credential`

        :rtype: :class:`~otcextensions.sdk.identity.v3.credential.Credential`
        """
        return self._update(_credential.Credential, credential, **attrs)
