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
from otcextensions.sdk.waf.v1 import domain as _domain


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

    # ======== Domains ========
    def domains(self, **query):
        """Retrieve a generator of domains

        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.
            * `limit`: pagination limit
            * `offset`: pagination offset
            * `name`: domain name (hostname)
            * `policy_name`: policy name

        :returns: A generator of domain
            :class:`~otcextensions.sdk.waf.v1.domain.Domain`
            instances
        """
        return self._list(_domain.Domain, **query)

    def create_domain(self, **attrs):
        """Upload domain from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.waf.v1.domain.Domain`,
            comprised of the properties on the Domain class.
        :returns: The results of domain creation
        :rtype: :class:`~otcextensions.sdk.waf.v1.domain.Domain`
        """
        return self._create(_domain.Domain, prepend_key=False, **attrs)

    def get_domain(self, domain):
        """Get a domain

        :param domain: The value can be the ID of a domain
             or a :class:`~otcextensions.sdk.waf.v1.domain.Domain`
             instance.
        :returns: Domain instance
        :rtype: :class:`~otcextensions.sdk.waf.v1.domain.Domain`
        """
        return self._get(_domain.Domain, domain)

    def delete_domain(self, domain, ignore_missing=True):
        """Delete a domain

        :param domain: The value can be the ID of a domain
             or a :class:`~otcextensions.sdk.waf.v1.domain.Domain`
             instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the domain does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent domain.

        :returns: Domain been deleted
        :rtype: :class:`~otcextensions.sdk.waf.v1.domain.Domain`
        """
        return self._delete(_domain.Domain, domain,
                            ignore_missing=ignore_missing)

    def update_domain(self, domain, **attrs):
        """Update domain attributes

        :param domain: The id or an instance of
            :class:`~otcextensions.sdk.waf.v1.domain.Domain`
        :param dict attrs: attributes for update on
            :class:`~otcextensions.sdk.waf.v1.domain.Domain`

        :rtype: :class:`~otcextensions.sdk.waf.v1.domain.Domain`
        """
        return self._update(_domain.Domain, domain, **attrs)

    def find_domain(self, name_or_id, ignore_missing=True, **attrs):
        """Find a single domain

        :param name_or_id: The name or ID of a domain
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the domain does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent domain.

        :returns: ``None``
        """
        return self._find(_domain.Domain, name_or_id,
                          ignore_missing=ignore_missing,
                          **attrs)

    # ======== Project cleanup ========
    def _get_cleanup_dependencies(self):
        return {
            'waf': {
                'before': []
            }
        }

    def _service_cleanup(self, dry_run=True, client_status_queue=None,
                         identified_resources=None,
                         filters=None, resource_evaluation_fn=None):
        for obj in self.domains():
            self._service_cleanup_del_res(
                self.delete_domain,
                obj,
                dry_run=dry_run,
                client_status_queue=client_status_queue,
                identified_resources=identified_resources,
                filters=filters,
                resource_evaluation_fn=resource_evaluation_fn)

        for obj in self.certificates():
            self._service_cleanup_del_res(
                self.delete_certificate,
                obj,
                dry_run=dry_run,
                client_status_queue=client_status_queue,
                identified_resources=identified_resources,
                filters=filters,
                resource_evaluation_fn=resource_evaluation_fn)
