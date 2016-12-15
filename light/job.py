import atexit

from apscheduler.schedulers.background import BackgroundScheduler


class Schedule(object):
    def __init__(self):
        self.scheduler = BackgroundScheduler()

    def tick(self):
        pass

    def start(self):
        self.scheduler.add_job(self.tick, 'interval', seconds=3*60*60)
        self.scheduler.start()
        atexit.register(lambda: self.shutdown())

    def shutdown(self):
        self.scheduler.shutdown(wait=False)
