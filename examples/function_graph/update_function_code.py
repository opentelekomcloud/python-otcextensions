#!/usr/bin/env python3
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
"""
Update function code
"""
import openstack
from otcextensions import sdk

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')
sdk.register_otc_extensions(conn)

code_attrs = {
    'code_filename': 'index.zip',
    'code_type': 'inline',
    'func_code': {
        'file': 'UEsDBAoAAAAIAPQ1M1gNImPLrAAAAAEBAAAIAAAAaW5kZXgucHlN'
                'jtEOgjAMRd/5igVfxDAlxhjDo0S/wB+YrMgMdMvWGYnh390wEfrU'
                '3nvb0xXjG85qLRU+Sk8NP0UhUb3RltjTaUwkNKwVKDuwbA0vQMrD'
                'AhK8KSsTFsoCeYvsMw2xUkeCvKu0hLRk+6LIZ0u5s3BwPFwwUEEG'
                '/yo6B4vEXcshyBG+lb437kfNFpEWhATrQmqGTkYVH0Pit8FEdCqM'
                '6VQtSGncxYPpPz5O3fgFUEsBAh4DCgAAAAgA9DUzWA0iY8usAAAA'
                'AQEAAAgAAAAAAAAAAAAAAPMCAAAAAGluZGV4LnB5UEsFBgAAAAAB'
                'AAEANgAAANIAAAAAAA=='
    }
}
code = conn.functiongraph.update_function_code("func_urn", **code_attrs)
