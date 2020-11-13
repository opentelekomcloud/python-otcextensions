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

DEFAULT_API_VERSION = '3'
API_VERSION_OPTION = 'os_identity_api_version'
API_NAME = "identity"
API_VERSIONS = {
    "3": "openstack.connection.Connection",
}


def make_client(instance):
    """Returns a identity proxy"""

    conn = instance.sdk_connection

    # register unconditionally, since we need to override default DNS
    sdk.register_otc_extensions(conn)

    LOG.debug('identity client initialized using OpenStack OTC SDK: %s',
              conn.identity)
    return conn.identity


def build_option_parser(parser):
    """Hook to add global options"""
    return parser
