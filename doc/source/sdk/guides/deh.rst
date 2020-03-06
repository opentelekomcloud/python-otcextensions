Dedicated Hosts (DeH)
=====================

.. contents:: Table of Contents
   :local:

The primary resource of the DeH service is the **host**.

CRUD operations
~~~~~~~~~~~~~~~

List Hosts
----------

A **host** is a dedicated host, where virtual machines would be running.

.. literalinclude:: ../examples/deh/list.py
   :pyobject: list_hosts

Full example: `deh host list`_

List Hosts Types
----------------

In order to allocate a host, it's type need to be chosen first. Types might
differ per availability zone, therefore it is required to specify in which
AZ to look for types

.. literalinclude:: ../examples/deh/list_types.py
   :pyobject: list_host_types

Full example: `deh host list type`_

List Host servers
-----------------

Each DeH Host is intended to run virtual instances. Only querying list of
servers is supported

.. literalinclude:: ../examples/deh/list_servers.py
   :pyobject: list_host_servers

Full example: `deh host list server`_

Provisioning operations
~~~~~~~~~~~~~~~~~~~~~~~

Provisioning actions are the main way to manipulate the hosts.

Allocating a DeH Host Instance
------------------------------

A host can be allocated with a following snip.

.. literalinclude:: ../examples/deh/create.py
   :pyobject: create_host

Allocating a DeH Host supports setting `quantity` parameter to allocate
multiple hosts in a one call. Due to that the IDs of allocated hosts are being
returned as part of the "virtual" resource in a `dedicated_host_ids` attribute

Full example: `deh host create`_


.. _deh host list: http://github.com/opentelekomcloud/python-otcextensions/tree/master/examples/deh/list.py
.. _deh host list type: http://github.com/opentelekomcloud/python-otcextensions/tree/master/examples/deh/list_types.py
.. _deh host create: http://github.com/opentelekomcloud/python-otcextensions/tree/master/examples/deh/create.py
.. _deh host list server: http://github.com/opentelekomcloud/python-otcextensions/tree/master/examples/deh/list_servers.py
