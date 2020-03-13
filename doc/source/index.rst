Welcome to the OTC Extensions of the OpenStack SDK and CLI!
===========================================================

Accessing the `OpenStack API`_ directly can be tedious. The `OpenStack
SDK`_ is a Python based client library that simplifies building
applications to work with OpenStack clouds. **This project, OTC
Extensions,** augments this SDK and adds extra functionality offered
by the `Open Telekom Cloud`_. The OTC Extensions serve two purposes:
Firstly, they provide Python classes and methods to attach your own
code to the cloud. For example, `Ansible modules`_ use this
way. Secondly, the OTC Extensions automatically extend the `OpenStack
Client`_, the CLI tool to manage the OpenStack cloud.

Content
-------

This documentation is split into four sections, adressing major use
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

The :doc:`installation <install/index>` guide explains system
administrators and developers how to setup the project from operation
system packages, from pip, directly from sources and other
installation forms. OTC Extensions are very easy to
:doc:`configure <install/configuration>`. All credentials can be configured
in one or two files.


Working with the CLI tool
-------------------------

Users who want to access Open Telekom Cloud specific services with
:doc:`command line tools <cli/index>` for a shell like Bash find
documentation of all of their operations and properties in this section.


Writing your own Scripts for the Cloud
--------------------------------------

Developers, who plan to write own Python code, may access the API more
easily by using the OTC Extensions' classes and methods. The
:doc:`SDK interfaces <sdk/index>` are documented in this
section.


Contribute to the Project
-------------------------

Developers, who want to :doc:`contribute <contributor/index>` to the
project, find helpful background information and architecture
specification of OTC Extensions here.


General Information
-------------------

Adding to that, there is some general background information
available:

* In a :doc:`glossary <appendices/glossary>` important terms and their
  naming conventions are described.

* There is a :doc:`history <appendices/history>` explaing the ancestry
  of this project. This may or may not be insightful if you want to
  understand the projects architecture.

* There is a :doc:`release history <appendices/releasenotes>`
  available.

* A list of :doc:`issues <appendices/issues>` is maintained.

* Currently 13 services are :doc:`covered <coverage>` by the OTC
  extensions.

.. _OpenStack SDK: https://docs.openstack.org/openstacksdk/
.. _OpenStack API: https://docs.openstack.org/api-quick-start/
.. _Open Telekom Cloud: https://open-telekom-cloud.com/
.. _Ansible modules: https://github.com/OpenTelekomCloud/ansible-collections/
.. _OpenStack Client: https://docs.openstack.org/python-openstackclient/
