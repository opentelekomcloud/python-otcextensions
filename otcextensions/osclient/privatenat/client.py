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

DEFAULT_API_VERSION = '3'
API_VERSION_OPTION = 'os_privatenat_api_version'
API_NAME = "privatenat"
API_VERSIONS = {
    "3": "openstack.connection.Connection"
}


def make_client(instance):
    """Returns a private NAT proxy"""
    conn = instance.sdk_connection

    if getattr(conn, 'natv3', None) is None:
        LOG.debug('OTC extensions are not registered. Do that now')
        sdk.register_otc_extensions(conn)

    LOG.debug('Private NAT client initialized using OpenStack OTC SDK: %s',
              conn.natv3)
    return conn.natv3


def build_option_parser(parser):
    """Hook to add global options"""
    parser.add_argument(
        '--os-privatenat-api-version',
        metavar='<privatenat-api-version>',
        default=utils.env('OS_PRIVATENAT_API_VERSION'),
        help=_("Private NAT API version, default=%s "
               "(Env: OS_PRIVATENAT_API_VERSION)") % DEFAULT_API_VERSION
    )
    return parser
