Welcome to the OTC Extensions of the OpenStack SDK and CLI!
===========================================================

There are several ways to access an OpenStack cloud. The ultimate way
is accessing the `OpenStack API`_ directly. But that can be very
tedious. The `OpenStack SDK`_ is a Python based client library that
simplifies building applications to work with OpenStack clouds. The
`OpenStack Client`_ is its equivalent on the command line.

**This project, OTC Extensions,** adds extra functionality to the SDK
and the CLI offered by the `Open Telekom Cloud`_. Technically, the OTC
Extensions provide Python classes and methods to attach your own code
to the cloud. They also integrate seamless into the OpenStack Client,
providing many extra commands.

Content
-------

This documentation is split into sections, adressing major use
cases. Additionally some auxiliary documentation is available:

.. toctree::
   :includehidden:
   :numbered: 1
   :maxdepth: 1

   install/index
   install/configuration
   cli/index
   sdk/index
   contributor/index
   coverage
   appendices/index


Installation and Configuration
------------------------------

The :doc:`installation guide <install/index>` explains to system
administrators and developers how to setup the project from system
packages, from pip, and directly from sources. OTC Extensions are easy
to :doc:`configure <install/configuration>`. All credentials can be
configured conveniently in a few files.


Working with the CLI tool
-------------------------

Users who want to access Open Telekom Cloud specific services with
:doc:`command line tools <cli/index>` for a shell like Bash find
documentation of all of their operations and properties in this
section.


Writing your own Scripts for the Cloud
--------------------------------------

Developers writing own Python code may access the API easily by using
the OTC Extensions' classes and methods. The :doc:`SDK interfaces
<sdk/index>` are documented in this section.


Contribute to the Project
-------------------------

To :doc:`contribute <contributor/index>` to the project itself,
developers find helpful background information and architecture
specification of OTC Extensions it this section.


General Information
-------------------

There is general background information about the OTC Extensions
available:

* A :doc:`glossary <appendices/glossary>` describes important terms
  and their naming conventions.

* The :doc:`history <appendices/history>` explains the ancestry of
  this project. This may or may not be insightful if you want to
  understand the project's architecture.

* The project keeps a :doc:`release history
  <appendices/releasenotes>`.

* A list of :doc:`issues <appendices/issues>` is maintained.

* Currently 13 services are :doc:`covered <coverage>` by the OTC
  extensions.

.. _OpenStack API: https://docs.openstack.org/api-quick-start/
.. _OpenStack SDK: https://docs.openstack.org/openstacksdk/
.. _OpenStack Client: https://docs.openstack.org/python-openstackclient/
.. _Ansible modules: https://github.com/OpenTelekomCloud/ansible-collections/
.. _Open Telekom Cloud: https://open-telekom-cloud.com/
