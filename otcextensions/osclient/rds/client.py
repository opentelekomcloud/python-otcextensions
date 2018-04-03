#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

import logging

from openstack import connection

# NOTE(agoncharov): Follow when OSC is not using profiles anymore
try:
    from openstack.config import loader as config   # noqa
    profile = None
except ImportError:
    from openstack import profile
from osc_lib import utils

from otcextensions.i18n import _

from otcextensions import sdk


LOG = logging.getLogger(__name__)

DEFAULT_API_VERSION = '1.0'
API_VERSION_OPTION = 'os_rds_api_version'
API_NAME = "rds"
API_VERSIONS = {
    "1.0": "openstack.connection.Connection",
    "1": "openstack.connection.Connection",
}


def make_client(instance):
    """Returns a rds proxy"""

    LOG.debug('Instantiating RDS Client: ')

    if getattr(instance, "sdk_connection", None) is None:
        if profile is None:
            # If the installed OpenStackSDK is new enough to not require a
            # Profile obejct and osc-lib is not new enough to have created
            # it for us, make an SDK Connection.
            # NOTE(agoncharov): This can be removed when this bit is in the
            #                released osc-lib in requirements.txt.
            conn = connection.Connection(
                config=instance._cli_options,
                session=instance.session,
            )
        else:
            # Fall back to the original Connection creation
            prof = profile.Profile()
            prof.set_region(API_NAME, instance.region_name)
            prof.set_version(API_NAME, instance._api_version[API_NAME])
            prof.set_interface(API_NAME, instance.interface)
            conn = connection.Connection(
                authenticator=instance.session.auth,
                verify=instance.session.verify,
                cert=instance.session.cert,
                profile=prof,
            )

        instance.sdk_connection = conn

    conn = instance.sdk_connection

    if getattr(conn, 'rds', None) is None:
        LOG.debug('OTC extensions are not registered. Do that now')
        sdk.register_otc_extensions(conn)

    LOG.debug('Connection: %s', conn)
    LOG.debug('RDS client initialized using OpenStack OTC SDK: %s',
              conn.rds)
    return conn.rds


def build_option_parser(parser):
    """Hook to add global options"""
    # parser.add_argument(
    #     '--os-rds-api-version',
    #     metavar='<rds-api-version>',
    #     default=utils.env('OS_RDS_API_VERSION'),
    #     help=_("RDS API version, default=%s "
    #            "(Env: OS_RDS_API_VERSION)") % DEFAULT_API_VERSION
    # )
    return parser
