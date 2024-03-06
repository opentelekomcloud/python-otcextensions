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
import json

from openstack import exceptions
from openstack import resource


class ParameterSpec(resource.Resource):
    #: Parameter name.
    label = resource.Body("label")
    #: Whether a parameter is mandatory.
    required = resource.Body("required", type=bool)
    #: Parameter value.
    value = resource.Body("value")


class BuiltInModel(resource.Resource):
    base_path = "/built-in-algorithms"

    resources_key = "models"

    # capabilities
    allow_list = True
    allow_fetch = True

    _query_mapping = resource.QueryParameters(
        "limit",
        "order",
        "offset",
        "search_content",
        "sort_by",
        limit="per_page",
        offset="page",
        sort_by="sortBy",
    )

    # Properties
    #: Time when a model is created.
    created_at = resource.Body("create_time", type=int)
    #: Engine ID of a model.
    engine_id = resource.Body("engine_id", type=int)
    #: Engine name of a model.
    engine_name = resource.Body("engine_name")
    #: Engine version of a model.
    engine_version = resource.Body("engine_version")
    #: Whether the request is successful.
    is_success = resource.Body("is_success", type=bool)
    #: Dataset format required by a model.
    model_dataset_format = resource.Body("model_dataset_format")
    #: URL of the model description.
    model_description_url = resource.Body("model_description_url")
    #: Model ID.
    model_id = resource.Body("model_id")
    #: Model name.
    model_name = resource.Body("model_name")
    #: Model precision.
    model_precision = resource.Body("model_precision")
    #: Model size, in bytes.
    model_size = resource.Body("model_size", type=int)
    #: Model training dataset.
    model_train_dataset = resource.Body("model_train_dataset")
    #: Model usage.
    model_usage = resource.Body("model_usage", type=int)
    #: Model name.
    # name = resource.Body("name", alias="model_name")
    #: Running parameters of a model.
    parameter = resource.Body("parameter", type=list, list_type=ParameterSpec)

    @classmethod
    def existing(cls, connection=None, **kwargs):
        """Create an instance of an existing remote resource.

        When creating the instance set the ``_synchronized`` parameter
        of :class:`Resource` to ``True`` to indicate that it represents the
        state of an existing server-side resource. As such, all attributes
        passed in ``**kwargs`` are considered "clean", such that an immediate
        :meth:`update` call would not generate a body of attributes to be
        modified on the server.

        :param dict kwargs: Each of the named arguments will be set as
            attributes on the resulting Resource object.
        """
        parameter = kwargs.get("parameter")
        if parameter and isinstance(parameter, str):
            kwargs["parameter"] = json.loads(parameter)
        return cls(_synchronized=True, connection=connection, **kwargs)

    @classmethod
    def _get_one_match(cls, name_or_id, results):
        """Given a list of results, return the match"""
        the_result = None
        for maybe_result in results:
            id_value = str(maybe_result.model_id)
            name_value = maybe_result.model_name

            if (id_value == name_or_id) or (name_value == name_or_id):
                # Only allow one resource to be found. If we already
                # found a match, raise an exception to show it.
                if the_result is None:
                    the_result = maybe_result
                else:
                    msg = "More than one %s exists with the name '%s'."
                    msg = msg % (cls.__name__, name_or_id)
                    raise exceptions.DuplicateResource(msg)

        return the_result

    @classmethod
    def find(
        cls,
        session,
        name_or_id: str,
        ignore_missing: bool = True,
        **params,
    ):
        """Find a resource by its name or id.

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param name_or_id: This resource's identifier, if needed by
            the request. The default is ``None``.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the resource does not exist.  When set to ``True``, None will be
            returned when attempting to find a nonexistent resource.
        :param dict params: Any additional parameters to be passed into
            underlying methods, such as to
            :meth:`~openstack.resource.Resource.existing` in order to pass on
            URI parameters.

        :return: The :class:`Resource` object matching the given name or id
            or None if nothing matches.
        :raises: :class:`openstack.exceptions.DuplicateResource` if more
            than one resource is found for this request.
        :raises: :class:`openstack.exceptions.ResourceNotFound` if nothing
            is found and ignore_missing is ``False``.
        """
        session = cls._get_session(session)

        data = cls.list(session, **params)

        result = cls._get_one_match(name_or_id, data)
        if result is not None:
            return result

        if ignore_missing:
            return None

        raise exceptions.ResourceNotFound(
            "No %s found for %s" % (cls.__name__, name_or_id)
        )
