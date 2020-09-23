OTC Extensions
==============

.. image:: https://travis-ci.org/OpenTelekomCloud/python-otcextensions.svg?branch=master
    :target: https://travis-ci.org/OpenTelekomCloud/python-otcextensions

.. image:: https://readthedocs.org/projects/python-otcextensions/badge/?version=latest
    :target: http://python-otcextensions.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

The OTC Extensions augment the OpenStack SDK of features and services
provided by the Open Telekom Cloud. If installed as a Python package,
they add several extra commands to the OpenStack Client CLI. Therefore
the project interacts closely with the

* `python-openstacksdk`
* `python-openstackclient`

packages.

Documentation
-------------

`Documentation Overview <http://python-otcextensions.readthedocs.io/en/latest/>`_

Installation
------------

`Installation Page <https://python-otcextensions.readthedocs.io/en/latest/install/index.html>`_

The OTC Extensions are hosted as the package `otcextensions` on PyPI
and can be installed by pip as

.. code-block: console

   $ pip install otcextensions

There are several options
to do that including but not limited to pip userland installation, system wide
installation as well as installation from operating system packets or directly
from source. Refer to the installation instructions_ in the projects
documentation.

Configuration
-------------

`Configuration Page <https://python-otcextensions.readthedocs.io/en/latest/install/configuration.html>`_

Acessing the Open Telekom Cloud APIs requires authentication and
authorization. For both there are several options available:

* **Configuration files** (recommended): A file called `clouds.yaml`
  holds all necessary configuration parameters. The file can be placed
  either in the local directory, below the user home directory in
  `.config/openstack` or in the system-wide directory
  `/etc/openstack`. You may use a second file `secure.yaml` in the
  same directories to extra protect clear-text password
  credentials. For more details see the section `configuration`_ in
  the official documentation.

  Minimal sample ``clouds.yaml`` file:

  .. code-block:: yaml

    clouds:
      otc:
        profile: otc
        auth:
          username: '<USER_NAME>'
          password: '<PASSWORD>'
          project_name: '<eu-de_project>'
          # or project_id: '<123456_PROJECT_ID>'
          user_domain_name: 'OTC00000000001000000xxx'
          # or user_domain_id: '<123456_DOMAIN_ID>'
          auth_url: 'https://iam.eu-de.otc.t-systems.com:443/v3'
        interface: 'public'
        identity_api_version: 3 # !Important
        ak: '<AK_VALUE>' # AK/SK pair for access to OBS
        sk: '<SK_VALUE>'

  With this configuration you can start using the CLI with ``openstack
  --os-cloud otc *command*`` or by ``export OS_CLOUD=otc; openstack
  *command*``.

* **Environment variables:** Authentication using username/password is often
  used::

    export OS_AUTH_URL=<url-to-openstack-identity>
    export OS_IDENTITY_API_VERSION=3
    export OS_PROJECT_NAME=<project-name>
    export OS_PROJECT_DOMAIN_NAME=<project-domain-name>
    export OS_USERNAME=<username>
    export OS_USER_DOMAIN_NAME=<user-domain-name>
    export OS_PASSWORD=<password>  # (optional)
    export S3_ACCESS_KEY_ID=<access_key>
    export S3_SECRET_ACCESS_KEY=<secret_access_key>

* **Command-Line Options:** The corresponding command-line options look
  very similar::

    --os-auth-url <url>
    --os-identity-api-version 3
    --os-project-name <project-name>
    --os-project-domain-name <project-domain-name>
    --os-username <username>
    --os-user-domain-name <user-domain-name>
    [--os-password <password>]

    If a password is not provided above (in plaintext), you will be
    interactively prompted to provide one securely.

* **Existing Token:** Authentication may also be performed using an
  already-acquired token and a URL pointing directly to the service
  API that presumably was acquired from the Service Catalog::

    export OS_TOKEN=<token>
    export OS_URL=<url-to-openstack-service>

* The corresponding command-line options look very similar::

    --os-token <token>
    --os-url <url-to-openstack-service>

In addition to that a regular `clouds.yaml` configuration file can be used

More information is available at
https://docs.openstack.org/python-openstackclient/latest/cli/authentication.html
or
https://developer.openstack.org/sdks/python/openstacksdk/users/config

OTC Extensions CLI Usage
------------------------

`OTCE CLI Command Overview <https://python-otcextensions.readthedocs.io/en/latest/cli/index.html>`_

OTC Extensions SDK Guides
-------------------------

`OTCE SDK Guides <https://python-otcextensions.readthedocs.io/en/latest/sdk/guides/index.html>`_

Contributing
------------

* `Contribution Page <https://python-otcextensions.readthedocs.io/en/latest/contributor/index.html>`_

Further Links
-------------

* `Issue Tracker <https://github.com/OpenTelekomCloud/python-otcextensions/issues>`_

.. _instructions: http://python-otcextensions.readthedocs.io/en/latest/install/
