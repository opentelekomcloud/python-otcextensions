============
Installation
============

As of now no pip package exist, therefore the project could be installed following way:

* clone git repo
* create virtual env `virtualenv venv && source vent/bin/activate`
* install project dependencies into the virtualenv `pip install -r requirements.txt`
* alternatively, instead of creating virtual env and installing requirements use tox venv manager `tox -e py36`
* register CLI plugin using `python setup.py install_egg_info` or alternatively install project into venv `python setup.py install`

At the command line::

    $ pip install python-otcextensions

Or, if you have virtualenv wrapper installed::

    $ mkvirtualenv python-otcextensions
    $ pip install python-otcextensions
