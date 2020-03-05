Configuration for the Cloud Connection
======================================

You can connect to the Open Telekom Cloud and OpenStack clouds in general
using two approaches. The first one uses a credential file called
``clouds.yaml`` and the other one is to use environment variables.

Configuring a clouds.yaml file
------------------------------

The credential file clouds.yaml will be queried automatically in different
locations with increasing precedence:

1. system-wide (/etc/openstack/{clouds,secure}.yaml)
2. Home directory / user space (~/.config/openstack/{clouds,secure}.yaml)
3. Current directory (./{clouds,secure}.yaml)

A sample clouds.yaml file is listed below to connect with Open Telekom Cloud:

**clouds.yaml**

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

The name otc is self-defined and can be changed. AK/SK values required for
access to some services (i.e. OBS) can be either configured as shown above
in the clouds.yaml/secure.yaml, or they can be automatically retrieved from
the S3_ACCESS_KEY_ID and S3_SECRET_ACCESS_KEY.

Additional connections to other Openstack-clouds or -projects can be added
to the file as shown below:

**clouds.yaml**

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
    otcsecondproject:
      region_name: eu-de
      auth:
        username: '<USERNAME2>'
        password: '<PASSWORD2>'
        project_id: '<PROJECT-ID2>'
        user_domain_id: '<DOMAIN-ID2>'
        auth_url: 'https://iam.eu-de.otc.t-systems.com:443/v3'

Test your connection
^^^^^^^^^^^^^^^^^^^^

Use the following command to test the basic functionality.

.. code-block:: bash

    $ openstack --os-cloud otc flavor list

Splitting the credentials in clouds.yaml and secure.yaml
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In some scenarios a split of security credentials from the configuration file
is necessary. The optional file ``secure.yaml`` can be used to store the
secret which is left out from ``clouds.yaml``:

**clouds.yaml**

.. code-block:: yaml

  clouds:
    otc:
      auth:
        username: 'USER_NAME'
        project_name: 'eu-de'
        auth_url: 'https://iam.eu-de.otc.t-systems.com:443/v3'
        user_domain_name: 'OTC00000000001000000xxx'
      interface: 'public'
      identity_api_version: 3 # !Important
      ak: 'AK_VALUE' # AK/SK pair for access to OBS
      sk: 'SK_VALUE'

**secure.yaml**

.. code-block:: yaml

  clouds:
    otc:
      auth:
        password: '<PASSWORD>'

Configuration of Environment Variables
--------------------------------------

Instead of using the clouds.yaml file, environmnt variables can be configured
to connect to the Open Telekom Cloud. Create a simple file like ``.ostackrc``
in the home directory and source the file to make the variables available. On
Open Telekom Cloud servers this file exists on bootup and needs to be changed
according to your credentials.

.. code-block:: bash

    $ export OS_AUTH_URL=<url-to-openstack-identity>
    $ export OS_IDENTITY_API_VERSION=3
    $ export OS_PROJECT_NAME=<project-name>
    $ export OS_PROJECT_DOMAIN_NAME=<project-domain-name>
    $ export OS_USERNAME=<username>
    $ export OS_USER_DOMAIN_NAME=<user-domain-name>
    $ export OS_PASSWORD=<password>  # (optional)
    $ export S3_ACCESS_KEY_ID=<access_key>
    $ export S3_SECRET_ACCESS_KEY=<secret_access_key>

Test your connection
^^^^^^^^^^^^^^^^^^^^

Use the following command to test the basic functionality.

.. code-block:: bash

    $ openstack flavor list
