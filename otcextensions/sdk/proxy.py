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
from openstack import proxy as os_proxy

_logger = _log.setup_logging('openstack')


class SdkProxy(os_proxy.BaseProxy):

    pass

    # @proxy._check_resource(strict=False)
    # def _get(self, resource_type, value=None, requires_id=True,
    #          endpoint_override=None, headers=None,
    #          **attrs):
    #     """Get a resource
    #
    #     overriden to incorporate headers and endpoint_override
    #
    #     :param resource_type: The type of resource to get.
    #     :type resource_type: :class:`~openstack.resource.Resource`
    #     :param value: The value to get. Can be either the ID of a
    #                   resource or a :class:`~openstack.resource.Resource`
    #                   subclass.
    #     :param dict attrs: Attributes to be passed onto the
    #                        :meth:`~openstack.resource.Resource.get`
    #                        method. These should correspond
    #                        to either :class:`~openstack.resource.Body`
    #                        or :class:`~openstack.resource.Header`
    #                        values on this resource.
    #
    #     :returns: The result of the ``get``
    #     :rtype: :class:`~openstack.resource.Resource`
    #     """
    #
    #     res = self._get_resource(resource_type, value, **attrs)
    #
    #     _logger.debug('resource %s' % res)
    #
    #     return res.get(
    #         self, requires_id=requires_id,
    #         error_message="No {resource_type} found for {value}".format(
    #             resource_type=resource_type.__name__, value=value),
    #         endpoint_override=endpoint_override,
    #         headers=headers)
