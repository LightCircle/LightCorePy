import logging


# TODO: setup timezone,
# TODO: print user id
class Log:
    @staticmethod
    def init():
        logging.basicConfig(
            format='[%(asctime)s.%(msecs)03d] [A] [%(levelname)s] %(filename)s:%(lineno)d - - - - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            level=logging.DEBUG)
