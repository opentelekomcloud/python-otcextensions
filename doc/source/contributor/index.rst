Contributing to the OTC Extensions
==================================

This section of documentation pertains to those who wish to contribute to the
development of this project. If you're looking for documentation on how to use
the SDK to build applications, please see the `user <../user>`_ section.


Contribution Mechanics
----------------------

.. toctree::
   :maxdepth: 2

   contributing

Contacting the Developers
-------------------------

GitHub
******

Currently no official communication other than GitHub is available

Email
*****

???

Coding Standards
----------------

We are a bit stricter than usual in the coding standards department. It's a
good idea to read through the :doc:`coding <coding>` section.

.. toctree::
   :maxdepth: 2

   coding

Development Environment
-----------------------

The first step towards contributing code and documentation is to setup your
development environment. We use a pretty standard setup, but it is fully
documented in our :doc:`setup <setup>` section.

.. toctree::
   :maxdepth: 2

   setup

Testing
-------

The project contains three test packages, one for unit tests, one for
functional tests and one for examples tests. The ``openstack.tests.unit``
package tests the SDK's features in isolation. The
``openstack.tests.functional`` and ``openstack.tests.examples`` packages test
the SDK's features and examples against an OpenStack cloud.

.. toctree::

   testing

Project Layout
--------------

The project contains a top-level ``openstack`` package, which houses several
modules that form the foundation upon which each service's API is built on.
Under the ``openstack`` package are packages for each of those services,
such as ``openstack.compute``.

.. toctree::

   layout

Adding Features
---------------

Does this SDK not do what you need it to do? Is it missing a service? Are you
a developer on another project who wants to add their service? You're in the
right place. Below are examples of how to add new features to the
OpenStack SDK.

.. toctree::
   :maxdepth: 2

   create/resource

.. TODO(briancurtin): document how to create a proxy
.. TODO(briancurtin): document how to create auth plugins
