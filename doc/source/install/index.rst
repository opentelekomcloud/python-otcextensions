Installation
============

There are several install options for OTC Extensions to enhance the
native `OpenStack Client`_ and to extend the `OpenStack SDK`_. Once
installed, they cover additional `Open Telekom Cloud`_ services and
provide extra functionality on top of the stock OpenStack SDK and CLI.

.. toctree::
   :maxdepth: 3

   pip_install
   source_install

Overview of Related Packages
----------------------------

The OTC Extensions are, as most software in OpenStack, written in
Python and are eventually a Python package. These packages come with
dependencies to other packages. Usually a package manager such as pip
is used to resolve those dependencies or all requirements are bundled
in a single packet. These are the main packages and their relations to
each other:

**OpenStack SDK:** A library on the client side that translates Python
function calls into API calls to an OpenStack cloud. It depends only
on other, internal Python packages.

**OpenStack Client:** An application that turns the Python interface
of OpenStack SDK and OTC Extensions into a CLI tool. If installed, it
requires the SDK.

**OTC Extensions:** An addition to OpenStack SDK with enhanced
functionality that is specific for the Open Telekom Cloud. This is the
package you are currently looking at. It requires the SDK since it
extends its interfaces. If it is installed as a Python package it is
detected and integrated automatically by the other two packages
without further installation or configuration.

So effectively, using a package manager like pip it is sufficient to
install the packages like this:

.. code-block::

  $ pip install openstackclient otcextensions

Other packaging methods may or may not have these dependencies built
in already.


Installation Options
--------------------

There are a number of alternatives available to install OTC Extensions
(including the SDK and CLI):

* **Installing from operating system packages (deb, rpm, yum, dnf):**
  This is a very easy way that is also easy to revert. The downside of
  this aproach is that operating system packages for the major
  distributions are often quite outdated, as many of the internal
  dependencies are also often outdated. You often experience a backlog
  of several months up to years behind the latest development.

* **Installing with a Python package manager (pip):** Python comes
  with its own package manager `pip` for the `Python Package Index
  (PyPI)`_. That is today the standard way to install Python
  packages. All other described options use this method under the
  hood. This way is operating system independent. Installing with
  `pip` comes with three sub-options: Installing system-wide, for a
  single user, or inside a virtual environemt. **This is the
  recommended way to install OTC Extensions.**

* **Installing from sources:** All related projects are hosted on
  public source code repositories. So if you need a bleeding edge
  feature or want to contribute directly to the project yourself,
  installation from sources is for you. It requires some extra steps,
  though.

There are also ready-made installation packages for various operating
systems which have their own versions, package names and sometimes
bugs.  A repository based on openSUSE's build services tries to cover
these issues which is available under:
https://build.opensuse.org/project/show/Cloud:OTC:Tools:OpenStack.

.. _OpenStack SDK: https://docs.openstack.org/openstacksdk/
.. _OpenStack Client: https://docs.openstack.org/python-openstackclient/
.. _Open Telekom Cloud: https://open-telekom-cloud.com/
.. _Python Package Index (PyPI): https://pypi.org/
