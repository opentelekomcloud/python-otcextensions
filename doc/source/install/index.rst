============
Installation
============

Each OS version has it's own package names, versions, bugs. Therefore installation as RPM is available at the moment only for Fedora through CORP `<https://copr.fedorainfracloud.org/coprs/gtema/OTC/>`_

With a pip package can be installed the following way (please remember, it is not the latest development state). At the command line::

    $ pip install python-otcextensions


Or, if you have virtualenv wrapper installed::

    $ mkvirtualenv python-otcextensions
    $ pip install python-otcextensions

A more reliable and at the moment tested way is a "developer" approach with a latest state:

The project could be installed following way:

* clone git repo
* create virtual env `virtualenv venv && source vent/bin/activate`
* install project dependencies into the virtualenv `pip install -r requirements.txt`
* alternatively, instead of creating virtual env and installing requirements use tox venv manager `tox -e py36`
* register CLI plugin using `python setup.py install_egg_info` or alternatively install project into venv `python setup.py install`

Note
====

Ensure you have pip package installed. In the CentOS it is for example `python-pip`,
in Fedora it is better to use `python3` overall with `python3-pip`, `python3-virtualenv` (or `python3-tox`)
