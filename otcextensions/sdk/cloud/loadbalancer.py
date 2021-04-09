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


class LoadBalancerMixin:

    def list_elbv2_load_balancers(self, **query):
        result = []
        for lb in self.elb.load_balancers(**query):
            result.append(lb)
        return result

    def find_elbv2_load_balancer(self, name_or_id, ignore_missing=True):
        return self.elb.find_load_balancer(
            name_or_id=name_or_id,
            ignore_missing=ignore_missing
        )

    def create_elbv2_load_balancer(self, **attrs):
        return self.elb.create_load_balancer(**attrs)

    def update_elbv2_load_balancer(self, current_lb, **attrs):
        return self.elb.update_load_balancer(current_lb, **attrs)

    def delete_elbv2_load_balancer(self, name_or_id, cascade=False):
        lb = self.elb.find_load_balancer(name_or_id, ignore_missing=True)
        if lb:
            self.elb.delete_load_balancer(lb, cascade=cascade)
            return True
        else:
            return False

    def list_elbv2_listeners(self, **query):
        result = []
        for lsnr in self.elb.listeners(**query):
            result.append(lsnr)
        return result

    def list_elbv3_load_balancers(self, **query):
        result = []
        for lb in self.vlb.load_balancers(**query):
            result.append(lb)
        return result

    def list_elbv3_listeners(self, **query):
        result = []
        for lb in self.vlb.listeners(**query):
            result.append(lb)
        return result

    def find_elbv2_listener(self, name_or_id, ignore_missing=True):
        lsnr = self.elb.find_listener(
            name_or_id=name_or_id,
            ignore_missing=ignore_missing
        )
        return lsnr

    def create_elbv2_listener(self, **attrs):
        return self.elb.create_listener(**attrs)

    def update_elbv2_listener(self, current, **attrs):
        return self.elb.update_listener(current, **attrs)

    def delete_elbv2_listener(self, name_or_id):
        lsnr = self.elb.find_listener(name_or_id, ignore_missing=True)
        if lsnr:
            self.elb.delete_listener(lsnr)
            return True
        else:
            return False
