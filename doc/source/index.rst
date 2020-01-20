Welcome to the OTC Extensions of the OpenStack SDK and CLI!
===========================================================

.. toctree::
   :includehidden:
   :maxdepth: 1

   Installation <install/index>
   CLI Usage <cli/index>
   Package Reference <user/index>
   Contributing <contributor/index>
   History <history>
   Glossary of Terms <glossary>
   Release Notes <releasenotes>
   Service Coverage <coverage>
   Potential Issues <issues>

Accessing the `OpenStack API`_ directly can be tedious. The `OpenStack
SDK`_ is a Python based client library that simplifies building
applications to work with OpenStack clouds. This project, OTC
Extensions, augments this SDK and adds extra functionality offered by
the `Open Telekom Cloud`_. The OTC Extensions serve two purposes:
Firstly, they provide Python classes and methods to attach your own
code to the cloud. For example, `Ansible modules`_ use this
way. Secondly, the OTC Extensions automatically extend the `OpenStack
Client`_, the CLI tool to manage the OpenStack cloud.

This documentation is split into four sections, adressing several use
cases:

* The :doc:`installation <install/index>` guide explains system
  administrators and developers how to setup the project from
  operation system packages, from pip, directly from sources and other
  installation forms. Configuration

* Users who want to access Open Telekom Cloud specific services with
  :doc:`command line tools <cli/index>` find documentation of all of
  their opetions and properties in this section.

* Developers, who plan to write own Python code, may access the API
  more easily by using the OTC Extensions' classes and methods. The
  :doc:`architecture and interfaces <user/index>` are documented in
  this section.
  
* Developers, who want to :doc:`contribute <contributor/index>` to the
  project find helpful background information.

General Information
-------------------

In a `glossary`_ important terms and their naming conventions are described.

There is a `history`_ explaing the ancestry of this project. This may
or may not be insightful if you want to understand the projects
architecture.

There is a `release history`_ available.

A list of `potential issues`_ is maintained.

Currently 13 services are `covered` by the OTC extensions.

.. _OpenStack SDK: https://docs.openstack.org/openstacksdk/
.. _OpenStack API: https://openstack.org/api-ref/
.. _Open Telekom Cloud: https://open-telekom-cloud.com/
.. _Ansible modules: https://github.com/OpenTelekomCloud/ansible-collections/
.. _OpenStack Client: https://docs.openstack.org/python-openstackclient/
.. _glossary: <glossary>
.. _history: <history>
.. _release history: <releasenotes>
.. _potential issues: <issues>
.. _covered: <coverage>
