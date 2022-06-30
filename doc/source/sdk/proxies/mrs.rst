MRS API
=======

.. automodule:: otcextensions.sdk.mrs.v1._proxy

The MapReduce Service Class
---------------------------

The CBR high-level interface is available through the ``mrs``
member of a :class:`~openstack.connection.Connection` object.  The
``mrs`` member will only be added if the
``otcextensions.sdk.register_otc_extensions(conn)`` method is called.

Cluster Operations
^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.mrs.v1._proxy.Proxy
  :noindex:
  :members: clusters, get_cluster, find_cluster, update_cluster,
            delete_cluster, hosts

Datasource Operations
^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.mrs.v1._proxy.Proxy
  :noindex:
  :members: datasources, create_datasource, get_datasource,
            delete_datasource, find_datasource, update_datasource

Jobbinary Operations
^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.mrs.v1._proxy.Proxy
  :noindex:
  :members: jobbinaries, create_jobbinary, get_jobbinary,
            delete_jobbinary, find_jobbinary, update_jobbinary

Job Operations
^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.mrs.v1._proxy.Proxy
  :noindex:
  :members: jobs, create_job, get_job, delete_job, find_job,
            update_job
