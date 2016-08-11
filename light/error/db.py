class NotExist(Exception):
    def __init__(self):
        self.code = 'D1004'
        self.message = 'Not Exist'


class NotCorrect(Exception):
    def __init__(self):
        self.code = 'D1006'
        self.message = 'Not Correct'
