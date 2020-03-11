Installation
============

.. toctree::
   :maxdepth: 3

   pip_install.rst
   source_install.rst

There are several ways to install OTC Extensions to enhance the native
OpenStack Client and to extend the OpenStack SDK to cover the
additional Open Telekom Cloud services providing a larger
functionality on top of OpenStack.

The easiest way is to use the Python pip installer which is working
distribution independent and can be used in an isolated virtual environment
as described below. Ansible can be used to install python-otcextensions on
various operating systems, too by using the following Ansible Role:
https://github.com/OpenTelekomCloud/ansible-role-otcextensions .
There are also ready-made installation packages for various operating
systems which have their own versions, package names and sometimes bugs.
A repository based on openSUSE's build services tries to cover these issues
which is available under:
https://build.opensuse.org/project/show/Cloud:OTC:Tools:OpenStack.

Overview of Related Packages
----------------------------

**OpenStack SDK:**
A library on the client side that translates Python function calls into
API calls to an OpenStack cloud.

**OpenStack Client:**
An application that turns the Python interface of OpenStack SDK and
OTC Extensions into a CLI tool.

**OTC Extensions:**
An addition to OpenStack SDK with enhanced functionality that is
specific for the Open Telekom Cloud. This is the package you are
currently looking at.
