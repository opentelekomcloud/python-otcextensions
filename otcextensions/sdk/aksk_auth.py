import abc
import six
from keystoneauth1.identity.v3 import base
from keystoneauth1 import plugin
from keystoneauth1 import loading


@six.add_metaclass(abc.ABCMeta)
class AkskAuth(base.BaseAuth):

    def __init__(self, **kwargs):
        print('_init %s' % kwargs)
        self.ak = None

    def get_auth_ref(self, session, **kwargs):
        print('get auth ref')
        pass

    def get_project_id(self, session, **kwargs):
        print('get project id')
        pass

    def get_headers(self, session, **kwargs):
        print('get headers')
        headers = {}
        return headers

    def get_endpoint(self, session, service_type=None, **kwargs):
        if (service_type is plugin.AUTH_INTERFACE
                or service_type.lower() == 'object'):
            return self.auth_url

        return None

    def get_token(self, session, **kwargs):
        print('get token %s' % kwargs)


class Aksk(loading.BaseV3Loader):
    @property
    def plugin_class(self):
        return AkskAuth

    def create_plugin(self, **kwargs):
        print('create plugin')
        return self.plugin_class(**kwargs)

    def get_options(self, **kwargs):
        options = super(Aksk, self).get_options()
        options.extend([
            loading.Opt('ak', required=True, prompt='AK:'),
            loading.Opt('secret', secret=True, prompt='Secret Key:', help='SK')
        ])
        print('get opts: %s' % options)
        return options

    def load_from_options(self, **kwargs):
        print('load from options %s' % kwargs)

        return super(Aksk, self).load_from_options(**kwargs)
