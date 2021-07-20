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
# from otcextensions.sdk.vlb.v2 import member as _member
# from otcextensions.sdk.vlb.v2 import pool as _pool
# from otcextensions.sdk.vlb.v2 import provider as _provider
from otcextensions.sdk.vlb.v3 import certificate as _certificate
# from otcextensions.sdk.vlb.v2 import availability_zone_profile as \
#    _availability_zone_profile
from otcextensions.sdk.vlb.v3 import flavor as _flavor
# from otcextensions.sdk.vlb.v2 import flavor_profile as _flavor_profile
# from otcextensions.sdk.vlb.v2 import health_monitor as _hm
# from otcextensions.sdk.vlb.v2 import l7_policy as _l7policy
# from otcextensions.sdk.vlb.v2 import l7_rule as _l7rule
from otcextensions.sdk.vlb.v3 import listener as _listener
from otcextensions.sdk.vlb.v3 import load_balancer as _lb
from otcextensions.sdk.vlb.v3 import load_balancer_status as _lb_statuses
from otcextensions.sdk.vlb.v3 import quota as _quota


class Proxy(proxy.Proxy):
    skip_discovery = True

    # ======== Load balancer ========
    def create_load_balancer(self, **attrs):
        """Create a new load balancer from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.vlb.v2.
            load_balancer.LoadBalancer`, comprised of the properties on the
            LoadBalancer class.

        :returns: The results of load balancer creation
        :rtype: :class:`~otcextensions.sdk.vlb.v2.load_balancer.LoadBalancer`
        """
        return self._create(_lb.LoadBalancer, **attrs)

    def get_load_balancer(self, *attrs):
        """Get a load balancer

        :param load_balancer: The value can be the name of a load balancer
             or :class:`~otcextensions.sdk.vlb.v2.load_balancer.LoadBalancer`
             instance.

        :returns: One
             :class:`~otcextensions.sdk.vlb.v2.load_balancer.LoadBalancer`
        """
        return self._get(_lb.LoadBalancer, *attrs)

    def get_load_balancer_statistics(self, name_or_id):
        """Get the load balancer statistics

        :param name_or_id: The name or ID of a load balancer

        :returns: One :class:`~otcextensions.sdk.vlb.v2.load_balancer.
                  LoadBalancerStats`
        """
        return self._get(_lb.LoadBalancerStats, lb_id=name_or_id,
                         requires_id=False)

    def load_balancers(self, **query):
        """Retrieve a generator of load balancers

        :returns: A generator of load balancer instances
        """
        return self._list(_lb.LoadBalancer, **query)

    def delete_load_balancer(self, load_balancer, ignore_missing=True,
                             cascade=False):
        """Delete a load balancer

        :param load_balancer: The load_balancer can be either the name or a
            :class:`~otcextensions.sdk.vlb.v2.load_balancer.LoadBalancer`
            instance
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the load balancer does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent load balancer.

        :returns: ``None``
        """
        load_balancer = self._get_resource(_lb.LoadBalancer, load_balancer)
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
            :class:`~otcextensions.sdk.vlb.v2.load_balancer.LoadBalancer`
            instance
        :param dict attrs: The attributes to update on the load balancer
                           represented by ``load_balancer``.

        :returns: The updated load_balancer
        :rtype: :class:`~otcextensions.sdk.vlb.v2.load_balancer.LoadBalancer`
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
            a :class:`~otcextensions.sdk.vlb.v2.
            listener.Listener`, comprised of the properties on the
            Listener class.

        :returns: The results of listener creation
        :rtype: :class:`~otcextensions.sdk.vlb.v2.listener.Listener`
        """
        return self._create(_listener.Listener, **attrs)

    def delete_listener(self, listener, ignore_missing=True):
        """Delete a listener

        :param listener: The value can be either the ID of a listner or a
               :class:`~otcextensions.sdk.vlb.v2.listener.Listener` instance.
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
                      :class:`~otcextensions.sdk.vlb.v2.listener.Listener`
                      instance.
        :param dict attrs: The attributes to update on the listener
                           represented by ``listener``.
        :returns: The updated listener
        :rtype: :class:`~otcextensions.sdk.vlb.v2.listener.Listener`
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
        :returns: One :class:`~otcextensions.sdk.vlb.v2.listener.Listener`
         or None
        """
        return self._find(_listener.Listener, name_or_id,
                          ignore_missing=ignore_missing)

    def get_listener(self, listener):
        """Get a single listener

        :param listener: The value can be the ID of a listener or a
               :class:`~otcextensions.sdk.vlb.v2.listener.Listener`
               instance.
        :returns: One :class:`~otcextensions.sdk.vlb.v2.listener.Listener`
        :raises: :class:`~openstack.exceptions.ResourceNotFound`
                 when no resource can be found.
        """
        return self._get(_listener.Listener, listener)

    def listeners(self, **query):
        """Retrieve a generator of listeners

        :returns: A generator of listeners instances
        :rtype: :class:`~otcextensions.sdk.vlb.v2.listener.Listener`
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
    def quotas(self):
        """Retrieve a quotas

        :returns: A quota instance
        :rtype: :class:`~otcextensions.sdk.vlb.v3.quota.Quota`
        """
        return _quota.Quota.get(self)

    # ======== Availability zone ========
    def availability_zones(self, **query):
        """Retrieve a generator of availability zones

        :returns: A AvailabilityZone instance
        :rtype: :class:`~otcextensions.sdk.vlb.v3.availability_zone.
            AvailabilityZone`
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
        """Get a single instance

        :param instance: The value can be either the ID of an instance or a
            :class:`~otcextensions.sdk.dds.v3.flavor.Flavor` instance.

        :returns: One :class:`~otcextensions.sdk.vlb.v3.flavor.Flavor`
        """
        return self._get(_flavor.Flavor, flavor)

    def find_flavor(self, name_or_id, ignore_missing=True):
        """Find a single flavor

        :param name_or_id: The name or ID of a flavor
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the load balancer does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent load balancer.

        :returns: ``None``
        """
        return self._find(_flavor.Flavor, name_or_id,
                          ignore_missing=ignore_missing)
