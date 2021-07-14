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
from openstack import exceptions
from openstack import resource
from openstack.dns.v2 import zone
from openstack.network.v2 import router
from openstack import utils

from urllib import parse


class Router(router.Router):
    """DNS Private Zone Router Resource"""

    router_id = resource.Body('router_id')
    router_region = resource.Body('router_region')

    @classmethod
    def find(cls, session, name_or_id, ignore_missing=True, **params):
        """Find a resource by its name or id.

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param name_or_id: This resource's identifier, if needed by
                           the request. The default is ``None``.
        :param bool ignore_missing: When set to ``False``
                    :class:`~openstack.exceptions.ResourceNotFound` will be
                    raised when the resource does not exist.
                    When set to ``True``, None will be returned when
                    attempting to find a nonexistent resource.
        :param dict params: Any additional parameters to be passed into
                            underlying methods, such as to
                            :meth:`~openstack.resource.Resource.existing`
                            in order to pass on URI parameters.

        :return: The :class:`Resource` object matching the given name or id
                 or None if nothing matches.
        :raises: :class:`openstack.exceptions.DuplicateResource` if more
                 than one resource is found for this request.
        :raises: :class:`openstack.exceptions.ResourceNotFound` if nothing
                 is found and ignore_missing is ``False``.
        """
        session = cls._get_session(session)
        # Try to short-circuit by looking directly for a matching ID.
        try:
            match = cls.existing(
                id=name_or_id,
                connection=session._get_connection(),
                **params)
            return match.fetch(session, **params)
        except exceptions.SDKException:
            # DNS may return 400 when we try to do GET with name
            pass

        if ('name' in cls._query_mapping._mapping.keys()
                and 'name' not in params):
            params['name'] = name_or_id

        data = cls.list(session, **params)

        result = cls._get_one_match(name_or_id, data)
        if result is not None:
            return result

        if ignore_missing:
            return None
        raise exceptions.ResourceNotFound(
            "No %s found for %s" % (cls.__name__, name_or_id))

    @classmethod
    def _get_next_link(cls, uri, response, data, marker, limit, total_yielded):
        next_link = None
        params = {}
        if isinstance(data, dict):
            links = data.get('links')
            if links:
                next_link = links.get('next')
            total = data.get('metadata', {}).get('total_count')
            if total:
                # We have a kill switch
                total_count = int(total)
                if total_count <= total_yielded:
                    return None, params

        # Parse params from Link (next page URL) into params.
        # This prevents duplication of query parameters that with large
        # number of pages result in HTTP 414 error eventually.
        if next_link:
            parts = parse.urlparse(next_link)
            query_params = parse.parse_qs(parts.query)
            params.update(query_params)
            next_link = parse.urljoin(next_link,
                                                       parts.path)

        # If we still have no link, and limit was given and is non-zero,
        # and the number of records yielded equals the limit, then the user
        # is playing pagination ball so we should go ahead and try once more.
        if not next_link:
            next_link = uri
            params['marker'] = marker
            if limit:
                params['limit'] = limit
        return next_link, params


class Zone(zone.Zone):
    """DNS ZONE Resource"""

    _query_mapping = resource.QueryParameters(
        'zone_type', 'limit', 'marker', 'offset', 'tags',
        zone_type='type')

    #: Recordset number of the zone
    record_num = resource.Body('record_num', type=int)
    #: A dictionary represent Router(VPC), for private zone
    router = resource.Body('router', type=Router)
    #: Router list associated to this zone
    routers = resource.Body('routers', type=list, list_type=Router)
    #: Zone type, if private, domain will only available in a special VPC.
    #: Valid values include `private`, `public`
    #: *Type: str*
    zone_type = resource.Body('zone_type')

    def _action(self, session, action, body):
        """Preform actions given the message body.

        """
        url = utils.urljoin(self.base_path, self.id, action)
        return session.post(
            url,
            json=body)

    def associate_router(self, session, **router):
        body = {'router': {}}
        body['router']['router_id'] = router.get('router_id')
        if 'router_region' in router:
            body['router']['router_region'] = router.get('router_region')
        return self._action(session, 'associaterouter', body)

    def disassociate_router(self, session, **router):
        body = {'router': {}}
        body['router']['router_id'] = router.get('router_id')
        if 'router_region' in router:
            body['router']['router_region'] = router.get('router_region')
        return self._action(session, 'disassociaterouter', body)

    @classmethod
    def find(cls, session, name_or_id, ignore_missing=True, **params):
        """Find a resource by its name or id.

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param name_or_id: This resource's identifier, if needed by
                           the request. The default is ``None``.
        :param bool ignore_missing: When set to ``False``
                    :class:`~openstack.exceptions.ResourceNotFound` will be
                    raised when the resource does not exist.
                    When set to ``True``, None will be returned when
                    attempting to find a nonexistent resource.
        :param dict params: Any additional parameters to be passed into
                            underlying methods, such as to
                            :meth:`~openstack.resource.Resource.existing`
                            in order to pass on URI parameters.

        :return: The :class:`Resource` object matching the given name or id
                 or None if nothing matches.
        :raises: :class:`openstack.exceptions.DuplicateResource` if more
                 than one resource is found for this request.
        :raises: :class:`openstack.exceptions.ResourceNotFound` if nothing
                 is found and ignore_missing is ``False``.
        """
        session = cls._get_session(session)
        # Try to short-circuit by looking directly for a matching ID.
        try:
            match = cls.existing(
                id=name_or_id,
                connection=session._get_connection(),
                **params)
            return match.fetch(session, **params)
        except exceptions.SDKException:
            # DNS may return 400 when we try to do GET with name
            pass

        if ('name' in cls._query_mapping._mapping.keys()
                and 'name' not in params):
            params['name'] = name_or_id

        data = cls.list(session, **params)

        result = cls._get_one_match(name_or_id, data)
        if result is not None:
            return result

        if ignore_missing:
            return None
        raise exceptions.ResourceNotFound(
            "No %s found for %s" % (cls.__name__, name_or_id))

    @classmethod
    def _get_next_link(cls, uri, response, data, marker, limit, total_yielded):
        next_link = None
        params = {}
        if isinstance(data, dict):
            links = data.get('links')
            if links:
                next_link = links.get('next')
            total = data.get('metadata', {}).get('total_count')
            if total:
                # We have a kill switch
                total_count = int(total)
                if total_count <= total_yielded:
                    return None, params

        # Parse params from Link (next page URL) into params.
        # This prevents duplication of query parameters that with large
        # number of pages result in HTTP 414 error eventually.
        if next_link:
            parts = parse.urlparse(next_link)
            query_params = parse.parse_qs(parts.query)
            params.update(query_params)
            next_link = parse.urljoin(next_link,
                                                       parts.path)

        # If we still have no link, and limit was given and is non-zero,
        # and the number of records yielded equals the limit, then the user
        # is playing pagination ball so we should go ahead and try once more.
        if not next_link:
            next_link = uri
            params['marker'] = marker
            if limit:
                params['limit'] = limit
        return next_link, params
