import flask
import os
import json
import logging

from light.http import unparam
from light.constant import Const


class Context(object):
    def __init__(self, uid=None, domain=None, code=None, param=None):
        self._uid = uid
        self._domain = domain
        self._code = code
        self._user = None
        self._params = Params()
        self._res = None
        self.req = None
        self.session = None

        # If uid is specified, then that is created manually
        if not uid:
            self.req = flask.request
            self.session = flask.session

        if param is not None:
            self._params = Params(param)
        else:
            self._params = Params(
                flask.request.form.to_dict(), unparam.query(), flask.request.get_json(), flask.request.files
            )

    def copy(self, params):
        handler = Context(param=params)
        handler.set_uid(self._uid)
        handler.set_domain(self._domain)
        handler.set_code(self._code)
        return handler

    def get_params(self):
        return self._params

    def set_params(self, objects):
        """
        Clear old content, create a new parameter
        :param objects:
        :return:
        """
        self._params = Params(objects)

    def add_params(self, key, val):
        self._params.add(key, val)

    def remove_params(self, key):
        self._params.remove(key)

    def extend_params(self, objects):
        self._params.update(objects)

    params = property(fget=get_params, fset=set_params)

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

        if self.session and 'domain' in self.session:
            return self.session['domain']

        return os.environ[Const().ENV_LIGHT_APP_DOMAIN]

    def set_domain(self, domain):
        self._domain = domain

    domain = property(fget=get_domain, fset=set_domain)

    def get_code(self):
        if self._code:
            return self._code

        if self.session and 'code' in self.session:
            return self.session['code']

        return self._code

    def set_code(self, code):
        self._code = code

    code = property(fget=get_code, fset=set_code)

    def get_res(self):
        if self._res is None:
            self._res = flask.Response()
        return self._res

    res = property(fget=get_res)

    def get_corp(self):
        if self.session and 'corp' in self.session:
            return self.session['corp']
        return None

    corp = property(fget=get_corp)

    def get_user(self):
        if self._user:
            return self._user

        if self.session and 'user' in self.session:
            return self.session['user']

        return self._user

    def set_user(self, user):
        self._user = user

    user = property(fget=get_user, fset=set_user)


class Params(object):
    def __init__(self, form=None, query=None, data=None, files=None):
        self.values = form or {}
        if query:
            self.values = query
        if data:
            if isinstance(data, dict):
                self.values.update(data)
            else:
                try:
                    self.values.update(json.loads(data))
                except ValueError or TypeError:
                    logging.error('Unable to parse the parameter.')
        if files:
            self.values['files'] = files.getlist('files')

    def __getattr__(self, key):
        if key in self.values:
            return self.values[key]
        return None

    def add(self, key, val):
        self.values[key] = val

    def update(self, data):
        self.values.update(data)

    def remove(self, key):
        if key in self.values:
            del self.values[key]
