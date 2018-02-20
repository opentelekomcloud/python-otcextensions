#   Copyright 2013 Nebula Inc.
#
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


def parse_s3_uri(s3path):
    bucket, path = '', ''
    if str(s3path) and s3path.startswith('s3://'):
        val = str(s3path).replace('s3://', '').split('/', 1)
        bucket = val[0]
        if len(val) > 1:
            path = val[1].strip('/')
        else:
            path = ""
    return bucket, path
