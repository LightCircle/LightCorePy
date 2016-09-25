class BadRequest(Exception):
    def __init__(self):
        self.code = 400
        self.message = 'Bad Request'
