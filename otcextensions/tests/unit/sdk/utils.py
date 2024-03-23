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
#


def assert_attributes_equal(test_case, sot, data):
    if isinstance(data, dict):
        try:
            test_case.assertEqual(sot, data)
        except AssertionError:
            for k, v in data.items():
                if isinstance(v, list):
                    assert_attributes_equal(test_case, getattr(sot, k), v)
                else:
                    try:
                        test_case.assertEqual(getattr(sot, k), v)
                    except AssertionError:
                        assert_attributes_equal(test_case, getattr(sot, k), v)
    elif isinstance(data, list):
        try:
            test_case.assertEqual(sot, data)
        except AssertionError:
            for ix, list_data in enumerate(data):
                assert_attributes_equal(test_case, sot[ix], list_data)
