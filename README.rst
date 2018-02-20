OpenTelekomCloud extensions
===========================

OTCExtensions is a project to bring OTC extensions into the native OpenStack
toolstack. Covered are currently following items:
* `python-openstacksdk`
* `python-openstackclient`

The primary goal is to provide a possibility to use native OpenStack SDK and CLI

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


    import openstack
    from otcextensions import sdk

    conn = openstack.connect('otc') # Nave of the cloud from clouds.yaml config

    sdk.register_otc_extensions(conn) # Register OTC extensions in the OpenStackSDK

    obs = conn.obs # Get the OBS service proxy

    list(obs.buckets) # list the Buckets


Configuration
=============

The CLI is configured via environment variables and command-line
options as listed in  https://docs.openstack.org/python-openstackclient/latest/cli/authentication.html.

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
