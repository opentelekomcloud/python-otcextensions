Contributing to the OTC Extensions
==================================

This section of the documentation is intended for those who want to
contribute to the development of the OTC Extensions. If you're looking
for documentation on how to use the SDK to build applications, please
see the `SDK <../sdk>`_ section.


Setting up an Development Environment
-------------------------------------

The first step towards contributing code and documentation is to setup
your development environment. The project implements a pretty standard
setup. It is fully documented in the :doc:`setup <setup>` section.

.. toctree::
   :maxdepth: 2

   setup


Project Layout
--------------

The project contains a top-level ``otcextensions`` package, which houses
several modules that form the foundation upon which each service's API is
built on. Under the ``otcextensions`` package are packages for the
``sdk``, the ``osclient`` (OpenStackClient / CLI) and the related ``tests``
of each service implementation. Inside of those directories, the custom
created services such as ``Cloud Container Engine (CCE)`` are hosted.

.. toctree::

   layout


Coding Standards
----------------

We are a bit stricter than usual in the coding standards
department. It's a good idea to read through the :doc:`coding
<coding>` section.

.. toctree::
   :maxdepth: 2

   coding


Testing
-------

The project contains three test packages, one for unit tests, one for
functional tests and one for examples tests. The
``openstack.tests.unit`` package tests the SDK's features in
isolation. The ``openstack.tests.functional`` and
``openstack.tests.examples`` packages test the SDK's features and
examples against an OpenStack cloud.

.. toctree::

   testing


Example SDK Service and Resource Implementation
-----------------------------------------------

Do the OTC Extensions not do what you need them to do? Are they
missing a service? Are you a developer on another project who wants to
add a service? You're in the right place. Below are examples of how to
add new features to the project.

.. toctree::
   :maxdepth: 2

   create/resource


Contacting the OTC Extensions Developers
----------------------------------------

Currently no official communication other than `GitHub
<https://github.com/opentelekomcloud/python-otcextensions>`_ is
available.  Feel free to open new issues if you want to contact us
directly or have questions related to the existent packages.
