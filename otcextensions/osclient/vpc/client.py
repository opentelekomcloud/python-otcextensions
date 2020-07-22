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

from osc_lib import utils

from otcextensions import sdk
from otcextensions.i18n import _

LOG = logging.getLogger(__name__)

DEFAULT_API_VERSION = '2'
API_VERSION_OPTION = 'os_vpc_api_version'
API_NAME = "vpc"
API_VERSIONS = {
    "2": "openstack.connection.Connection"
}


def make_client(instance):
    """Returns a vpc proxy"""

    conn = instance.sdk_connection

    if getattr(conn, 'vpc', None) is None:
        LOG.debug('OTC extensions are not registered. Do that now')
        sdk.register_otc_extensions(conn)

    LOG.debug('VPC client initialized using OpenStack OTC SDK: %s',
              conn.vpc)
    return conn.vpc


def build_option_parser(parser):
    """Hook to add global options"""
    parser.add_argument(
        '--os-vpc-api-version',
        metavar='<vpc-api-version>',
        default=utils.env('OS_VPC_API_VERSION'),
        help=_("VPC API version, default=%s "
               "(Env: OS_VPC_API_VERSION)") % DEFAULT_API_VERSION
    )
    return parser
