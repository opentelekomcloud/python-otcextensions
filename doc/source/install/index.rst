============
Installation
============

Each OS version has it's own package names, versions, bugs. However there is a
repository, which tries to address those issues (at least for RPM based
distributions) -
https://build.opensuse.org/project/show/Cloud:OTC:Tools:OpenStack.  RPMs for
most often used OSs are prepared and can be taken there.

With a pip package can be installed the following way (please remember, it is
not the latest development state). At the command line::

    $ sudo yum install python-pip
    $ sudo pip install otcextensions --upgrade

Or, if you have virtualenv wrapper installed (more suitable for development)::

    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install otcextensions
    $ python setup.py install

A more reliable and at the moment tested way is a "developer" approach with a
latest state:

The project could be installed following way:

* clone git repo
* create virtual env `virtualenv venv && source vent/bin/activate`
* install project dependencies into the virtualenv `pip install -r
  requirements.txt`
* alternatively, instead of creating virtual env and installing requirements
  use tox venv manager `tox -e py36`
* register CLI plugin using `python setup.py install_egg_info` or alternatively
  install project into venv `python setup.py install`

Note
====

Ensure you have pip package installed. In the CentOS it is for example
`python-pip`, in Fedora it is better to use `python3` overall with
`python3-pip`, `python3-virtualenv` (or `python3-tox`)
