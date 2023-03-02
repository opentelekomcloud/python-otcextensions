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
from otcextensions.sdk.elb.v2 import load_balancer as _load_balancer
from openstack.load_balancer.v2 import listener as _listener
from otcextensions.sdk.elb.v2 import load_balancer_tag as _lb_tag
from otcextensions.sdk.elb.v2 import listener_tag as _lstnr_tag


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

    # ======== Load Balancer ========
    def delete_loadbalancer(self, load_balancer, ignore_missing=True,
                            cascade=False):
        """Delete load balancer

        :param load_balancer: Either the ID of a load_balancer
         or a :class:`~otcextensions.sdk.elb.v2.load_balancer.LoadBalancer`
         instance.

        :returns: ``None``
        """
        loadbalancer = self.find_load_balancer(name_or_id=load_balancer)
        if cascade:
            resources = self.process_resources(loadbalancer)
            for healthmonitor in resources['healthmonitors']:
                self.delete_health_monitor(healthmonitor)
            for member in resources['members']:
                self.delete_member(
                    member=member['member_id'],
                    pool=member['pool_id']
                )
            for pool in resources['pools']:
                self.delete_pool(pool)
            for listener in resources['listeners']:
                self.delete_listener(listener)

        return self._delete(
            _load_balancer.LoadBalancer, load_balancer,
            ignore_missing=ignore_missing)

    def process_resources(self, loadbalancer):
        resources = {
            'listeners': [],
            'pools': [],
            'members': [],
            'healthmonitors': []
        }
        if loadbalancer.get('listeners'):
            for listener in loadbalancer.listeners:
                resources['listeners'].append(listener['id'])
        if loadbalancer.get('pools'):
            for pool in loadbalancer.pools:
                resources['pools'].append(pool['id'])
                find_pool = self.find_pool(name_or_id=pool['id'])
                if find_pool.get('health_monitor_id'):
                    resources['healthmonitors'].append(
                        find_pool['health_monitor_id'])
                if find_pool.get('members'):
                    for member in find_pool['members']:
                        resources['members'].append(
                            {
                                'member_id': member['id'],
                                'pool_id': find_pool['id']
                            }
                        )
        return resources

    # ======== Load Balancer Tag ========
    def load_balancer_tags(self, load_balancer, **query):
        """Return a generator of tags

        :param load_balancer: The load_balancer can be either the ID of a
            load balancer or
            :class:`~otcextensions.sdk.elb.v2.loadbalancer.Loadbalancer`
            instance that the load_balancer belongs to.
        :param dict query: Optional query parameters to be sent to limit
            the resources being returned.

        :returns: A generator of tags objects.
        """
        lb_obj = self._get_resource(
            _load_balancer.LoadBalancer,
            load_balancer
        )
        pr_id = self.session.get_project_id()
        base_path = pr_id + _lb_tag.Tag.base_path
        return self._list(
            _lb_tag.Tag,
            base_path=base_path,
            loadbalancer_id=lb_obj.id,
            paginated=False,
            **query)

    def create_load_balancer_tag(self, load_balancer, **attrs):
        """Create a new tag from attributes

        :param load_balancer: The load_balancer can be either the ID of a
            load balancer or
            :class:`~otcextensions.sdk.elb.v2.loadbalancer.Loadbalancer`
            instance that the load_balancer belongs to.
        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.elb.v2.load_balancer_tag.Tag`,
            comprised of the properties on the Tag class.

        :returns: The results of the Tag Creation

        :rtype: :class:`~otcextensions.sdk.elb.v2.load_balancer_tag.Tag`
        """
        lb_obj = self._get_resource(
            _load_balancer.LoadBalancer,
            load_balancer
        )
        return self._create(
            _lb_tag.Tag,
            loadbalancer_id=lb_obj.id,
            **attrs)

    def delete_load_balancer_tag(
            self, load_balancer, key, ignore_missing=True
    ):
        """Delete a tag

        :param key: tag key
        :param load_balancer: The load_balancer can be either the ID of a
            load balancer or
            :class:`~otcextensions.sdk.elb.v2.loadbalancer.Loadbalancer`
            instance that the load_balancer belongs to..
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the tag does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent tag.

        :returns: ``None``
        """
        lb_obj = self._get_resource(
            _load_balancer.LoadBalancer,
            load_balancer
        )
        return self._delete(
            _lb_tag.Tag,
            key,
            loadbalancer_id=lb_obj.id,
            ignore_missing=ignore_missing,
        )

    # ======== Listener Tag ========
    def listener_tags(self, listener, **query):
        """Return a generator of tags

        :param listener: The listener can be either the ID of a
            listener or
            :class:`~otcextensions.sdk.elb.v2.listener.Listener`
            instance that the listener belongs to.
        :param dict query: Optional query parameters to be sent to limit
            the resources being returned.

        :returns: A generator of tags objects.
        """
        listener_obj = self._get_resource(
            _listener.Listener,
            listener
        )
        pr_id = self.session.get_project_id()
        base_path = pr_id + _lstnr_tag.Tag.base_path
        return self._list(
            _lstnr_tag.Tag,
            listener_id=listener_obj.id,
            base_path=base_path,
            paginated=False,
            **query)

    def create_listener_tag(self, listener, **attrs):
        """Create a new tag from attributes

        :param listener: The listener can be either the ID of a
            listener or
            :class:`~otcextensions.sdk.elb.v2.listener.Listener`
            instance that the listener belongs to.
        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.elb.v2.listener_tag.Tag`,
            comprised of the properties on the Tag class.

        :returns: The results of the Tag Creation

        :rtype: :class:`~otcextensions.sdk.elb.v2.listener_tag.Tag`
        """
        listener_obj = self._get_resource(
            _listener.Listener,
            listener
        )
        return self._create(
            _lstnr_tag.Tag,
            listener_id=listener_obj.id,
            **attrs
        )

    def delete_listener_tag(self, listener, key, ignore_missing=True):
        """Delete a tag

        :param key: tag key
        :param listener: The listener can be either the ID of a
            listener or
            :class:`~otcextensions.sdk.elb.v2.listener.Listener`
            instance that the load_balancer belongs to..
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the tag does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent tag.

        :returns: ``None``
        """
        listener_obj = self._get_resource(
            _listener.Listener,
            listener
        )
        return self._delete(
            _lstnr_tag.Tag,
            key,
            listener_id=listener_obj.id,
            ignore_missing=ignore_missing
        )
