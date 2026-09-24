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
import xml.etree.ElementTree as ET

from openstack import _log
from openstack import exceptions
from openstack import resource
from otcextensions.sdk.obs.v1 import _base

_logger = _log.setup_logging("openstack")


class FileSystem(_base.BaseResource):
    """A SFS General Purpose File System (SFS3).

    Internally an SFS3 file system is an OBS bucket of type SFS, so the
    resource reuses the OBS XML parsing helpers from
    :class:`~otcextensions.sdk.obs.v1._base.BaseResource`.
    """

    resources_key = "Buckets"
    resource_key = "Bucket"

    allow_get = True
    allow_fetch = True
    allow_head = True
    allow_list = True
    allow_create = True
    allow_delete = True

    base_path = "/"

    # all requests (except create) default to requires_id = None,
    # because the file system name is part of the virtual-hosted
    # endpoint, not the URI
    requires_id = None

    #: The unique name of the file system.
    name = resource.Body("Name", alternate_id=True, alias="id")
    #: The time when the file system was created.
    created_at = resource.Body("CreationDate", alias="creation_date")
    #: The location (region) of the file system.
    location = resource.Body("Location")
    #: The type of the bucket backing the file system (SFS).
    bucket_type = resource.Body("BucketType")

    # Headers required by the SFS3 API
    #: Marks the request as a file system operation (value: SFS).
    sfs_type = resource.Header("x-obs-bucket-type")
    #: File system redundancy, required on create (value: 3az).
    az_redundancy = resource.Header("x-obs-az-redundancy")

    def _prepare_request(self, requires_id=None, prepend_key=False):
        """Prepare a request to be sent to the server.

        The URI is always "/" -- the file system name, when needed, is
        carried by the virtual-hosted endpoint (endpoint_override).
        """
        if requires_id is None:
            requires_id = self.requires_id

        base_path = "/"
        headers = {}
        for k, v in self._header.dirty.items():
            if isinstance(v, list):
                headers[k] = ", ".join(v)
            else:
                headers[k] = str(v)

        if requires_id:
            if self.id is None:
                raise exceptions.InvalidRequest(
                    "Request requires an ID but none was found"
                )

        return resource._Request(base_path, None, headers)

    def create(
        self,
        session,
        prepend_key=True,
        endpoint_override=None,
        headers=None,
        requests_auth=None,
    ):
        """Create a file system (PUT / with SFS headers and an XML body).

        :param session: The session to use for making this request.
        :param endpoint_override: The virtual-hosted endpoint of the
            file system (``<name>.sfs3.<region>...``).
        :param headers: Additional headers for the request.
        :param requests_auth: The ``AKRequestsAuth`` instance to sign the
            request.

        :returns: This :class:`FileSystem` instance.
        :raises: :exc:`~openstack.exceptions.MethodNotSupported` if
            :data:`Resource.allow_create` is not set to ``True``.
        """
        if not self.allow_create:
            raise exceptions.MethodNotSupported(self, "create")

        session = self._get_session(session)

        request = self._prepare_request()

        req_args = self._prepare_override_args(
            endpoint_override=endpoint_override,
            request_headers=request.headers,
            additional_headers=headers,
            requests_auth=requests_auth,
        )

        # SFS3 creates the file system from the virtual-hosted host and the
        # ``x-obs-bucket-type: SFS`` header, signed with the native OBS V1
        # scheme. A request body is optional -- the service defaults the
        # redundancy (3az) and protocol (NFS) when none is supplied.
        response = session.put(request.url, data=None, **req_args)

        self._translate_response(response)
        return self

    def _translate_response(
        self, response, has_body=True, error_message=None, resource_response_key=None
    ):
        """Given a response, inflate this instance with its data.

        SFS3 responses are XML or empty (204); the meaningful part of a
        file system object is its name, which is known from the
        virtual-hosted endpoint.
        """
        exceptions.raise_from_response(response, error_message=response.text)

    @classmethod
    def list(
        cls,
        session,
        paginated=False,
        endpoint_override=None,
        headers=None,
        requests_auth=None,
        **params
    ):
        """List all file systems.

        :param session: The session to use for making this request.
        :param endpoint_override: The base SFS3 endpoint.
        :param headers: Headers for the request (must contain
            ``x-obs-bucket-type: SFS``).
        :param requests_auth: The ``AKRequestsAuth`` instance to sign the
            request.

        :returns: A generator of :class:`FileSystem` objects.
        :raises: :exc:`~openstack.exceptions.MethodNotSupported` if
            :data:`Resource.allow_list` is not set to ``True``.
        """
        if not cls.allow_list:
            raise exceptions.MethodNotSupported(cls, "list")

        cls._query_mapping._validate(params, base_path=cls.base_path)

        session = cls._get_session(session)

        get_args = cls._prepare_override_args(
            endpoint_override=endpoint_override,
            additional_headers=headers,
            requests_auth=requests_auth,
        )

        response = session.get(
            session.get_endpoint(endpoint_override=endpoint_override),
            **get_args,
        )

        exceptions.raise_from_response(response)

        if not response.content:
            return

        root = ET.fromstring(response.content)

        if root.tag != ET.QName(cls.OBS_NS, "ListAllMyBucketsResult"):
            _logger.warn("Namespace in the response does not match expectation")
            cls.OBS_NS = root.tag.split("}", 1)[0][1:]

        for element in root:
            if element.tag == ET.QName(cls.OBS_NS, cls.resources_key):
                for el in element:
                    if el.tag == ET.QName(cls.OBS_NS, cls.resource_key):
                        # Convert XML part into dict
                        dict_raw_resource = cls.etree_to_dict(el)
                        # extract resource data
                        dict_resource = dict_raw_resource[cls.resource_key]
                        yield cls.existing(**dict_resource)

        return
