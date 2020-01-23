import re
import os
from datetime import datetime
import matplotlib.pyplot as plt
import timeit
import pandas as pd
import seaborn as sns


class Simulation:
    def __init__(self, filenames):
        
        self.fake_total_stopped_time = []
        self.idle_start_time = 0
        self.time_diff = 100
        self.delay = 3
        self.count = 0
        self.openFile()

    def getDatetime(self, time):
        date_time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
        return datetime.timestamp(date_time)

    def openFile(self):
        inRange = False
        changed = False
        inIdle = False
        inRun = False
        with open('runtime_test.txt') as f3:
            for line in f3:
                time = self.getDatetime(line.split(',')[0])
                if inRange and "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line:
                    # modify time here and ()
                    self.count += 1
                    current_time = self.fake_idle_start_time + self.delay
                    print(current_time, self.fake_idle_start_time)
                    changed = True
                    inRange = False
                    # break

                if "SCANNER RUNNING message" in line:
                    if not changed:
                        self.fake_idle_end_time = time
                    else:
                        self.fake_idle_end_time = current_time + (time - last_time)
                    self.time_diff = self.fake_idle_end_time - self.fake_idle_start_time
                    self.fake_total_stopped_time += self.time_diff,
                    inRange = False
                    inRun = True

                elif "SCANNER IDLE message and disabling RTR" in line:
                    if not changed:
                        self.fake_idle_start_time = time
                    else:
                        self.fake_idle_start_time = current_time + (time - last_time)
                    inRange = False
                    inIdle = True

                if (inIdle and inRun) and self.time_diff < 3:  # within the range, add delay to next conveyor running (idle_start_time + 3s)
                    inRange = True
                    print("in time diff: ", self.fake_idle_start_time)
                    # changed = True
                last_time = self.getDatetime(line.split(',')[0])


if __name__ == '__main__':
    s = Simulation(['C:/Users/wzhong/Documents/temp/logfiles/AnalogicStandaloneType2_20190623.log'])
     # print(line.replace(text_to_search, replacement_text), end='')
