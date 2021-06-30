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
from otcextensions.sdk.dns.v2 import nameserver as _ns
from otcextensions.sdk.dns.v2 import recordset as _rs
from otcextensions.sdk.dns.v2 import zone as _zone
from otcextensions.sdk.dns.v2 import floating_ip as _fip


class Proxy(proxy.Proxy):

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
        return self._list(_zone.Zone, **query)

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

    def find_zone(self, name_or_id, ignore_missing=True, **attrs):
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
                          ignore_missing=ignore_missing,
                          **attrs)

    def add_router_to_zone(self, zone, **router):
        """Add router(VPC) to private zone

        :param zone: The value can be the ID of a zone
             or a :class:`~otcextensions.sdk.dns.v2.zone.Zone` instance.
        :param router: The parameter router_id is mandatory
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
        :param router: The parameter router_id is mandatory
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
    def recordsets(self, zone=None, **query):
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
        base_path = None
        if not zone:
            base_path = '/recordsets'
        else:
            zone = self._get_resource(_zone.Zone, zone)
            query.update({'zone_id': zone.id})
        return self._list(_rs.Recordset, base_path=base_path, **query)

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
        return self._create(_rs.Recordset, prepend_key=False, **attrs)

    def update_recordset(self, recordset, **attrs):
        """Update Recordset attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.dns.v2.recordset.Recordset`,
            comprised of the properties on the Recordset class.
        :returns: The results of zone creation
        :rtype: :class:`~otcextensions.sdk.dns.v2.recordset.Recordset`
        """
        return self._update(_rs.Recordset, recordset, **attrs)

    def get_recordset(self, recordset, zone):
        """Get a recordset

        :param zone: The value can be the ID of a zone
             or a :class:`~otcextensions.sdk.dns.v2.zone.Zone` instance.
        :returns: Recordset instance
        :rtype: :class:`~otcextensions.sdk.dns.v2.recordset.Recordset`
        """
        zone = self._get_resource(_zone.Zone, zone)
        return self._get(_rs.Recordset, recordset, zone_id=zone.id)

    def delete_recordset(self, recordset, zone=None, ignore_missing=True):
        """Delete a zone

        :param recordset: The value can be the ID of a recordset
             or a :class:`~otcextensions.sdk.dns.v2.recordset.Recordset`
             instance.
        :param zone: The value can be the ID of a zone
             or a :class:`~otcextensions.sdk.dns.v2.zone.Zone` instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the zone does not exist. When set to ``True``, no exception will
            be set when attempting to delete a nonexistent zone.

        :returns: Recordset instance been deleted
        :rtype: :class:`~otcextensions.sdk.dns.v2.recordset.Recordset`
        """
        if zone:
            zone = self._get_resource(_zone.Zone, zone)
            recordset = self._get(
                _rs.Recordset, recordset, zone_id=zone.id)
        return self._delete(_rs.Recordset, recordset,
                            ignore_missing=ignore_missing)

    def find_recordset(self, zone, name_or_id, ignore_missing=True, **attrs):
        """Find a single recordset

        :param zone: The value can be the ID of a zone
             or a :class:`~otcextensions.sdk.dns.v2.zone.Zone` instance.
        :param name_or_id: The name or ID of a recordset
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the recordset does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent recordset.

        :returns: :class:`~otcextensions.sdk.dns.v2.recordset.Recordset`
        """
        zone = self._get_resource(_zone.Zone, zone)
        return self._find(_rs.Recordset, name_or_id,
                          ignore_missing=ignore_missing, zone_id=zone.id,
                          **attrs)

    # ======== FloatingIPs ========
    def floating_ips(self, **query):
        """Retrieve a generator of FloatingIP PTR records

        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.

            * `name`: Recordset Name field.
            * `type`: Type field.
            * `status`: Status of the recordset.
            * `ttl`: TTL field filter.
            * `description`: Recordset description field filter.

        :returns: A generator of floatingips
            (:class:`~otcextensions.sdk.dns.v2.floating_ip.FloatingIP`)
            instances
        """
        return self._list(_fip.FloatingIP, **query)

    def get_floating_ip(self, floating_ip):
        """Get a Floating IP

        :param floating_ip: The value can be the ID of a floating ip
             or a :class:`~otcextensions.sdk.dns.v2.floating_ip.FloatingIP`
             instance.
             The ID is in format "region_name:floatingip_id"
        :returns: FloatingIP instance.
        :rtype: :class:`~otcextensions.sdk.dns.v2.floating_ip.FloatingIP`
        """
        return self._get(_fip.FloatingIP, floating_ip)

    def set_floating_ip(self, floating_ip, **attrs):
        """Set a Floating IP PTR record

        :param floating_ip: the Floating IP ID

        :returns: FloatingIP PTR record.
        :rtype: :class:`~otcextensions.sdk.dns.v2.floating_ip.FloatingIP`
        """
        return self._update(_fip.FloatingIP, floating_ip, **attrs)

    def update_floating_ip(self, floating_ip, **attrs):
        """Update floating ip attributes

        :param floating_ip: The id or an instance of
            :class:`~otcextensions.sdk.dns.v2.fip.FloatingIP`.
        :param dict attrs: attributes for update on
            :class:`~otcextensions.sdk.dns.v2.fip.FloatingIP`.

        :rtype: :class:`~otcextensions.sdk.dns.v2.fip.FloatingIP`
        """
        return self._update(_fip.FloatingIP, floating_ip, **attrs)

    def unset_floating_ip(self, floating_ip):
        """Unset a Floating IP PTR record

        :param floating_ip: ID for the floatingip associated with the
            project.

        :returns: FloatingIP PTR record.
        :rtype: :class:`~otcextensions.sdk.dns.v2.floating_ip.FloatipgIP`
        """
        # concat `region:floating_ip_id` as id
        attrs = {'ptrdname': None}
        return self._update(_fip.FloatingIP, floating_ip, **attrs)

    def _get_cleanup_dependencies(self):
        # DNS may depend on floating ip
        return {
            'dns': {
                'before': ['network']
            }
        }

    def _service_cleanup(self, dry_run=True, client_status_queue=False,
                         identified_resources=None,
                         filters=None, resource_evaluation_fn=None):
        # Delete all public zones
        for obj in self.zones():
            self._service_cleanup_del_res(
                self.delete_zone,
                obj,
                dry_run=dry_run,
                client_status_queue=client_status_queue,
                identified_resources=identified_resources,
                filters=filters,
                resource_evaluation_fn=resource_evaluation_fn)
        # Delete all private zones
        for obj in self.zones(type='private'):
            self._service_cleanup_del_res(
                self.delete_zone,
                obj,
                dry_run=dry_run,
                client_status_queue=client_status_queue,
                identified_resources=identified_resources,
                filters=filters,
                resource_evaluation_fn=resource_evaluation_fn)
        # Unset all floatingIPs
        # NOTE: FloatingIPs are not cleaned when filters are set
        for obj in self.floating_ips():
            self._service_cleanup_del_res(
                self.unset_floating_ip,
                obj,
                dry_run=dry_run,
                client_status_queue=client_status_queue,
                identified_resources=identified_resources,
                filters=filters,
                resource_evaluation_fn=resource_evaluation_fn)
