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

from otcextensions import sdk


LOG = logging.getLogger(__name__)

DEFAULT_API_VERSION = '1'
API_VERSION_OPTION = 'os_sdrs_api_version'
API_NAME = "sdrs"
API_VERSIONS = {
    "1": "openstack.connection.Connection"
}


def make_client(instance):
    """Returns a SDRS proxy"""

    conn = instance.sdk_connection

    if getattr(conn, 'sdrs', None) is None:
        LOG.debug('OTC extensions are not registered. Do that now')
        sdk.register_otc_extensions(conn)

    LOG.debug('SDRS client initialized using OpenStack OTC SDK: %s',
              conn.sdrs)
    return conn.sdrs


def build_option_parser(parser):
    """Hook to add global options"""
    return parser
