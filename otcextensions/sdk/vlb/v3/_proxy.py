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
from openstack import resource

from otcextensions.sdk.vlb.v3 import availability_zone as _availability_zone
from otcextensions.sdk.vlb.v3 import certificate as _certificate
from otcextensions.sdk.vlb.v3 import flavor as _flavor
from otcextensions.sdk.vlb.v3 import health_monitor as _hm
from otcextensions.sdk.vlb.v3 import ip_address_group as _ip_address_group
from otcextensions.sdk.vlb.v3 import l7_policy as _l7policy
from otcextensions.sdk.vlb.v3 import l7_rule as _l7rule
from otcextensions.sdk.vlb.v3 import listener as _listener
from otcextensions.sdk.vlb.v3 import load_balancer as _lb
from otcextensions.sdk.vlb.v3 import load_balancer_status as _lb_statuses
from otcextensions.sdk.vlb.v3 import member as _member
from otcextensions.sdk.vlb.v3 import pool as _pool
from otcextensions.sdk.vlb.v3 import quota as _quota


class Proxy(proxy.Proxy):
    skip_discovery = True

    # ======== Load balancer ========
    def create_load_balancer(self, **attrs):
        """Create a new load balancer from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.vlb.v3.
            load_balancer.LoadBalancer`, comprised of the properties on the
            LoadBalancer class.

        :returns: The results of load balancer creation
        :rtype: :class:`~otcextensions.sdk.vlb.v3.load_balancer.LoadBalancer`
        """
        return self._create(_lb.LoadBalancer, **attrs)

    def get_load_balancer(self, *attrs):
        """Get a load balancer

        :param load_balancer: The value can be the name of a load balancer
             or :class:`~otcextensions.sdk.vlb.v3.load_balancer.LoadBalancer`
             instance.

        :returns: One
             :class:`~otcextensions.sdk.vlb.v3.load_balancer.LoadBalancer`
        """
        return self._get(_lb.LoadBalancer, *attrs)

    def get_load_balancer_statistics(self, name_or_id):
        """Get the load balancer statistics

        :param name_or_id: The name or ID of a load balancer

        :returns: One :class:`~otcextensions.sdk.vlb.v3.load_balancer.
                  LoadBalancerStats`
        """
        return self._get(_lb.LoadBalancerStats, lb_id=name_or_id,
                         requires_id=False)

    def load_balancers(self, **query):
        """Retrieve a generator of load balancers

        :returns: A generator of load balancer instances
        """
        return self._list(_lb.LoadBalancer, **query)

    def delete_load_balancer(self, load_balancer, ignore_missing=True):
        """Delete a load balancer

        :param load_balancer: The load_balancer can be either the name or a
            :class:`~otcextensions.sdk.vlb.v3.load_balancer.LoadBalancer`
            instance
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the load balancer does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent load balancer.

        :returns: ``None``
        """
        # load_balancer = self._get_resource(_lb.LoadBalancer, load_balancer)
        return self._delete(_lb.LoadBalancer, load_balancer,
                            ignore_missing=ignore_missing)

    def find_load_balancer(self, name_or_id, ignore_missing=True):
        """Find a single load balancer

        :param name_or_id: The name or ID of a load balancer
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the load balancer does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent load balancer.

        :returns: ``None``
        """
        return self._find(_lb.LoadBalancer, name_or_id,
                          ignore_missing=ignore_missing)

    def update_load_balancer(self, load_balancer, **attrs):
        """Update a load balancer

        :param load_balancer: The load_balancer can be either the name or a
            :class:`~otcextensions.sdk.vlb.v3.load_balancer.LoadBalancer`
            instance
        :param dict attrs: The attributes to update on the load balancer
                           represented by ``load_balancer``.

        :returns: The updated load_balancer
        :rtype: :class:`~otcextensions.sdk.vlb.v3.load_balancer.LoadBalancer`
        """
        return self._update(_lb.LoadBalancer, load_balancer, **attrs)

    def wait_for_load_balancer(self, name_or_id, status='ACTIVE',
                               failures=['ERROR'], interval=2, wait=300):
        lb = self._find(_lb.LoadBalancer, name_or_id, ignore_missing=False)

        return resource.wait_for_status(self, lb, status, failures, interval,
                                        wait, attribute='provisioning_status')

    def get_load_balancer_statuses(self, loadbalancer_id):
        """Get specific load balancer statuses by load balancer id.

        :param loadbalancer_id: The load balancer id
        :returns: The status of load balancer
        :rtype:
            :class:
            `~otcextensions.sdk.vlb.v3.load_balancer_status.LoadBalancerStatus`
        """
        return self._get(
            _lb_statuses.LoadBalancerStatus,
            requires_id=False,
            loadbalancer_id=loadbalancer_id
        )

    # ======== Listener ========
    def create_listener(self, **attrs):
        """Create a new listener from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.vlb.v3.
            listener.Listener`, comprised of the properties on the
            Listener class.

        :returns: The results of listener creation
        :rtype: :class:`~otcextensions.sdk.vlb.v3.listener.Listener`
        """
        return self._create(_listener.Listener, **attrs)

    def delete_listener(self, listener, ignore_missing=True):
        """Delete a listener

        :param listener: The value can be either the ID of a listner or a
               :class:`~otcextensions.sdk.vlb.v3.listener.Listener` instance.
        :param bool ignore_missing: When set to ``False``
                    :class:`~openstack.exceptions.ResourceNotFound` will be
                    raised when the listner does not exist.
                    When set to ``True``, no exception will be set when
                    attempting to delete a nonexistent listener.
        :returns: ``None``
        """
        self._delete(_listener.Listener, listener,
                     ignore_missing=ignore_missing)

    def update_listener(self, listener, **attrs):
        """Update a listener

        :param listener: Either the id of a listener or a
                      :class:`~otcextensions.sdk.vlb.v3.listener.Listener`
                      instance.
        :param dict attrs: The attributes to update on the listener
                           represented by ``listener``.
        :returns: The updated listener
        :rtype: :class:`~otcextensions.sdk.vlb.v3.listener.Listener`
        """
        return self._update(_listener.Listener, listener, **attrs)

    def find_listener(self, name_or_id, ignore_missing=True):
        """Find a single listener

        :param name_or_id: The name or ID of a listener.
        :param bool ignore_missing: When set to ``False``
                    :class:`~openstack.exceptions.ResourceNotFound` will be
                    raised when the resource does not exist.
                    When set to ``True``, None will be returned when
                    attempting to find a nonexistent resource.
        :returns: One :class:`~otcextensions.sdk.vlb.v3.listener.Listener`
         or None
        """
        return self._find(_listener.Listener, name_or_id,
                          ignore_missing=ignore_missing)

    def get_listener(self, listener):
        """Get a single listener

        :param listener: The value can be the ID of a listener or a
               :class:`~otcextensions.sdk.vlb.v3.listener.Listener`
               instance.
        :returns: One :class:`~otcextensions.sdk.vlb.v3.listener.Listener`
        :raises: :class:`~openstack.exceptions.ResourceNotFound`
                 when no resource can be found.
        """
        return self._get(_listener.Listener, listener)

    def listeners(self, **query):
        """Retrieve a generator of listeners

        :returns: A generator of listeners instances
        :rtype: :class:`~otcextensions.sdk.vlb.v3.listener.Listener`
        """
        return self._list(_listener.Listener, **query)

    # ======== Certificate ========
    def create_certificate(self, **attrs):
        """Create a new certificate from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.vlb.v3.certificate.Certificate`,
            comprised of the properties on the Certificate class.

        :returns: The results of the Certificate Creation
        :rtype: :class:`~otcextensions.sdk.vlb.v3.certificate.Certificate`
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
            :class:`~otcextensions.sdk.vlb.v3.certificate.Certificate`
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
            :class:`~otcextensions.sdk.vlb.v3.certificate.Certificate`
            instance.

        :returns: One :class:
            `~otcextensions.sdk.vlb.v3.certificate.Certificate`
        :raises: :class:`~openstack.exceptions.ResourceNotFound`
            when no resource can be found.
        """
        return self._get(_certificate.Certificate, certificate)

    def update_certificate(self, certificate, **attrs):
        """Update a certificate

        :param certificate: The value can be either the ID of a ELB certificate
            or a :class:`~otcextensions.sdk.vlb.v3.certificate.Certificate`
            instance.
        :param dict attrs: The attributes to update on the certificate
            represented by ``certificate``.
        :returns: The updated certificate.

        :rtype: :class:`~otcextensions.vlb.v3.certificate.Certificate`
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
            One :class:`~otcextensions.sdk.vlb.v3.certificate.Certificate`
            or ``None``
        """
        return self._find(_certificate.Certificate, name_or_id,
                          ignore_missing=ignore_missing)

    # ======== Quota ========
    def get_quotas(self):
        """Retrieve a quotas

        :returns: A quota instance
        :rtype: :class:`~otcextensions.sdk.vlb.v3.quota.Quota`
        """
        return _quota.Quota.get(self)

    # ======== Availability zone ========
    def availability_zones(self, **query):
        """Retrieve a generator of availability zones

        :returns: A AvailabilityZone instance
        :rtype: :class:`AvailabilityZone`
        """

        return self._list(_availability_zone.AvailabilityZone, **query)

    # ======= Flavor =======
    def flavors(self, **query):
        """List all load balancer flavors that are
        available to a specific user in a specific region.

        :param engine_name: database engine name
        :param region: region

        :returns: A generator of flavor
        :rtype: :class:`~otcextensions.sdk.vlb.v3.flavor.Flavor`
        """

        return self._list(
            _flavor.Flavor,
            **query
        )

    def get_flavor(self, flavor):
        """Get a single flavor

        :param flavor: The value can be either the ID of an flavor or a
            :class:`~otcextensions.sdk.vlb.v3.flavor.Flavor`.

        :returns: One :class:`~otcextensions.sdk.vlb.v3.flavor.Flavor`
        """
        return self._get(_flavor.Flavor, flavor)

    def find_flavor(self, name_or_id, ignore_missing=True):
        """Find a single flavor

        :param name_or_id: The name or ID of a flavor
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the flavor does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent flavor.

        :returns: ``None``
        """
        return self._find(_flavor.Flavor, name_or_id,
                          ignore_missing=ignore_missing)

    # ======= Pool =======
    def create_pool(self, **attrs):
        """Create a new pool from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.vlb.v3.pool.Pool`,
            comprised of the properties on the Pool class.

        :returns: The results of the Pool Creation
        :rtype: :class:`~otcextensions.sdk.vlb.v3.pool.Pool`
        """
        return self._create(_pool.Pool, **attrs)

    def get_pool(self, *attrs):
        """Get a single pool

        :param dict attrs: Keyword arguments which will be used to get a
            :class:`~otcextensions.sdk.vlb.v3.pool.Pool`
            instance.

        :returns: One :class:
            `~otcextensions.sdk.vlb.v3.pool.Pool`
        :raises: :class:`~openstack.exceptions.ResourceNotFound`
            when no resource can be found.
        """
        return self._get(_pool.Pool, *attrs)

    def pools(self, **query):
        """Return a generator of pool

        :param dict query: Optional query parameters to be sent to limit
            the resources being returned.
        :returns: A generator of pools objects.
        """
        return self._list(_pool.Pool, **query)

    def delete_pool(self, pool, ignore_missing=True):
        """Delete a pool

        :param pool: The value can be the ID of a ELB pool or a
            :class:`~otcextensions.sdk.vlb.v3.pool.Pool`
            instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the pool does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent pool.
        :returns: ``None``
        """
        return self._delete(_pool.Pool, pool,
                            ignore_missing=ignore_missing)

    def find_pool(self, name_or_id, ignore_missing=True):
        """Find a single pool

        :param name_or_id: The name or ID of a pool
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the pool does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent pool.
        :returns: ``None``
        """
        return self._find(_pool.Pool, name_or_id,
                          ignore_missing=ignore_missing)

    def update_pool(self, pool, **attrs):
        """Update a pool

        :param pool: The value can be either the ID of a ELB pool
            or a :class:`~otcextensions.sdk.vlb.v3.pool.Pool`
            instance.
        :param dict attrs: The attributes to update on the pool
            represented by ``pool``.
        :returns: The updated pool.

        :rtype: :class:`~otcextensions.vlb.v3.pool.Pool`
        """
        return self._update(_pool.Pool, pool, **attrs)

    # ======= Member =======
    def create_member(self, pool, **attrs):
        """Create a new member from attributes

        :param pool: The pool can be either the ID of a pool or a
            :class:`~otcextensions.sdk.vlb.v3.pool.Pool` instance
            that the member will be created in.
        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.vlb.v3.member.Member`,
            comprised of the properties on the Member class.
        :returns: The results of member creation
        :rtype: :class:`~otcextensions.sdk.vlb.v3.member.Member`
        """
        poolobj = self._get_resource(_pool.Pool, pool)
        return self._create(_member.Member, pool_id=poolobj.id,
                            **attrs)

    def delete_member(self, member, pool, ignore_missing=True):
        """Delete a member

        :param member:
            The member can be either the ID of a member or a
            :class:`~otcextensions.sdk.vlb.v3.member.Member` instance.
        :param pool: The pool can be either the ID of a pool or a
            :class:`~otcextensions.sdk.vlb.v3.pool.Pool` instance
            that the member belongs to.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be
            raised when the member does not exist.
            When set to ``True``, no exception will be set when
            attempting to delete a nonexistent member.
        :returns: ``None``
        """
        poolobj = self._get_resource(_pool.Pool, pool)
        self._delete(_member.Member, member,
                     ignore_missing=ignore_missing, pool_id=poolobj.id)

    def find_member(self, name_or_id, pool, ignore_missing=True):
        """Find a single member

        :param str name_or_id: The name or ID of a member.
        :param pool: The pool can be either the ID of a pool or a
            :class:`~otcextensions.sdk.vlb.v3.pool.Pool` instance
            that the member belongs to.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be
            raised when the resource does not exist.
            When set to ``True``, None will be returned when
            attempting to find a nonexistent resource.
        :returns: One :class:`~otcextensions.sdk.vlb.v3.member.Member`
            or None
        """
        poolobj = self._get_resource(_pool.Pool, pool)
        return self._find(_member.Member, name_or_id,
                          ignore_missing=ignore_missing, pool_id=poolobj.id)

    def get_member(self, member, pool):
        """Get a single member

        :param member: The member can be the ID of a member or a
            :class:`~openstack.load_balancer.v3.member.Member`
            instance.
        :param pool: The pool can be either the ID of a pool or a
            :class:`~otcextensions.sdk.vlb.v3.pool.Pool` instance
            that the member belongs to.
        :returns: One :class:`~otcextensions.sdk.vlb.v3.member.Member`
        :raises: :class:`~openstack.exceptions.ResourceNotFound`
            when no resource can be found.
        """
        poolobj = self._get_resource(_pool.Pool, pool)
        return self._get(_member.Member, member,
                         pool_id=poolobj.id)

    def members(self, pool, **query):
        """Return a generator of members

        :param pool: The pool can be either the ID of a pool or a
            :class:`~otcextensions.sdk.vlb.v3.pool.Pool` instance
            that the member belongs to.
        :param dict query: Optional query parameters to be sent to limit
            the resources being returned.
        :returns: A generator of member objects
        :rtype: :class:`~otcextensions.sdk.vlb.v3.member.Member`
        """
        poolobj = self._get_resource(_pool.Pool, pool)
        return self._list(_member.Member, pool_id=poolobj.id, **query)

    def update_member(self, member, pool, **attrs):
        """Update a member

        :param member: Either the ID of a member or a
            :class:`~otcextensions.sdk.vlb.v3.member.Member`
            instance.
        :param pool: The pool can be either the ID of a pool or a
            :class:`~otcextensions.sdk.vlb.v3.pool.Pool` instance
            that the member belongs to.
        :param dict attrs: The attributes to update on the member
            represented by ``member``.
        :returns: The updated member
        :rtype: :class:`~otcextensions.sdk.vlb.v3.member.Member`
        """
        poolobj = self._get_resource(_pool.Pool, pool)
        return self._update(_member.Member, member,
                            pool_id=poolobj.id, **attrs)

    # ======= HealthMonitor =======
    def find_health_monitor(self, name_or_id, ignore_missing=True):
        """Find a single health monitor

        :param str name_or_id: The name or ID of a health monitor.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be
            raised when the resource does not exist.
            When set to ``True``, None will be returned when
            attempting to find a nonexistent resource.
        :returns: One
            :class:`~otcextensions.sdk.vlb.v3.healthmonitor.HealthMonitor`
            or None
        :raises: :class:`openstack.exceptions.DuplicateResource` if more
            than one resource is found for this request.
        :raises: :class:`openstack.exceptions.ResourceNotFound` if nothing
            is found and ignore_missing is ``False``.
        """
        return self._find(_hm.HealthMonitor, name_or_id,
                          ignore_missing=ignore_missing)

    def create_health_monitor(self, **attrs):
        """Create a new health monitor from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.vlb.v3.healthmonitor.HealthMonitor`,
            comprised of the properties on the Member class.
        :returns: The results of health monitor creation
        :rtype: :class:`~otcextensions.sdk.vlb.v3.healthmonitor.HealthMonitor`
        """
        return self._create(_hm.HealthMonitor, **attrs)

    def get_health_monitor(self, healthmonitor):
        """Get a single health monitor

        :param healthmonitor: The value can be the ID of a health monitor or a
            :class:`~openstack.load_balancer.v3.healthmonitor.HealthMonitor`
            instance.
        :returns: One
            :class:`~otcextensions.sdk.vlb.v3.healthmonitor.HealthMonitor`
        :raises: :class:`~openstack.exceptions.ResourceNotFound`
            when no resource can be found.
        """
        return self._get(_hm.HealthMonitor, healthmonitor)

    def health_monitors(self, **query):
        """Return a generator of health monitors

        :param dict query: Optional query parameters to be sent to limit
            the resources being returned.
        :returns: A generator of health monitor objects
        :rtype: :class:`~otcextensions.sdk.vlb.v3.healthmonitor.HealthMonitor`
        """
        return self._list(_hm.HealthMonitor, **query)

    def delete_health_monitor(self, healthmonitor, ignore_missing=True):
        """Delete a health monitor

        :param healthmonitor:
            The value can be either the ID of a health monitor or a
            :class:`~otcextensions.sdk.vlb.v3.health monitor.HealthMonitor`
            instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be
            raised when the member does not exist.
            When set to ``True``, no exception will be set when
            attempting to delete a nonexistent health monitor.
        :returns: ``None``
        """
        return self._delete(_hm.HealthMonitor, healthmonitor,
                            ignore_missing=ignore_missing)

    def update_health_monitor(self, healthmonitor, **attrs):
        """Update a health monitor

        :param healthmonitor: The healthmonitor can be either the ID of the
            health monitor or a
            :class:`~openstack.load_balancer.v3.healthmonitor.HealthMonitor`
            instance
        :param dict attrs: The attributes to update on the health monitor
            represented by ``healthmonitor``.
        :returns: The updated health monitor
        :rtype: :class:`~otcextensions.sdk.vlb.v3.health monitor.HealthMonitor`
        """
        return self._update(_hm.HealthMonitor, healthmonitor,
                            **attrs)

    # ======= L7Policy =======
    def create_l7_policy(self, **attrs):
        """Create a new l7policy from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.vlb.v3.l7_policy.L7Policy`,
            comprised of the properties on the L7Policy class.
        :returns: The results of l7policy creation
        :rtype: :class:`~otcextensions.sdk.vlb.v3.l7_policy.L7Policy`
        """
        return self._create(_l7policy.L7Policy, **attrs)

    def delete_l7_policy(self, l7_policy, ignore_missing=True):
        """Delete a l7policy

        :param l7_policy:
            The value can be either the ID of a l7policy or a
            :class:`~otcextensions.sdk.vlb.v3.l7_policy.L7Policy`
            instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be
            raised when the l7policy does not exist.
            When set to ``True``, no exception will be set when
            attempting to delete a nonexistent l7policy.
        :returns: ``None``
        """
        self._delete(_l7policy.L7Policy, l7_policy,
                     ignore_missing=ignore_missing)

    def find_l7_policy(self, name_or_id, ignore_missing=True):
        """Find a single l7policy

        :param str name_or_id: The name or ID of a l7policy.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be
            raised when the resource does not exist.
            When set to ``True``, None will be returned when
            attempting to find a nonexistent resource.
        :returns: One
            :class:`~otcextensions.sdk.vlb.v3.l7_policy.L7Policy`
            or None
        :raises: :class:`openstack.exceptions.DuplicateResource` if more
            than one resource is found for this request.
        :raises: :class:`openstack.exceptions.ResourceNotFound` if nothing
            is found and ignore_missing is ``False``.
        """
        return self._find(_l7policy.L7Policy, name_or_id,
                          ignore_missing=ignore_missing)

    def get_l7_policy(self, l7_policy):
        """Get a single l7policy

        :param healthmonitor: The value can be the ID of a l7policy or a
            :class:`~openstack.load_balancer.v3.l7_policy.L7Policy`
            instance.
        :returns: One
            :class:`~otcextensions.sdk.vlb.v3.l7_policy.L7Policy`
        :raises: :class:`~openstack.exceptions.ResourceNotFound`
            when no resource can be found.
        """
        return self._get(_l7policy.L7Policy, l7_policy)

    def l7_policies(self, **query):
        """Return a generator of l7policies

        :param dict query: Optional query parameters to be sent to limit
            the resources being returned.
        :returns: A generator of l7policies objects
        :rtype: :class:`~otcextensions.sdk.vlb.v3.l7_policy.L7Policy`
        """
        return self._list(_l7policy.L7Policy, **query)

    def update_l7_policy(self, l7_policy, **attrs):
        """Update a l7policy

        :param l7_policy: The l7policy can be either the ID of the
            l7policy or a
            :class:`~openstack.load_balancer.v3.l7_policy.L7Policy`
            instance
        :param dict attrs: The attributes to update on the l7policy
            represented by ``L7policy``.
        :returns: The updated l7policy
        :rtype: :class:`~otcextensions.sdk.vlb.v3.l7_policy.L7Policy`
        """
        return self._update(_l7policy.L7Policy, l7_policy, **attrs)

    # ======= L7Rule =======
    def create_l7_rule(self, l7_policy, **attrs):
        """Create a new l7rule from attributes

        :param l7_policy: The l7_policy can be either the ID of a l7policy or
            :class:`~otcextensions.sdk.vlb.v3.l7_policy.L7Policy`
            instance that the l7rule will be created in.
        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.vlb.v3.l7_rule.L7Rule`,
            comprised of the properties on the L7Rule class.
        :returns: The results of l7rule creation
        :rtype: :class:`~otcextensions.sdk.vlb.v3.l7_rule.L7Rule`
        """
        l7policyobj = self._get_resource(_l7policy.L7Policy, l7_policy)
        return self._create(_l7rule.L7Rule, l7policy_id=l7policyobj.id,
                            **attrs)

    def delete_l7_rule(self, l7rule, l7_policy, ignore_missing=True):
        """Delete a l7rule

        :param l7rule:
            The l7rule can be either the ID of a l7rule or a
            :class:`~otcextensions.sdk.vlb.v3.l7_rule.L7Rule` instance.
        :param l7_policy: The l7_policy can be either the ID of a l7policy or
            :class:`~otcextensions.sdk.vlb.v3.l7_policy.L7Policy`
            instance that the l7rule belongs to.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be
            raised when the l7rule does not exist.
            When set to ``True``, no exception will be set when
            attempting to delete a nonexistent l7rule.
        :returns: ``None``
        """
        l7policyobj = self._get_resource(_l7policy.L7Policy, l7_policy)
        self._delete(_l7rule.L7Rule, l7rule, ignore_missing=ignore_missing,
                     l7policy_id=l7policyobj.id)

    def find_l7_rule(self, name_or_id, l7_policy, ignore_missing=True):
        """Find a single l7rule

        :param str name_or_id: The name or ID of a l7rule.
        :param l7_policy: The l7_policy can be either the ID of a l7policy or
            :class:`~otcextensions.sdk.vlb.v3.l7_policy.L7Policy`
            instance that the l7rule belongs to.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be
            raised when the resource does not exist.
            When set to ``True``, None will be returned when
            attempting to find a nonexistent resource.
        :returns: One :class:`~otcextensions.sdk.vlb.v3.l7_rule.L7Rule`
            or None
        """
        l7policyobj = self._get_resource(_l7policy.L7Policy, l7_policy)
        return self._find(_l7rule.L7Rule, name_or_id,
                          ignore_missing=ignore_missing,
                          l7policy_id=l7policyobj.id)

    def get_l7_rule(self, l7rule, l7_policy):
        """Get a single l7rule

        :param l7rule: The l7rule can be the ID of a l7rule or a
            :class:`~otcextensions.sdk.vlb.v3.l7_rule.L7Rule`
            instance.
        :param l7_policy: The l7_policy can be either the ID of a l7policy or
            :class:`~otcextensions.sdk.vlb.v3.l7_policy.L7Policy`
            instance that the l7rule belongs to.
        :returns: One :class:`~otcextensions.sdk.vlb.v3.l7_rule.L7Rule`
        :raises: :class:`~openstack.exceptions.ResourceNotFound`
            when no resource can be found.
        """
        l7policyobj = self._get_resource(_l7policy.L7Policy, l7_policy)
        return self._get(_l7rule.L7Rule, l7rule,
                         l7policy_id=l7policyobj.id)

    def l7_rules(self, l7_policy, **query):
        """Return a generator of l7rules

        :param l7_policy: The l7_policy can be either the ID of a l7_policy or
            :class:`~otcextensions.sdk.vlb.v3.l7_policy.L7Policy`
            instance that the l7rule belongs to.
        :param dict query: Optional query parameters to be sent to limit
            the resources being returned. Valid parameters are:
        :returns: A generator of l7rule objects
        :rtype: :class:`~otcextensions.sdk.vlb.v3.l7_rule.L7Rule`
        """
        l7policyobj = self._get_resource(_l7policy.L7Policy, l7_policy)
        return self._list(_l7rule.L7Rule, l7policy_id=l7policyobj.id, **query)

    def update_l7_rule(self, l7rule, l7_policy, **attrs):
        """Update a l7rule

        :param l7rule: Either the ID of a l7rule or a
            :class:`~otcextensions.sdk.vlb.v3.l7_rule.L7Rule`
            instance.
        :param l7_policy: The l7_policy can be either the ID of a l7policy or
            :class:`~otcextensions.sdk.vlb.v3.l7_policy.L7Policy`
            instance that the l7rule belongs to.
        :param dict attrs: The attributes to update on the l7rule
            represented by ``l7rule``.
        :returns: The updated l7rule
        :rtype: :class:`~otcextensions.sdk.vlb.v3.l7_rule.L7Rule`
        """
        l7policyobj = self._get_resource(_l7policy.L7Policy, l7_policy)
        if 'value' in attrs:
            attrs['rule_value'] = attrs.pop('value')
        return self._update(_l7rule.L7Rule, l7rule,
                            l7policy_id=l7policyobj.id, **attrs)

    # ======== Ip address group ========
    def create_ip_address_group(self, **attrs):
        """Create a new ip address group from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.vlb.v3.
            ip_address_group.IpAddressGroup`, comprised of the properties
            on the IpAddressGroup class.

        :returns: The results of ip address group creation
        :rtype: :class:`~otcextensions.sdk.vlb.v3.ip_address_group.
            IpAddressGroup`
        """
        return self._create(_ip_address_group.IpAddressGroup, **attrs)

    def get_ip_address_group(self, ip_address_group):
        """Get an ip address group

        :param ip_address_group: The value can be the name of an
            ip_address_group or :class:`~otcextensions.sdk.vlb.v3.
            ip_address_group.IpAddressGroup` instance.

        :returns: One
             :class:`~otcextensions.sdk.vlb.v3.ip_address_group.IpAddressGroup`
        """
        return self._get(_ip_address_group.IpAddressGroup, ip_address_group)

    def ip_address_groups(self, **query):
        """Retrieve a generator of an ip address group

        :returns: A generator of ip address group instances
        """
        return self._list(_ip_address_group.IpAddressGroup, **query)

    def delete_ip_address_group(self, ip_address_group, ignore_missing=True):
        """Delete an ip address group

        :param ip_address_group: The ip address group can be either the name or
            a :class:`~otcextensions.sdk.vlb.v3.ip_address_group.
            IpAddressGroup` instance
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the ip address group does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent ip address group.

        :returns: ``None``
        """
        ip_address_group = self._get_resource(_ip_address_group.IpAddressGroup,
                                              ip_address_group)
        return self._delete(_ip_address_group.IpAddressGroup, ip_address_group,
                            ignore_missing=ignore_missing)

    def find_ip_address_group(self, name_or_id, ignore_missing=True):
        """Find a single ip address group

        :param name_or_id: The name or ID of an ip address group
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the ip address group does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent ip address group.

        :returns: ``None``
        """
        return self._find(_ip_address_group.IpAddressGroup, name_or_id,
                          ignore_missing=ignore_missing)

    def update_ip_address_group(self, ip_address_group, **attrs):
        """Update a ip address group

        :param ip_address_group: The ip_address_group can be either the name or
            a :class:`~otcextensions.sdk.vlb.v3.ip_address_group.
            IpAddressGroup` instance
        :param dict attrs: The attributes to update on the ip address group
                           represented by ``ip_address_group``.

        :returns: The updated ip_address_group
        :rtype: :class:`~otcextensions.sdk.vlb.v3.ip_address_group.
            IpAddressGroup`
        """
        return self._update(_ip_address_group.IpAddressGroup, ip_address_group,
                            **attrs)

    def update_ip_addresses_in_ip_address_group(self, ip_address_group,
                                                ip_list):
        """Update ip addresses list in an existing ip address group

        :param ip_address_group: The value can be the ID of an ip address group
            or a :class:`~otcextensions.sdk.vlb.v3.ip_address_group.
            IpAddressGroup` instance.
        :param list ip_list: The list contains the IP addresses to be
            updated in the form
            {"ip": "192.168.0.3",  "description": " your description"}
            where "description" is optional
        :returns: The results of ip address group updation
        :rtype: :class:`~otcextensions.sdk.vlb.v3.ip_address_group.
            IpAddressGroup`
        """
        ip_address_group = self._get_resource(_ip_address_group.IpAddressGroup,
                                              ip_address_group)

        return ip_address_group.update_ip_addresses(
            self, ip_list=ip_list
        )

    def delete_ip_addresses_in_ip_address_group(self, ip_address_group,
                                                ip_list):
        """Delete ip addresses list from an existing ip address group

        :param ip_address_group: The value can be the ID of a ip address group
            or a :class:`~otcextensions.sdk.vlb.v3.ip_address_group.
            IpAddressGroup` instance.
        :param list ip_list: The list contains the IP addresses to be deleted
            in the form {"ip": "192.168.0.3"}
        :returns: The results of ip address group deletion
        :rtype: :class:`~otcextensions.sdk.vlb.v3.ip_address_group.
            IpAddressGroup`
        """
        ip_address_group = self._get_resource(_ip_address_group.IpAddressGroup,
                                              ip_address_group)

        return ip_address_group.delete_ip_addresses(
            self, ip_list=ip_list
        )
