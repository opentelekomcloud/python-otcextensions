OpenTelekomCloud extensions
===========================

.. image:: https://travis-ci.org/OpenTelekomCloud/python-otcextensions.svg?branch=master
    :target: https://travis-ci.org/OpenTelekomCloud/python-otcextensions

.. image:: https://readthedocs.org/projects/python-otcextensions/badge/?version=latest
    :target: http://python-otcextensions.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

OTCExtensions is a project to bring OTC extensions into the native OpenStack
toolstack. Covered are currently following items:

* `python-openstacksdk`
* `python-openstackclient`

The primary goal is to provide a possibility to use native OpenStack SDK and CLI with the OTC additional services

Getting Started
===============

If you want to make changes to the OTCExtensions for testing and contribution,
make any changes and then run::

    python setup.py develop

or::

    pip install -e .

`tox` utility is used to unify tests and documentation generation


`python setup.py install_egg_info` command should be invoked to register
(provide specific data) itself for use by the `openstackclient` tool


In order to use SDK a following snippet can be used:

.. code-block:: python

    import openstack
    from otcextensions import sdk

    conn = openstack.connect('otc') # Nave of the cloud from clouds.yaml config
    sdk.register_otc_extensions(conn) # Register OTC extensions in the OpenStackSDK

    obs = conn.obs # Get the OBS service proxy

    list(obs.buckets) # list the Buckets


In order to use OTCExtensions plugin (development) in the openstackCLI the following can be done:

* create virtual environment (`virtualenv-3 venv`)
* source into the virtual env (`source venv/bin/activate`)
* install project dependencies including openstackCLI (`pip install -r requirements.txt`)
* install otcextensions entry_points into the environment (`python setup.py install_egg_info`)
* start using openstackclient (inside the virtual environment) as usual (`openstack --os-cloud otc rds instance list`)

Alternatively you can install otcextensions globally without virtual environment:

* `python setup.py install`


Configuration
=============

The CLI/SDK is configured via environment variables and command-line
options as listed in https://docs.openstack.org/python-openstackclient/latest/cli/authentication.html or https://developer.openstack.org/sdks/python/openstacksdk/users/config.

Authentication using username/password is most commonly used::

    export OS_AUTH_URL=<url-to-openstack-identity>
    export OS_IDENTITY_API_VERSION=3
    export OS_PROJECT_NAME=<project-name>
    export OS_PROJECT_DOMAIN_NAME=<project-domain-name>
    export OS_USERNAME=<username>
    export OS_USER_DOMAIN_NAME=<user-domain-name>
    export OS_PASSWORD=<password>  # (optional)

The corresponding command-line options look very similar::

    --os-auth-url <url>
    --os-identity-api-version 3
    --os-project-name <project-name>
    --os-project-domain-name <project-domain-name>
    --os-username <username>
    --os-user-domain-name <user-domain-name>
    [--os-password <password>]

If a password is not provided above (in plaintext), you will be interactively
prompted to provide one securely.

Authentication may also be performed using an already-acquired token
and a URL pointing directly to the service API that presumably was acquired
from the Service Catalog::

    export OS_TOKEN=<token>
    export OS_URL=<url-to-openstack-service>

The corresponding command-line options look very similar::

    --os-token <token>
    --os-url <url-to-openstack-service>

In addition to that a regular `clouds.yaml` configuration file can be used

openstack.config
================

``openstack.config`` will find cloud configuration for as few as 1 clouds and
as many as you want to put in a config file. It will read environment variables
and config files, and it also contains some vendor specific default values so
that you don't have to know extra info to use OpenStack

* If you have a config file, you will get the clouds listed in it
* If you have environment variables, you will get a cloud named `envvars`
* If you have neither, you will get a cloud named `defaults` with base defaults

Sometimes an example is nice.

Create a ``clouds.yaml`` file:

.. code-block:: yaml

     clouds:
      otc:
        region_name: Dallas
        auth:
          username: 'USER_NAME'
          password: 'PASS'
          project_name: 'eu-de'
          auth_url: 'https://iam.eu-de.otc.t-systems.com:443/v3'
          user_domain_name: 'OTC00000000001000000xxx'
        interface: 'public'
        identity_api_version: 3

Please note: ``openstack.config`` will look for a file called ``clouds.yaml``
in the following locations:

* Current Directory
* ``~/.config/openstack``
* ``/etc/openstack``

With this configuration you can start using openstackCLI simply ``openstack --os-cloud otc``

More information at https://developer.openstack.org/sdks/python/openstacksdk/users/config


Links
=====

* `Issue Tracker <https://github.com/OpenTelekomCloud/python-otcextensions/issues>`_
* `Documentation <http://python-otcextensions.readthedocs.io/en/latest/>`_
