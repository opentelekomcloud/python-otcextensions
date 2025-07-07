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
Create the AppCode
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')
attrs = {
    "app_code": "GjOD3g80AABuuFeEJpVQADBlAjBh3UzC7W+gr4V"
                "JBB5BtJ4fdVOQoSvoji3gFxUDb5pWBz9wUcw9+8"
                "/bFZ1B/4pq29wCMQC0pQWX6zTndljDEl99As1pw+"
                "WntAU9xcq+ffagoH6zDpKUvdxV6Ezj8LcCcPZN6BU="
}
created = conn.apig.create_app_code(gateway='gateway_id',
                                    app='app_id',
                                    **attrs)
