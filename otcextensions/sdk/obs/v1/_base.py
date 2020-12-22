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

from openstack import _log

from collections import defaultdict

from otcextensions.sdk import sdk_resource


_logger = _log.setup_logging('openstack')


class BaseResource(sdk_resource.Resource):
    OBS_NS = "http://obs.otc.t-systems.com/doc/2016-01-01/"

    @classmethod
    def etree_to_dict(cls, t):
        """Convert ETree to python dict
        """
        if cls.OBS_NS in t.tag:
            t.tag = t.tag.lstrip('{%s}' % (cls.OBS_NS))
        d = {t.tag: {} if t.attrib else None}
        children = list(t)
        if children:
            dd = defaultdict(list)
            for dc in map(cls.etree_to_dict, children):
                for k, v in dc.items():
                    dd[k].append(v)
            d = {t.tag: {k: v[0] if len(v) == 1 else v for k, v in dd.items()}}
        if t.attrib:
            d[t.tag].update(('@' + k, v) for k, v in t.attrib.items())
        if t.text:
            # strip spaces and quotes
            text = t.text.strip(' "')
            if children or t.attrib:
                if text:
                    d[t.tag]['#text'] = text
            else:
                d[t.tag] = text
        return d
