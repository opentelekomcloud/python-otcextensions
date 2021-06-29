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
from openstack import proxy

from otcextensions.sdk.dds.v3 import datastore as _datastore


class Proxy(proxy.Proxy):
    skip_discovery = True

    # ======= Datastores =======
    def datastore_types(self):
        """List supported datastore types

        :returns: A generator of supported datastore types
        """
        for ds in ['DDS-Community']:
            obj = type('obj', (object, ), {'name': ds})
            yield obj

    def datastores(self, datastore_name):
        """List datastores

        :param database_name: database store name
            (currently only DDS-Community and is case-sensitive.)

        :returns: A generator of supported datastore versions.

        :rtype: :class:`~otcextensions.sdk.dds.v3.datastore.Datastore`
        """
        return self._list(
            _datastore.Datastore,
            datastore_name=datastore_name,
        )
