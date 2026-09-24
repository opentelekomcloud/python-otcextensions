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
import time
from urllib import parse
from urllib.parse import urlsplit

from openstack import exceptions
from otcextensions.common.utils import extract_region_from_url
from otcextensions.sdk import aksk_auth
from otcextensions.sdk import sdk_proxy
from otcextensions.sdk.sfs3.v3 import file_system as _file_system

#: The number of seconds a temporary AK/SK is renewed before it expires
TMP_AKSK_RENEWAL = 30

#: Minimal duration (in seconds) of a temporary AK/SK
TMP_AKSK_DURATION = 900


class Proxy(sdk_proxy.Proxy):
    skip_discovery = True

    #: Fallback endpoint used when the service catalog does not provide
    #: one (the SFS3 endpoint carries no project id or API version).
    FILE_SYSTEM_ENDPOINT = "https://sfs3.%(region_name)s.otc.t-systems.com"

    def _extract_name(self, url, service_type=None, project_id=None):
        url_path = parse.urlparse(url).path.strip()
        # Remove / from the beginning to keep the list indexes of interesting
        # things consistent
        if url_path.startswith("/"):
            url_path = url_path[1:]

        # Split url into parts and exclude potential project_id in some urls
        url_parts = url_path.split("/")

        # Strip out anything that's empty or None
        parts = [part for part in url_parts if part]

        # Getting the root of an endpoint is a bucket operation
        if not parts:
            return ["bucket"]
        else:
            return ["object"]

    def get_filesystem_endpoint(self, name):
        """Return the virtual-hosted endpoint of a file system.

        :param name: The file system name.
        :returns: ``scheme://name.<base endpoint netloc>``
        """
        split_url = urlsplit(self.get_endpoint())
        return f"{split_url.scheme}://{name}.{split_url.netloc}"

    def _get_region(self):
        """Determine the region used in the request signature scope."""
        try:
            region = extract_region_from_url(self.get_endpoint())
        except Exception:
            region = None
        if not region:
            region = getattr(self, "region_name", None)
        if not region and hasattr(self, "_connection"):
            region = self._connection.region_name
        return region

    def _get_credentials(self):
        """Fetch an AK/SK pair for the SFS3 service.

        The pair is first looked up on the connection (user-supplied
        AK/SK, or the shared ``_tmp_aksk`` cache when ``autocreate_aksk``
        is enabled). If none is available -- i.e. the connection is
        password/token based -- a temporary AK/SK is created via the
        identity service. A still-valid temporary token already cached on
        the connection is reused instead of minting a new one, so this
        interop with the ``autocreate_aksk`` flow and does not create a
        new token on every request.

        :returns: (access_key, secret_key, security_token)
        :raises: :class:`~openstack.exceptions.ResourceFailure` when
            neither AK/SK nor a working identity proxy is available.
        """
        conn = self.session._sdk_connection

        ak = sk = token = None
        if hasattr(conn, "get_ak_sk"):
            aksk = conn.get_ak_sk(conn)
            if len(aksk) == 2:
                ak, sk = aksk
            elif len(aksk) == 3:
                ak, sk, token = aksk

        if ak and sk:
            return ak, sk, token

        # No user AK/SK: fall back to a temporary AK/SK.
        cached = conn.config.config.get("_tmp_aksk", {})
        if (
            cached.get("access_key")
            and cached.get("secret_key")
            and (cached.get("expires", 0) - TMP_AKSK_RENEWAL) >= int(time.time())
        ):
            # Reuse a still-valid temporary token
            return (
                cached["access_key"],
                cached["secret_key"],
                cached.get("security_token"),
            )

        self.log.info(
            "AK/SK is not configured; creating a temporary AK/SK "
            "for the SFS3 service"
        )
        tmp_aksk = conn.identity.create_security_token(duration=TMP_AKSK_DURATION)
        cached["expires"] = int(time.time()) + TMP_AKSK_DURATION
        cached["access_key"] = tmp_aksk.access
        cached["secret_key"] = tmp_aksk.secret
        cached["security_token"] = tmp_aksk.security_token
        conn.config.config["_tmp_aksk"] = cached

        if not (tmp_aksk.access and tmp_aksk.secret):
            raise exceptions.ResourceFailure(
                "Cannot obtain an AK/SK pair for the SFS3 service: "
                "none is configured and a temporary one could not "
                "be created"
            )
        return tmp_aksk.access, tmp_aksk.secret, tmp_aksk.security_token

    def _get_bucket_from_host(self, host):
        """Derive the bucket (file system) name from a request host.

        The SFS3 file systems use virtual-hosted endpoints of the form
        ``<name>.sfs3.<region>...``; the base endpoint ``sfs3.<region>...``
        (used for listing) carries no bucket. The name is the first label
        of the host when it differs from the base endpoint's first label.
        """
        base = urlsplit(self.get_endpoint()).netloc
        netloc = urlsplit(host).netloc if "://" in host else host
        if not netloc or netloc == base:
            return ""
        first = netloc.split(".", 1)[0]
        base_first = base.split(".", 1)[0] if base else ""
        # A virtual-hosted endpoint has the bucket name prepended, so its
        # first label differs from the base endpoint's (``sfs3``).
        if first != base_first:
            return first
        return ""

    def _get_req_auth(self, host=None):
        """Build (and cache) the request authentication.

        The SFS3 service only creates SFS-type buckets when the request is
        signed with the native OBS V1 scheme, so this returns an
        :class:`~otcextensions.sdk.aksk_auth.AkskRequestsAuth` signer
        (HMAC-SHA1, ``Authorization: OBS <ak>:<sig>``), distinct from the
        SigV4 signer in :mod:`otcextensions.sdk.ak_auth` used by OBS.

        Static (token-less) signers are cached for the lifetime of the
        proxy. Signers carrying a security token (temporary credentials)
        are rebuilt on every call so the shared ``_tmp_aksk`` cache stays
        authoritative and an expiring token is refreshed transparently.

        :param host: The host the request will be signed for
            (virtual-hosted endpoints differ per file system). The bucket
            name is derived from it for the canonical resource.
        :returns: An :class:`~otcextensions.sdk.aksk_auth.AkskRequestsAuth`
            instance.
        """
        if not host:
            host = self.get_endpoint()
        ak, sk, token = self._get_credentials()
        bucket = self._get_bucket_from_host(host)
        if not token:
            # A cached static signer for this bucket is reused
            cache = getattr(self, "_aksk_auth_cache", None)
            if cache and bucket in cache:
                return cache[bucket]
        auth_params = {
            "access_key": ak,
            "secret_key": sk,
            "bucket": bucket,
        }
        if token:
            auth_params["security_token"] = token
        auth = aksk_auth.AkskRequestsAuth(**auth_params)
        # Cache only token-less (static) signers; the cache key includes
        # the bucket so per-file-system signers are not shared across hosts.
        if not token:
            cache = getattr(self, "_aksk_auth_cache", {})
            cache[bucket] = auth
            setattr(self, "_aksk_auth_cache", cache)
        return auth

    # ======== File Systems ========

    def file_systems(self, **query):
        """Obtain FileSystem objects for this project.

        :param kwargs query: Optional query parameters to be sent to
            limit the resources being returned.

        :rtype: A generator of
            :class:`~otcextensions.sdk.sfs3.v1.file_system.FileSystem`
            objects.
        """
        endpoint = self.get_endpoint()
        return self._list(
            _file_system.FileSystem,
            endpoint_override=endpoint,
            headers={"x-obs-bucket-type": "SFS"},
            requests_auth=self._get_req_auth(endpoint),
            **query,
        )

    def create_filesystem(self, name, location=None, **attrs):
        """Create a new file system.

        :param str name: The name of the file system to create. It must
            be unique within SFS.
        :param str location: The region in which to create the file
            system. Defaults to the connection region.
        :param dict attrs: Additional attributes for the
            :class:`~otcextensions.sdk.sfs3.v1.file_system.FileSystem`.

        :returns: The created file system
        :rtype:
            :class:`~otcextensions.sdk.sfs3.v1.file_system.FileSystem`
        """
        if not location:
            location = self._get_region()
        # A file system is addressed by its virtual-hosted endpoint
        # (<name>.sfs3.<region>...), same as OBS containers
        endpoint = self.get_filesystem_endpoint(name)
        return self._create(
            _file_system.FileSystem,
            name=name,
            location=location,
            sfs_type="SFS",
            az_redundancy="3az",
            endpoint_override=endpoint,
            requests_auth=self._get_req_auth(endpoint),
            **attrs,
        )

    def get_filesystem(self, name):
        """Get the detail of a file system.

        :param name: The file system name or an object of class
            :class:`~otcextensions.sdk.sfs3.v1.file_system.FileSystem`.
        :returns: The file system details
        :rtype:
            :class:`~otcextensions.sdk.sfs3.v1.file_system.FileSystem`
        """
        name = self._get_filesystem_name(name)
        endpoint = self.get_filesystem_endpoint(name)
        return self._head(
            _file_system.FileSystem,
            name,
            endpoint_override=endpoint,
            requests_auth=self._get_req_auth(endpoint),
        )

    def delete_filesystem(self, name, ignore_missing=True):
        """Delete a file system.

        :param name: The file system name or an object of class
            :class:`~otcextensions.sdk.sfs3.v1.file_system.FileSystem`.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be
            raised when the file system does not exist. When set to
            ``True``, no exception will be raised when attempting to
            delete a nonexistent file system.

        :returns: ``None``
        """
        name = self._get_filesystem_name(name)
        endpoint = self.get_filesystem_endpoint(name)
        self._delete(
            _file_system.FileSystem,
            name,
            endpoint_override=endpoint,
            requests_auth=self._get_req_auth(endpoint),
            ignore_missing=ignore_missing,
        )

    def _get_filesystem_name(self, name):
        """Normalize a file system reference to its name."""
        if isinstance(name, _file_system.FileSystem):
            return name.name
        if isinstance(name, str):
            return name
        raise ValueError(
            "name must be a file system name or a "
            "FileSystem instance, got %s" % type(name)
        )

    # ======== File System ACL ========

    def create_acl(self, name, statements):
        """Configure the ACL of a file system.

        The change takes about 30 seconds to become effective.

        :param name: The file system name or an object of class
            :class:`~otcextensions.sdk.sfs3.v1.file_system.FileSystem`.
        :param list statements: A list of ACL statements. Each statement is
            a dict with the following keys:

            - ``Action`` (required): ``FullControl`` (read/write) or
              ``Read`` (read-only).
            - ``Effect`` (required): always ``Allow``.
            - ``Condition`` (required): a dict with a required
              ``SourceVpc`` (a VPC id) and an optional ``VpcSourceIp``
              (list of IP addresses or CIDR ranges, currently ignored
              by the service).
            - ``Sid`` (optional): a statement id.

        :returns: ``None``
        """
        name = self._get_filesystem_name(name)
        endpoint = self.get_filesystem_endpoint(name)
        url = endpoint + "/?sfsacl"
        self.session.put(
            url,
            json={"Statement": statements},
            headers={"Content-Type": "application/json"},
            endpoint_override=endpoint,
            requests_auth=self._get_req_auth(endpoint),
        )

    def get_acl(self, name):
        """Get the ACL of a file system.

        :param name: The file system name or an object of class
            :class:`~otcextensions.sdk.sfs3.v1.file_system.FileSystem`.
        :returns: A list of ACL statement dicts, each with the keys
            ``Sid``, ``Action``, ``Effect`` and ``Condition``.
        :rtype: list
        """
        name = self._get_filesystem_name(name)
        endpoint = self.get_filesystem_endpoint(name)
        url = endpoint + "/?sfsacl"
        response = self.session.get(
            url,
            endpoint_override=endpoint,
            requests_auth=self._get_req_auth(endpoint),
        )
        if response.status_code == 204:
            return []
        return (response.json() or {}).get("Statement", [])

    def delete_acl(self, name):
        """Delete the ACL of a file system.

        :param name: The file system name or an object of class
            :class:`~otcextensions.sdk.sfs3.v1.file_system.FileSystem`.
        :returns: ``None``
        """
        name = self._get_filesystem_name(name)
        endpoint = self.get_filesystem_endpoint(name)
        url = endpoint + "/?sfsacl"
        self.session.delete(
            url,
            endpoint_override=endpoint,
            requests_auth=self._get_req_auth(endpoint),
        )

    # ======== Tags (TMS) ========

    def _get_project_id(self):
        """Return the project id for the TMS (tags) API paths."""
        project_id = self.session.get_project_id()
        if not project_id:
            raise exceptions.ResourceFailure(
                "Cannot determine the project id for the SFS3 tags "
                "API: the connection was not authenticated with a "
                "project"
            )
        return project_id

    def _tags_endpoint(self, project_id=None):
        """Return the TMS base endpoint for the SFS3 file system resource."""
        if not project_id:
            project_id = self._get_project_id()
        return "%s/v3/sfs/tms/%s/file-systems" % (self.get_endpoint(), project_id)

    def add_tags(self, name, tags):
        """Batch-add tags to a file system.

        Up to 20 tags can be attached to a resource.

        :param name: The file system name or an object of class
            :class:`~otcextensions.sdk.sfs3.v1.file_system.FileSystem`.
        :param list tags: A list of tag dicts, each with a required
            ``key`` and an optional ``value``.
        :returns: ``None``
        """
        name = self._get_filesystem_name(name)
        endpoint = self._tags_endpoint()
        self.session.post(
            endpoint + "/%s/tags/create" % name,
            json={"tags": tags},
            headers={"Content-Type": "application/json"},
            endpoint_override=self.get_endpoint(),
        )

    def delete_tags(self, name, tags):
        """Batch-delete tags from a file system.

        System tags cannot be deleted. If a tag to be deleted is not
        found, a success is returned.

        :param name: The file system name or an object of class
            :class:`~otcextensions.sdk.sfs3.v1.file_system.FileSystem`.
        :param list tags: A list of tag dicts to remove, each with a
            required ``key`` and an optional ``value``.
        :returns: ``None``
        """
        name = self._get_filesystem_name(name)
        endpoint = self._tags_endpoint()
        self.session.post(
            endpoint + "/%s/tags/delete" % name,
            json={"tags": tags},
            headers={"Content-Type": "application/json"},
            endpoint_override=self.get_endpoint(),
        )

    def get_tags(self, name):
        """Get the tags of a file system.

        :param name: The file system name or an object of class
            :class:`~otcextensions.sdk.sfs3.v1.file_system.FileSystem`.
        :returns: A dict with the keys ``tags`` (a list of tag dicts with
            ``key``/``value``) and, when the caller has the ``op_service``
            permission, ``sys_tags``.
        :rtype: dict
        """
        name = self._get_filesystem_name(name)
        endpoint = self._tags_endpoint()
        response = self.session.get(
            endpoint + "/%s/tags" % name,
            headers={"Content-Type": "application/json"},
            endpoint_override=self.get_endpoint(),
        )
        return response.json()

    def get_project_tags(self):
        """Query the tags of all file systems in this project.

        :returns: A dict with a ``tags`` key holding a list of tag dicts,
            each with a ``key`` and a ``values`` list.
        :rtype: dict
        """
        endpoint = self._tags_endpoint()
        response = self.session.get(
            endpoint + "/tags",
            headers={"Content-Type": "application/json"},
            endpoint_override=self.get_endpoint(),
        )
        return response.json()

    def filter_resources_by_tags(
        self,
        tags=None,
        sys_tags=None,
        without_any_tag=None,
        matches=None,
        limit=1000,
        offset=0,
    ):
        """Query file systems by tag.

        Resources are sorted by creation time, in descending order.
        Tag keys are in an AND relationship, values of a key are in an
        OR relationship.

        :param list tags: A list of tag dicts, each with a required
            ``key`` and a required ``values`` list. Up to 20 tags, up to
            20 values per key. When omitted, all resources are returned.
        :param list sys_tags: System tag filter (``op_service``
            permission only).
        :param bool without_any_tag: When ``True``, all resources without
            tags are returned and ``tags`` is ignored.
        :param list matches: A list of match dicts, each with a ``key``
            fixed at ``resource_name`` (prefix search) and a ``value``.
        :param int limit: The number of records to query (1-1000,
            default 1000).
        :param int offset: The start index (default 0).
        :returns: A dict with ``resources`` (a list of file system dicts
            with ``resource_id``, ``resource_name``, ``tags``) and
            ``total_count``.
        :rtype: dict
        """
        endpoint = self._tags_endpoint()
        body = {}
        if tags is not None:
            body["tags"] = tags
        if sys_tags is not None:
            body["sys_tags"] = sys_tags
        if without_any_tag is not None:
            body["without_any_tag"] = without_any_tag
        if matches is not None:
            body["matches"] = matches
        response = self.session.post(
            endpoint + "/resource-instances/filter",
            json=body,
            headers={"Content-Type": "application/json"},
            params={"limit": limit, "offset": offset},
            endpoint_override=self.get_endpoint(),
        )
        return response.json()

    def count_resources_by_tags(
        self, tags=None, sys_tags=None, without_any_tag=None, matches=None
    ):
        """Query the number of file systems matching the given tags.

        :param list tags: A list of tag dicts (``key``/``values``).
        :param list sys_tags: System tag filter (``op_service``
            permission only).
        :param bool without_any_tag: When ``True``, count resources
            without any tag.
        :param list matches: A list of match dicts (``resource_name``
            prefix search).
        :returns: A dict with a ``total_count`` key.
        :rtype: dict
        """
        endpoint = self._tags_endpoint()
        body = {}
        if tags is not None:
            body["tags"] = tags
        if sys_tags is not None:
            body["sys_tags"] = sys_tags
        if without_any_tag is not None:
            body["without_any_tag"] = without_any_tag
        if matches is not None:
            body["matches"] = matches
        response = self.session.post(
            endpoint + "/resource-instances/count",
            json=body,
            headers={"Content-Type": "application/json"},
            endpoint_override=self.get_endpoint(),
        )
        return response.json()
