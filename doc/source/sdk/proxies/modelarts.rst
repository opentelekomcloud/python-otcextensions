Modelarts API
=============

.. automodule:: otcextensions.sdk.modelarts.v1._proxy

The Modelarts Service Class
---------------------------

The modelarts high-level interface is available through the ``modelarts``
member of a :class:`~openstack.connection.Connection` object.  The
``modelarts`` member will only be added if the
``otcextensions.sdk.register_otc_extensions(conn)`` method is called.

Model Operations
^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.modelarts.v1._proxy.Proxy
  :noindex:
  :members: models, find_model, get_model, create_model,
            delete_model

DevEnviron Operations
^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.modelarts.v1._proxy.Proxy
  :noindex:
  :members: devenv_instances, find_devenv_instance, get_devenv_instance,
            create_devenv_instance, delete_devenv_instance,
            start_devenv_instance, stop_devenv_instance
