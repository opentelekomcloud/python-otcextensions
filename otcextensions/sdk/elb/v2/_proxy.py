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

from openstack.load_balancer.v2 import _proxy

from otcextensions.sdk.elb.v2 import elb_certificate as _certificate


class Proxy(_proxy.Proxy):
    skip_discovery = True

    # ======== Certificate ========
    def create_certificate(self, **attrs):
        """Create a new certificate from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.elb.v2.elb_certificate.Certificate`,
            comprised of the properties on the Certificate class.

        :returns: The results of the Certificate Creation

        :rtype: :class:`~otcextensions.sdk.elb.v2.elb_certificate.Certificate`
        """
        return self._create(_certificate.Certificate, **attrs)

    def certificates(self, **query):
        """Return a generator of certificates

        :param dict query: Optional query parameters to be sent to limit
            the resources being returned.

        :returns: A generator of certificates objects.
        """
        return self._list(_certificate.Certificate, **query)

    def delete_certificate(self, certificate, ignore_missing=True):
        """Delete a certificate

        :param certificate: The value can be the ID of a ELB certificate or a
            :class:`~otcextensions.sdk.elb.v2.elb_certificate.Certificate`
             instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
             when the certificate does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent certificate.

        :returns: ``None``
        """
        return self._delete(_certificate.Certificate, certificate,
                            ignore_missing=ignore_missing)

    def get_certificate(self, certificate):
        """Get a single certificate

        :param certificate: The value can be the ID of a ELB certificate or a
            :class:`~otcextensions.sdk.elb.v2.elb_certificate.Certificate`
            instance.

        :returns: One :class:
        `~otcextensions.sdk.elb.v2.elb_certificate.Certificate`

        :raises: :class:`~openstack.exceptions.ResourceNotFound`
            when no resource can be found.
        """
        return self._get(_certificate.Certificate, certificate)

    def update_certificate(self, certificate, **attrs):
        """Update a certificate

        :param certificate: The value can be either the ID of a ELB certificate
         or a :class:`~otcextensions.sdk.elb.v2.elb_certificate.Certificate`
          instance.
        :param dict attrs: The attributes to update on the certificate
         represented by ``certificate``.

        :returns: The updated certificate.

        :rtype: :class:`~otcextensions.elb.v2.elb_certificate.Certificate`
        """
        return self._update(_certificate.Certificate, certificate, **attrs)

    def find_certificate(self, name_or_id, ignore_missing=False):
        """Find a single certificate

        :param name_or_id: The name or ID of a ELB certificate
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the certificate does not exist.
            When set to ``True``, no exception will be set when attempting
            to find a nonexistent certificate.

        :returns:
            One :class:`~otcextensions.sdk.elb.v2.elb_certificate.Certificate`
             or ``None``
        """
        return self._find(_certificate.Certificate, name_or_id,
                          ignore_missing=ignore_missing)
