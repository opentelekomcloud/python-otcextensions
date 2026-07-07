# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import time

from openstack import exceptions as sdk_exceptions
from otcextensions.tests.functional import base


class TestSwr(base.BaseFunctionalTest):

    def setUp(self):
        super(TestSwr, self).setUp()
        self.client = self.conn.swr

    def _create_organization(self, namespace, retries=3, delay=5):
        """Create an SWR organization, retrying on transient server errors.

        The SWR "create namespace" API occasionally returns a transient
        5xx (e.g. SVCSTG.SWR.5000059) under load; retry a few times
        before giving up.
        """
        for attempt in range(retries):
            try:
                return self.client.create_organization(namespace=namespace)
            except sdk_exceptions.HttpException as e:
                status = e.response.status_code if e.response is not None else None
                if not status or status < 500 or attempt == retries - 1:
                    raise
                time.sleep(delay)
