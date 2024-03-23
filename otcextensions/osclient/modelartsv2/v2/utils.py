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
from cliff import columns as cliff_columns

DATASET_TYPES_VALUE_MAP = {
    0: "image classification",
    1: "object detection",
    100: "text classification",
    101: "named entity recognition",
    102: "text triplet",
    200: "sound classification",
    201: "speech content",
    202: "speech paragraph labeling",
    400: "table dataset",
    600: "video labeling",
    900: "custom format",
}

DATASET_STATUS_VALUE_MAP = {
    0: "creating dataset",
    1: "normal dataset",
    2: "deleting dataset",
    3: "deleted dataset",
    4: "abnormal dataset",
    5: "synchronizing dataset",
    6: "releasing dataset",
    7: "dataset in version switching",
    8: "importing dataset",
}

SAMPLE_TYPES_VALUE_MAP = {
    0: "Image",
    1: "Text",
    2: "Speech",
    4: "Table",
    6: "Video",
    9: "Custom_Format",
}


class DatasetType(cliff_columns.FormattableColumn):
    def human_readable(self):
        return DATASET_TYPES_VALUE_MAP.get(self._value, str(self._value))


class DatasetStatus(cliff_columns.FormattableColumn):
    def human_readable(self):
        return DATASET_STATUS_VALUE_MAP.get(self._value, str(self._value))


class SampleType(cliff_columns.FormattableColumn):
    def human_readable(self):
        return SAMPLE_TYPES_VALUE_MAP.get(self._value, str(self._value))
