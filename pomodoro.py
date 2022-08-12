import datetime
from time import sleep

class Pomodoro(object):

    def __init__(self, work_time=25, break_time=5, cycles=1):
        self.work_time = work_time
        self.break_time = break_time
        self.cycles = cycles

    def start(self):
        for i in range(self.cycles):
            now = datetime.datetime.now()
            work_period = datetime.timedelta(seconds=self.work_time)
            break_period = datetime.timedelta(seconds=self.break_time)
            end_work_time = now + work_period
            end_break_time = end_work_time + break_period
            while (now:=datetime.datetime.now()) < end_work_time:
                print(f"time left working: {(end_work_time - now).seconds} seconds")
                sleep(1)
            while (now:=datetime.datetime.now()) < end_break_time:
                print(f"time left in break: {(end_break_time - now).seconds} seconds")
                sleep(1)
            print(f"completed cycle {i+1}/{self.cycles}")
        print("Congratulations on accomplishing so much work!")

if __name__ == "__main__":
    p = Pomodoro(cycles=2, work_time=5, break_time=2)
    p.start()