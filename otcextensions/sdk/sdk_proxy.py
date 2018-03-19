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

from openstack import _log
from openstack import exceptions
from openstack import proxy as os_proxy

_logger = _log.setup_logging('openstack')


class Proxy(os_proxy.BaseProxy):

    def _find(self, resource_type, name_or_id, ignore_missing=True,
              endpoint_override=None, headers=None,
              **attrs):
        """Find a resource

        :param name_or_id: The name or ID of a resource to find.
        :param bool ignore_missing: When set to ``False``
                    :class:`~openstack.exceptions.ResourceNotFound` will be
                    raised when the resource does not exist.
                    When set to ``True``, None will be returned when
                    attempting to find a nonexistent resource.
        :param dict attrs: Attributes to be passed onto the
                           :meth:`~openstack.resource.Resource.find`
                           method, such as query parameters.

        :returns: An instance of ``resource_type`` or None
        """
        result = resource_type.find(self, name_or_id,
                                    ignore_missing=ignore_missing,
                                    endpoint_override=endpoint_override,
                                    headers=headers,
                                    **attrs)
        # Inject endpoint_override into the resource for potential
        # direct use (i.e. instance.reboot)
        if endpoint_override:
            setattr(result, 'endpoint_override', endpoint_override)

        return result

    @os_proxy._check_resource(strict=False)
    def _delete(self, resource_type, value, ignore_missing=True,
                endpoint_override=None, headers=None,
                **attrs):
        """Delete a resource

        :param resource_type: The type of resource to delete. This should
                              be a :class:`~openstack.resource.Resource`
                              subclass with a ``from_id`` method.
        :param value: The value to delete. Can be either the ID of a
                      resource or a :class:`~openstack.resource.Resource`
                      subclass.
        :param bool ignore_missing: When set to ``False``
                    :class:`~openstack.exceptions.ResourceNotFound` will be
                    raised when the resource does not exist.
                    When set to ``True``, no exception will be set when
                    attempting to delete a nonexistent resource.
        :param dict attrs: Attributes to be passed onto the
                           :meth:`~openstack.resource.Resource.delete`
                           method, such as the ID of a parent resource.

        :returns: The result of the ``delete``
        :raises: ``ValueError`` if ``value`` is a
                 :class:`~openstack.resource.Resource` that doesn't match
                 the ``resource_type``.
                 :class:`~openstack.exceptions.ResourceNotFound` when
                 ignore_missing if ``False`` and a nonexistent resource
                 is attempted to be deleted.

        """
        res = self._get_resource(resource_type, value, **attrs)

        try:
            rv = res.delete(
                self,
                error_message=(
                    "Unable to delete {resource_type} for {value}".format(
                        resource_type=resource_type.__name__,
                        value=value,
                    )
                ),
                endpoint_override=endpoint_override,
                headers=headers
            )
        except exceptions.NotFoundException:
            if ignore_missing:
                return None
            raise

        return rv

    @os_proxy._check_resource(strict=False)
    def _update(self, resource_type, value,
                endpoint_override=None, headers=None,
                **attrs):
        """Update a resource

        :param resource_type: The type of resource to update.
        :type resource_type: :class:`~openstack.resource.Resource`
        :param value: The resource to update. This must either be a
                      :class:`~openstack.resource.Resource` or an id
                      that corresponds to a resource.
        :param dict attrs: Attributes to be passed onto the
                           :meth:`~openstack.resource.Resource.update`
                           method to be updated. These should correspond
                           to either :class:`~openstack.resource.Body`
                           or :class:`~openstack.resource.Header`
                           values on this resource.

        :returns: The result of the ``update``
        :rtype: :class:`~openstack.resource.Resource`
        """
        res = self._get_resource(resource_type, value, **attrs)
        return res.update(
            self,
            endpoint_override=endpoint_override,
            headers=headers
        )

    def _create(self, resource_type,
                endpoint_override=None, headers=None,
                prepend_key=True,
                **attrs):
        """Create a resource from attributes

        :param resource_type: The type of resource to create.
        :type resource_type: :class:`~openstack.resource.Resource`
        :param path_args: A dict containing arguments for forming the request
                          URL, if needed.
        :param dict attrs: Attributes to be passed onto the
                           :meth:`~openstack.resource.Resource.create`
                           method to be created. These should correspond
                           to either :class:`~openstack.resource.Body`
                           or :class:`~openstack.resource.Header`
                           values on this resource.

        :returns: The result of the ``create``
        :rtype: :class:`~openstack.resource.Resource`
        """
        res = resource_type.new(**attrs)
        persist = res.create(
            self,
            endpoint_override=endpoint_override,
            headers=headers,
            prepend_key=prepend_key,
        )

        # Inject endpoint_override into the resource for potential
        # direct use (i.e. instance.reboot)
        if endpoint_override:
            persist.endpoint_override = endpoint_override

        return persist

    @os_proxy._check_resource(strict=False)
    def _get(self, resource_type, value=None, requires_id=True,
             endpoint_override=None, headers=None,
             **attrs):
        """Get a resource

        :param resource_type: The type of resource to get.
        :type resource_type: :class:`~openstack.resource.Resource`
        :param value: The value to get. Can be either the ID of a
                      resource or a :class:`~openstack.resource.Resource`
                      subclass.
        :param dict attrs: Attributes to be passed onto the
                           :meth:`~openstack.resource.Resource.get`
                           method. These should correspond
                           to either :class:`~openstack.resource.Body`
                           or :class:`~openstack.resource.Header`
                           values on this resource.

        :returns: The result of the ``get``
        :rtype: :class:`~openstack.resource.Resource`
        """
        res = self._get_resource(resource_type, value, **attrs)

        persist = res.get(
            self, requires_id=requires_id,
            error_message="No {resource_type} found for {value}".format(
                resource_type=resource_type.__name__, value=value),
            endpoint_override=endpoint_override,
            headers=headers
        )

        # Inject endpoint_override into the resource for potential
        # direct use (i.e. instance.reboot)
        if endpoint_override:
            persist.endpoint_override = endpoint_override

        return persist

    def _list(self, resource_type, value=None, paginated=False,
              endpoint_override=None, headers=None,
              **attrs):
        """List a resource

        :param resource_type: The type of resource to delete. This should
                              be a :class:`~openstack.resource.Resource`
                              subclass with a ``from_id`` method.
        :param value: The resource to list. It can be the ID of a resource, or
                      a :class:`~openstack.resource.Resource` object. When set
                      to None, a new bare resource is created.
        :param bool paginated: When set to ``False``, expect all of the data
                               to be returned in one response. When set to
                               ``True``, the resource supports data being
                               returned across multiple pages.
        :param dict attrs: Attributes to be passed onto the
            :meth:`~openstack.resource.Resource.list` method. These should
            correspond to either :class:`~openstack.resource.URI` values
            or appear in :data:`~openstack.resource.Resource._query_mapping`.

        :returns: A generator of Resource objects.
        :raises: ``ValueError`` if ``value`` is a
                 :class:`~openstack.resource.Resource` that doesn't match
                 the ``resource_type``.
        """
        res = self._get_resource(resource_type, value, **attrs)
        return res.list(self, paginated=paginated,
                        endpoint_override=endpoint_override,
                        headers=headers,
                        **attrs)

    def _head(self, resource_type, value=None,
              endpoint_override=None, headers=None,
              **attrs):
        """Retrieve a resource's header

        :param resource_type: The type of resource to retrieve.
        :type resource_type: :class:`~openstack.resource.Resource`
        :param value: The value of a specific resource to retreive headers
                      for. Can be either the ID of a resource,
                      a :class:`~openstack.resource.Resource` subclass,
                      or ``None``.
        :param dict attrs: Attributes to be passed onto the
                           :meth:`~openstack.resource.Resource.head` method.
                           These should correspond to
                           :class:`~openstack.resource.URI` values.

        :returns: The result of the ``head`` call
        :rtype: :class:`~openstack.resource.Resource`
        """
        res = self._get_resource(resource_type, value, **attrs)
        return res.head(self,
                        endpoint_override=endpoint_override,
                        headers=headers
                        )
