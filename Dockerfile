# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM docker.io/opendevorg/python-builder:3.7 as builder

COPY . /tmp/src
RUN echo "python-openstackclient" >> /tmp/src/requirements.txt
RUN assemble

FROM docker.io/opendevorg/python-base:3.7

COPY --from=builder /output/ /output
RUN /output/install-from-bindep

# Trigger entrypoint loading to trigger stevedore entrypoint caching
RUN openstack --help >/dev/null 2>&1

CMD ["/usr/local/bin/openstack"]
