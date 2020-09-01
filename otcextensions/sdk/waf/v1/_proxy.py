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

from otcextensions.sdk.waf.v1 import certificate as _cert


class Proxy(proxy.Proxy):

    skip_discovery = True

    def __init__(self, session, *args, **kwargs):
        super(Proxy, self).__init__(session=session, *args, **kwargs)
        self.endpoint_override = \
            '%s/%s/%s' % (
                self.get_endpoint(),
                'v1',
                '%(project_id)s')
        self.additional_headers = {
            'x-request-source-type': 'ApiCall',
            'content-type': 'application/json'
        }

    # ======== Certificates ========
    def certificates(self, **query):
        """Retrieve a generator of certificates

        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.
            * `limit`: pagination limit
            * `offset`: pagination offset

        :returns: A generator of certificate
            :class:`~otcextensions.sdk.waf.v1.certificate.Certificate`
            instances
        """
        return self._list(_cert.Certificate, **query)

    def create_certificate(self, **attrs):
        """Upload certificate from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.waf.v1.certificate.Certificate`,
            comprised of the properties on the Certificate class.
        :returns: The results of certificate creation
        :rtype: :class:`~otcextensions.sdk.waf.v1.certificate.Certificate`
        """
        print(attrs)
        return self._create(_cert.Certificate, prepend_key=False, **attrs)

    def get_certificate(self, certificate):
        """Get a certificate

        :param certificate: The value can be the ID of a certificate
             or a :class:`~otcextensions.sdk.waf.v1.certificate.Certificate`
             instance.
        :returns: Certificate instance
        :rtype: :class:`~otcextensions.sdk.waf.v1.certificate.Certificate`
        """
        return self._get(_cert.Certificate, certificate)

    def delete_certificate(self, certificate, ignore_missing=True):
        """Delete a certificate

        :param certificate: The value can be the ID of a certificate
             or a :class:`~otcextensions.sdk.waf.v1.certificate.Certificate`
             instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the certificate does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent certificate.

        :returns: Certificate been deleted
        :rtype: :class:`~otcextensions.sdk.waf.v1.certificate.Certificate`
        """
        return self._delete(_cert.Certificate, certificate,
                            ignore_missing=ignore_missing)

    def update_certificate(self, certificate, **attrs):
        """Update certificate attributes

        :param certificate: The id or an instance of
            :class:`~otcextensions.sdk.waf.v1.certificate.Certificate`
        :param dict attrs: attributes for update on
            :class:`~otcextensions.sdk.waf.v1.certificate.Certificate`

        :rtype: :class:`~otcextensions.sdk.waf.v1.certificate.Certificate`
        """
        return self._update(_cert.Certificate, certificate, **attrs)

    def find_certificate(self, name_or_id, ignore_missing=True, **attrs):
        """Find a single certificate

        :param name_or_id: The name or ID of a certificate
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the certificate does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent certificate.

        :returns: ``None``
        """
        return self._find(_cert.Certificate, name_or_id,
                          ignore_missing=ignore_missing,
                          **attrs)
