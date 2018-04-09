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

The very first step to get started is to install otcextensions into your system. For this please follow installation instructions_

.. _instructions: http://python-otcextensions.readthedocs.io/en/latest/install/index.html

Next step would be logically configuration

Configuration
=============

openstack.config
================

The recommended way, since it is the most efficient way to configure both SDK and the CLI in one place

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
        auth:
          username: 'USER_NAME'
          password: 'PASS'
          project_name: 'eu-de'
          auth_url: 'https://iam.eu-de.otc.t-systems.com:443/v3'
          user_domain_name: 'OTC00000000001000000xxx'
        interface: 'public'
        identity_api_version: 3 # !Important
        ak: 'AK_VALUE' # AK/SK pair for access to OBS
        sk: 'SK_VALUE'

Please note: ``openstack.config`` will look for a file called ``clouds.yaml``
in the following locations:

* Current Directory
* ``~/.config/openstack``
* ``/etc/openstack``

AK/SK values required for access to some services (i.e. OBS) can be either configured as shown above in the clouds.yaml/secure.yaml,
or they can be automatically retrieved from the S3_ACCESS_KEY_ID and S3_SECRET_ACCESS_KEY.
Values from the clouds.yaml/secure.yaml take precedence over the ones from environment.

With this configuration you can start using openstackCLI simply ``openstack --os-cloud otc``

More information at https://developer.openstack.org/sdks/python/openstacksdk/users/config

Old style way
=============

The CLI can be configured via environment variables and command-line
options as listed in https://docs.openstack.org/python-openstackclient/latest/cli/authentication.html or https://developer.openstack.org/sdks/python/openstacksdk/users/config.

Authentication using username/password is often used::

    export OS_AUTH_URL=<url-to-openstack-identity>
    export OS_IDENTITY_API_VERSION=3
    export OS_PROJECT_NAME=<project-name>
    export OS_PROJECT_DOMAIN_NAME=<project-domain-name>
    export OS_USERNAME=<username>
    export OS_USER_DOMAIN_NAME=<user-domain-name>
    export OS_PASSWORD=<password>  # (optional)
    export S3_ACCESS_KEY_ID=<access_key>
    export S3_SECRET_ACCESS_KEY=<secret_access_key>

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


Links
=====

* `Issue Tracker <https://github.com/OpenTelekomCloud/python-otcextensions/issues>`_
* `Documentation <http://python-otcextensions.readthedocs.io/en/latest/>`_
