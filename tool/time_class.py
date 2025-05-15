from datetime import datetime


class TimeClass:

    def __init__(self):
        self.now_time = datetime.now()

    def get_year(self):
        return self.now_time.year

    def get_month(self):
        return self.now_time.month

    def get_day(self):
        return self.now_time.day

time_class = TimeClass()