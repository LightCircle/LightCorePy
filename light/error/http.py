class BadRequest(Exception):
    def __init__(self):
        self.code = 400
        self.message = 'Bad Request'


class InternalServerError(Exception):
    def __init__(self):
        self.code = 500
        self.message = 'Internal Server Error'
