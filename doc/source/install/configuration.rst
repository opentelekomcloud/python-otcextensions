Configuration
=============

You can connect to the Open Telekom Cloud and OpenStack clouds in general
using two approaches. The first one uses a credential file called
``clouds.yaml`` and the other one is to use ``environment variables``.

.. _clouds-yaml:

Configuring a clouds.yaml file
------------------------------

The credential file ``clouds.yaml`` will be queried automatically in different
locations with increasing precedence:

1. system-wide (/etc/openstack/{clouds,secure}.yaml)
2. Home directory / user space (~/.config/openstack/{clouds,secure}.yaml)
3. Current directory (./{clouds,secure}.yaml)

A sample clouds.yaml file is listed below to connect with Open Telekom Cloud:

**clouds.yaml**

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

.. note::
   The name ``otc`` is self-defined and can be changed to any value.

AK/SK values required for access to some services (i.e. OBS) can
be either configured as shown above in the clouds.yaml/secure.yaml, or
they can be automatically retrieved from the S3_ACCESS_KEY_ID and
S3_SECRET_ACCESS_KEY.

Test your connection
^^^^^^^^^^^^^^^^^^^^

If you followed the :doc:`installation advices </install/index>`
for your specific  operating system, you can use the following
command to test the basic functionality.

.. code-block:: bash

    $ openstack --os-cloud otc flavor list


Configuration of a Second Project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Additional connections to other Openstack-clouds or -projects can be added
to the file as shown below:

**clouds.yaml**

.. code-block:: yaml

  clouds:
    otcfirstproject:
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
    otcsecondproject:
      profile: otc
      auth:
       username: '<USER_NAME>'
        password: '<PASSWORD>'
        project_name: '<eu-de_project2>'
        # or project_id: '<123456_PROJECT_ID2>'
        user_domain_name: 'OTC00000000001000000xxx'
        # or user_domain_id: '<123456_DOMAIN_ID2>'
        auth_url: 'https://iam.eu-de.otc.t-systems.com:443/v3'
      interface: 'public'
      identity_api_version: 3 # !Important
      ak: '<AK_VALUE>' # AK/SK pair for access to OBS
      sk: '<SK_VALUE>'

Splitting the credentials in clouds.yaml and secure.yaml
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In some scenarios a split of security credentials from the configuration file
is necessary. The optional file ``secure.yaml`` can be used to store the
secret which is left out from ``clouds.yaml``:

**clouds.yaml**

.. code-block:: yaml

  clouds:
    otc:
      profile: otc
      auth:
        username: '<USER_NAME>'
        project_name: '<eu-de_project>'
        # or project_id: '<123456_PROJECT_ID>'
        user_domain_name: 'OTC00000000001000000xxx'
        # or user_domain_id: '<123456_DOMAIN_ID>'
        auth_url: 'https://iam.eu-de.otc.t-systems.com:443/v3'
      interface: 'public'
      identity_api_version: 3 # !Important
      ak: '<AK_VALUE>' # AK/SK pair for access to OBS
      sk: '<SK_VALUE>'

**secure.yaml**

.. code-block:: yaml

  clouds:
    otc:
      auth:
        password: '<PASSWORD>'

.. _environment-variables:

Agency based authorization
^^^^^^^^^^^^^^^^^^^^^^^^^^

Open Telekom Cloud supports a concept of agencies. One domain delegates access
to resources to another domain. After trust relationship is established the
following configuration can be used in ``clouds.yaml``:

.. code-block:: yaml

  clouds:
    otc:
      profile: otc
      auth_type: agency
      auth:
        username: '<USER_NAME>'
        project_name: '<eu-de_project>'
        # or project_id: '<123456_PROJECT_ID>'
        user_domain_name: 'OTC00000000001000000xxx'
        # or user_domain_id: '<123456_DOMAIN_ID>'
        auth_url: 'https://iam.eu-de.otc.t-systems.com:443/v3'
        target_domain_id: '<123456_DOMAIN_ID>' # Domain where agency is created
        # or target_domain_name: '<123456_DOMAIN_NAME'
        target_agency_name: 'test_agency' # name of the agency
        target_project_name: '<123456_PROJECT_NAME>' # project scoped operations
        # or target_project_id: '<123456_PROJECT_ID>'
        # When target_project_xx is not set - domain scope is selected

Configuration of Environment Variables
--------------------------------------

Instead of using the clouds.yaml file, environmnt variables can be configured
to connect to the Open Telekom Cloud. Create a simple file like ``.ostackrc``
in the home directory and source the file to make the variables available. On
Open Telekom Cloud servers this file exists on bootup and needs to be changed
according to your credentials.

.. code-block:: bash

    # .ostackrc file
    export OS_USERNAME="<USER_NAME>"
    export OS_USER_DOMAIN_NAME=<OTC00000000001000000XYZ>
    export OS_PASSWORD=<PASSWORD> # optional
    export OS_TENANT_NAME=eu-de
    export OS_PROJECT_NAME=<eu-de_PROJECT_NAME>
    export OS_AUTH_URL=https://iam.eu-de.otc.t-systems.com:443/v3
    export NOVA_ENDPOINT_TYPE=publicURL
    export OS_ENDPOINT_TYPE=publicURL
    export CINDER_ENDPOINT_TYPE=publicURL
    export OS_VOLUME_API_VERSION=3
    export OS_IDENTITY_API_VERSION=3
    export OS_IMAGE_API_VERSION=2

Run the source command to make the ``environment variables`` available.

.. code-block:: bash

   $ source .ostackrc

The ``environment variables`` are now available for usage. For testing your
connection run the following command.

Test your connection
^^^^^^^^^^^^^^^^^^^^

If you followed the `installation advices <index>`_ for your specific
operating system, you can use the following command to test the basic
functionality.

.. code-block:: bash

    $ openstack flavor list

.. note::
   You don't need to specify the `--os-cloud` parameter when environment
   variables are used.
