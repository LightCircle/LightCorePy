from light.model.datarider import Rider


class User(object):
    def __init__(self):
        self.rider = Rider.instance()

    def verify(self, handler):
        condition = {'condition': {'id': handler.params.id}}
        user = self.rider.user.get(handler.copy(condition))

        print('>>>>', user)
