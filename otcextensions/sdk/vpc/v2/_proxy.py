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
from otcextensions.sdk.vpc.v2 import peering as _peering

from openstack import proxy


class Proxy(proxy.Proxy):

    def _override_endpoint(self):
        endpoint = self.get_endpoint(service_type='network')
        setattr(self, 'endpoint_override', endpoint)

    # ======== Peering ========
    def create_peering(self, **attrs):
        """Create a new vpc peering from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.vpc.v2.peering.Peering`
        """
        return self._create(_peering.Peering, **attrs)

    def delete_peering(self, peering, ignore_missing=True):
        """Delete a vpc peering

        :param peering: key id or an instance of
            :class:`~otcextensions.sdk.vpc.v2.peering.Peering`
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the vpc peering does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent peering.

        :returns: ``None``
        """
        self._override_endpoint()
        return self._delete(_peering.Peering, peering,
                            ignore_missing=ignore_missing)

    def peerings(self, **query):
        """Return a generator of vpc peerings

        :param dict query: Optional query parameters to be sent to limit
            the resources being returned.

        :returns: A generator of vpc peering objects

        :rtype: :class:`~otcextensions.sdk.vpc.v2.peering.Peering`
        """
        self._override_endpoint()
        return self._list(_peering.Peering, **query)

    def get_peering(self, peering):
        """Get a single vpc peering

        :param peering: The value can be the ID of a vpc peering or a
                        :class:`~otcextensions.sdk.vpc.v2.peering.Peering`
                        instance.

        :returns: One :class:`~otcextensions.sdk.vpc.v2.peering.Peering`

        :raises: :class:`~openstack.exceptions.ResourceNotFound`
                 when no resource can be found.
        """
        self._override_endpoint()
        return self._get(_peering.Peering, peering)

    def find_peering(self, name_or_id, ignore_missing=False):
        """Find a single vpc peering

        :param name_or_id: The name or ID of a zone
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the vpc peering does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent peering.

        :returns: One :class:`~otcextensions.sdk.vpc.v2.peering.Peering`
        """
        self._override_endpoint()
        return self._find(_peering.Peering, name_or_id,
                          ignore_missing=ignore_missing)

    def update_peering(self, peering, **attrs):
        """Update a vpc peering

        :param peering: Either the ID of a vpc peering or a
                       :class:`~otcextensions.sdk.vpc.v2.peering.Peering`
                       instance.
        :param dict attrs: The attributes to update on the vpc peering
            represented by ``peering``.

        :returns: The updated peering

        :rtype: :class:`~otcextensions.sdk.vpc.v2.peering.Peering`
        """
        self._override_endpoint()
        return self._update(_peering.Peering, peering, **attrs)

    def set_peering(self, peering, set_status):
        """Accept/Reject a vpc peering connection request

        :param peering: Either the ID of a vpc peering or a
                       :class:`~otcextensions.sdk.vpc.v2.peering.Peering`
                       instance.
        :param set_status: The value can been ``accept`` or ``reject``

        :returns: The updated peering

        :rtype: :class:`~otcextensions.sdk.vpc.v2.peering.Peering`
        """
        valid_status = ['accept', 'reject']
        if set_status.lower() not in valid_status:
            raise ValueError(
                "results: status must be one of %r." % valid_status)
        peering = self._get_resource(_peering.Peering, peering)
        self._override_endpoint()
        return peering._set_peering(self, set_status.lower())
