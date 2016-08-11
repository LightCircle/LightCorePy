from light.model.datarider import Rider
from light.error.db import NotExist, NotCorrect
from light.crypto import Crypto
from light.configuration import Config


class User(object):
    def __init__(self):
        self.rider = Rider.instance()

    def verify(self, handler):
        condition = {'condition': {'id': handler.params.id}}
        user = self.rider.user.get(handler.copy(condition))

        if user is None:
            return None, NotExist()

        password = handler.params.password
        hmackey = handler.params.hmackey
        if not hmackey:
            hmackey = Config.instance().app.hmackey

        if user['password'] != Crypto.sha256(password, hmackey):
            return None, NotCorrect()

        del user['password']
        return user, None
