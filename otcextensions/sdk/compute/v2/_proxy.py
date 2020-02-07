from openstack import proxy


class Proxy(proxy.Proxy):

    def test(self):
        return self.get('/')
        return 'some fake'
