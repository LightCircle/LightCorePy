import flask


class Context(object):
    def __init__(self, uid=None, domain=None, code=None, param=None):
        self._uid = uid
        self._domain = domain
        self._code = code
        self._user = None
        self._params = Params()

        # If uid is specified, then that is created manually
        if not uid:
            self.req = flask.request
            self.session = flask.session

        if param is not None:
            self._params = Params(param)
        else:
            self._params = Params(flask.request.values.to_dict(), flask.request.get_json())

    def copy(self, params):
        handler = Context(param=params)
        handler.set_uid(self._uid)
        handler.set_domain(self._domain)
        handler.set_code(self._code)
        return handler

    def get_params(self):
        return self._params

    def add_params(self, key, val):
        self._params[key] = val

    def remove_params(self, key):
        if key in self._params:
            del self._params[key]

    def extend_params(self, objects):
        self._params.update(objects)

    params = property(fget=get_params)

    def get_uid(self):
        if self._uid:
            return self._uid

        if self.user:
            return self.user['_id']

        return self._uid

    def set_uid(self, uid):
        self._uid = uid

    uid = property(fget=get_uid, fset=set_uid)

    def get_domain(self):
        if self._domain:
            return self._domain

        if self.session:
            return self.session['domain']

        return self._domain

    def set_domain(self, domain):
        self._domain = domain

    domain = property(fget=get_domain, fset=set_domain)

    def get_code(self):
        if self._code:
            return self._code

        if self.session:
            return self.session['code']

        return self._code

    def set_code(self, code):
        self._code = code

    code = property(fget=get_code, fset=set_code)

    def get_user(self):
        if self._user:
            return self._user

        if self.session:
            return self.session['user']

        return self._user

    def set_user(self, user):
        self._user = user

    user = property(fget=get_user, fset=set_user)


class Params(object):
    def __init__(self, values=None, data=None):
        self.values = {}
        if values:
            self.values = values
        if data:
            self.values.update(data)

    def __getattr__(self, key):
        if key in self.values:
            return self.values[key]
        return None
