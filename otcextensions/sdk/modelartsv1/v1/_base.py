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
#
from openstack import exceptions
from openstack import resource


class Resource(resource.Resource):
    query_marker_key = "offset"

    _query_mapping = resource.QueryParameters(
        "marker", "limit", marker="offset"
    )

    @classmethod
    def list(
        cls,
        session,
        paginated=True,
        base_path=None,
        allow_unknown_params=False,
        **params
    ):
        if not cls.allow_list:
            raise exceptions.MethodNotSupported(cls, "list")
        session = cls._get_session(session)
        microversion = cls._get_microversion(session, action="list")

        if base_path is None:
            base_path = cls.base_path
        params = cls._query_mapping._validate(
            params,
            base_path=base_path,
            allow_unknown_params=allow_unknown_params,
        )

        query_params = cls._query_mapping._transpose(params, cls)
        uri = base_path % params

        limit = query_params.get("limit")

        # Track the total number of resources yielded so we can paginate
        # swift objects
        total_yielded = query_params.get("offset", 0)
        while uri:
            # Copy query_params due to weird mock unittest interactions
            response = session.get(
                uri,
                headers={"Accept": "application/json"},
                params=query_params.copy(),
                microversion=microversion,
            )
            exceptions.raise_from_response(response)
            data = response.json()
            # Discard any existing pagination keys
            query_params.pop("offset", None)
            query_params.pop("limit", None)

            if cls.resources_key:
                resources = data[cls.resources_key]
            else:
                resources = data

            if not isinstance(resources, list):
                resources = [resources]

            marker = None
            for raw_resource in resources:
                value = cls.existing(
                    microversion=microversion,
                    connection=session._get_connection(),
                    **raw_resource
                )
                marker = total_yielded + 1
                yield value
                total_yielded += 1

            if resources and paginated:
                uri, next_params = cls._get_next_link(
                    uri, response, data, marker, limit, total_yielded
                )
                query_params.update(next_params)
            else:
                return

    @classmethod
    def _get_next_link(cls, uri, response, data, marker, limit, total_yielded):
        # RDS service pagination. Returns query for the next page
        next_link = None
        params = {}
        if "total_count" in data and total_yielded < data["total_count"]:
            next_link = uri
            params["offset"] = marker
            params["limit"] = limit
        else:
            next_link = None
        query_params = cls._query_mapping._transpose(params, cls)
        return next_link, query_params
