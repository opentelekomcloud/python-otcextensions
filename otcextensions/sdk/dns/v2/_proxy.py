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
from otcextensions.sdk import sdk_proxy
from otcextensions.sdk.dns.v2 import nameserver as _ns
from otcextensions.sdk.dns.v2 import ptr as _ptr
from otcextensions.sdk.dns.v2 import recordset as _rs
from otcextensions.sdk.dns.v2 import zone as _zone


class Proxy(sdk_proxy.Proxy):

    # ======== Zones ========
    def zones(self, **query):
        """Retrieve a generator of zones

        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.
            * `zone_type`: Zone Type
            * `marker`:  pagination marker
            * `limit`: pagination limit
            * `offset`: pagination offset

        :returns: A generator of zone
            :class:`~otcextensions.sdk.dns.v2.zone.Zone` instances
        """
        return self._list(_zone.Zone, paginated=True, **query)

    def create_zone(self, **attrs):
        """Create a new zone from attributes

        :param dict attrs: Keyword arguments which will be used to create
                           a :class:`~otcextensions.sdk.dns.v2.zone.Zone`,
                           comprised of the properties on the Zone class.
        :returns: The results of zone creation
        :rtype: :class:`~otcextensions.sdk.dns.v2.zone.Zone`
        """
        return self._create(_zone.Zone, prepend_key=False, **attrs)

    def get_zone(self, zone):
        """Get a zone

        :param zone: The value can be the ID of a zone
             or a :class:`~otcextensions.sdk.dns.v2.zone.Zone` instance.
        :returns: Zone instance
        :rtype: :class:`~otcextensions.sdk.dns.v2.zone.Zone`
        """
        return self._get(_zone.Zone, zone)

    def delete_zone(self, zone, ignore_missing=True):
        """Delete a zone

        :param zone: The value can be the ID of a zone
             or a :class:`~otcextensions.sdk.dns.v2.zone.Zone` instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the zone does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent zone.

        :returns: Zone been deleted
        :rtype: :class:`~otcextensions.sdk.dns.v2.zone.Zone`
        """
        return self._delete(_zone.Zone, zone, ignore_missing=ignore_missing)

    def update_zone(self, zone, **attrs):
        """Update zone attributes

        :param zone: The id or an instance of
            :class:`~otcextensions.sdk.dns.v2.zone.Zone`
        :param dict attrs: attributes for update on
            :class:`~otcextensions.sdk.dns.v2.zone.Zone`

        :rtype: :class:`~otcextensions.sdk.dns.v2.zone.Zone`
        """
        return self._update(_zone.Zone, zone, **attrs)

    def find_zone(self, name_or_id, ignore_missing=True):
        """Find a single zone

        :param name_or_id: The name or ID of a zone
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the zone does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent zone.

        :returns: ``None``
        """
        return self._find(_zone.Zone, name_or_id,
                          ignore_missing=ignore_missing)

    def add_router_to_zone(self, zone, **router):
        """Add router(VPC) to private zone

        :param zone: The value can be the ID of a zone
             or a :class:`~otcextensions.sdk.dns.v2.zone.Zone` instance.
        :returns: updater instance of
            :class:`~otcextensions.sdk.dns.v2.zone.Router`
        :rtype: :class:`~otcextensions.sdk.dns.v2.zone.Router`
        """
        zone = self._get_resource(_zone.Zone, zone)
        return zone.associate_router(self, **router)

    def remove_router_from_zone(self, zone, **router):
        """Remove router(VPC) from private zone

        :param zone: The value can be the ID of a zone
             or a :class:`~otcextensions.sdk.dns.v2.zone.Zone` instance.
        :returns: updater instance of
            :class:`~otcextensions.sdk.dns.v2.zone.Router`
        :rtype: :class:`~otcextensions.sdk.dns.v2.zone.Router`
        """
        zone = self._get_resource(_zone.Zone, zone)
        return zone.disassociate_router(self, **router)

    # ======== Nameservers ========
    def nameservers(self, zone):
        """list nameservers of Zone

        :param zone: The value can be the ID of a zone
             or a :class:`~otcextensions.sdk.dns.v2.zone.Zone` instance.
        :returns: list of `otcextensions.sdk.dns.v2.nameserver.NameServer`
            instance
        :rtype: :class:`~otcextensions.sdk.dns.v2.nameserver.NameServer`
        """
        instance = self._get_resource(_zone.Zone, zone)
        return self._list(_ns.NameServer, paginated=False,
                          zone_id=instance.id)

    # ======== Recordsets ========
    def recordsets(self, zone, **query):
        """Retrieve a generator of recordsets which belongs to `zone`

        :param zone: The optional value can be the ID of a zone
             or a :class:`~otcextensions.sdk.dns.v2.zone.Zone` instance.
        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.
            * `marker`:  pagination marker
            * `limit`: pagination limit

        :returns: A generator of zone
            (:class:`~otcextensions.sdk.dns.v2.recordset.Recordset`) instances
        """
        if zone:
            zone = self._get_resource(_zone.Zone, zone)
            resource_cls = _rs.ZoneRecordset
            query.update({'zone_id': zone.id})
        else:
            resource_cls = _rs.Recordset
        return self._list(resource_cls, paginated=True, **query)

    def create_recordset(self, zone, **attrs):
        """Create a new recordset in the zone

        :param zone: The value can be the ID of a zone
            or a :class:`~otcextensions.sdk.dns.v2.zone.Zone` instance.
        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.dns.v2.recordset.Recordset`,
            comprised of the properties on the Recordset class.
        :returns: The results of zone creation
        :rtype: :class:`~otcextensions.sdk.dns.v2.recordset.Recordset`
        """
        zone = self._get_resource(_zone.Zone, zone)
        attrs.update({'zone_id': zone.id})
        return self._create(_rs.ZoneRecordset, prepend_key=False, **attrs)

    def update_recordset(self, recordset, **attrs):
        """Update Recordset attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.dns.v2.recordset.Recordset`,
            comprised of the properties on the Recordset class.
        :returns: The results of zone creation
        :rtype: :class:`~otcextensions.sdk.dns.v2.recordset.Recordset`
        """
        return self._update(_rs.ZoneRecordset, recordset, **attrs)

    def get_recordset(self, zone, recordset):
        """Get a recordset

        :param zone: The value can be the ID of a zone
             or a :class:`~otcextensions.sdk.dns.v2.zone.Zone` instance.
        :returns: Recordset instance
        :rtype: :class:`~otcextensions.sdk.dns.v2.recordset.Recordset`
        """
        zone = self._get_resource(_zone.Zone, zone)
        return self._get(_rs.ZoneRecordset, zone_id=zone.id)

    def delete_recordset(self, recordset, ignore_missing=True):
        """Delete a zone

        :param zone: The value can be the ID of a zone
             or a :class:`~otcextensions.sdk.dns.v2.zone.Zone` instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the zone does not exist. When set to ``True``, no exception will
            be set when attempting to delete a nonexistent zone.

        :returns: Recordset instance been deleted
        :rtype: :class:`~otcextensions.sdk.dns.v2.recordset.Recordset`
        """
        return self._delete(_rs.ZoneRecordset, recordset,
                            ignore_missing=ignore_missing)

    # ======== PTR Records ========
    def ptrs(self, **query):
        """List FloatingIP PTR records

        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.
            * ``marker``:  pagination marker
            * ``limit``: pagination limit
        :returns: A generator of PTR
            :class:`~otcextensions.sdk.dns.v2.ptr.PTR` instances
        """
        return self._list(_ptr.PTR, paginated=True, **query)

    def create_ptr(self, region, floating_ip_id, **attrs):
        """Set FloatingIP PTR record

        :param region: project region
        :param floating_ip_id: floating ip id
        :param dict attrs: Keyword arguments which will be used to create
                           a :class:`~otcextensions.sdk.dns.v2.ptr.PTR`,
                           comprised of the properties on the PTR class.
        :returns: The results of zone creation
        :rtype: :class:`~otcextensions.sdk.dns.v2.ptr.PTR`
        """
        # concat `region:floating_ip_id` as id
        ptr_id = region + ':' + floating_ip_id
        attrs.update({'id': ptr_id})
        return self._update(_ptr.PTR, prepend_key=False, **attrs)

    def get_ptr(self, region, floating_ip_id):
        """Show FloatingIP's PTR record

        :param region: project region
        :param floating_ip_id: the PTR floating ip id
        :returns: PTR instance
        :rtype: :class:`~otcextensions.sdk.dns.v2.ptr.PTR`
        """
        # concat `region:floating_ip_id` as id
        ptr_id = region + ':' + floating_ip_id
        return self._get(_ptr.PTR, ptr_id)

    def restore_ptr(self, region, floating_ip_id):
        """Unset FloatingIP's PTR record

        :param region: project region
        :param floating_ip_id: floating ip id
        :returns: PTR instance been deleted
        :rtype: :class:`~otcextensions.sdk.dns.v2.ptr.PTR`
        """
        # concat `region:floating_ip_id` as id
        ptr_id = region + ':' + floating_ip_id
        return self._update(_ptr.PTR,
                            ptr_id,
                            prepend_key=False,
                            has_body=False,
                            ptrdname=None)
