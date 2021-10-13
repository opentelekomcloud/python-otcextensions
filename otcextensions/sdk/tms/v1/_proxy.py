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
from otcextensions.sdk.tms.v1 import tag as _tag

from openstack import proxy


class Proxy(proxy.Proxy):

    def create_predefine_tag(self, **attrs):
        return self._create(_tag.Tag, **attrs)

    def delete_predefine_tag(self, tag, ignore_missing=True):
        return self._delete(_tag.Tag, tag, ignore_missing=ignore_missing)

    def query_predefine_tag(self, **attrs):
        return self._list(_tag.Tag, **attrs)

    def get_predefine_tag(self, tag):
        return self._get(_tag.Tag, tag)

    def modify_predefine_tag(self, **attrs):
        return self._update(_tag.Tag, **attrs)
