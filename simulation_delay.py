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

    def peek_line(self, f):
        pos = f.tell()
        line = f.readline()
        f.seek(pos)
        return line

    def openFile(self):
        inRange = False
        changed = False
        inIdle = False
        inRun = False
        total = []
        with open('runtime_test.txt') as f3:
            for line in f3:
                time = self.getDatetime(line.split(',')[0])
                if "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line and (inIdle and inRun):
                    # print("in scan", line)
                    if check_time <= 2:
                        diff = 2                     
                    else:
                        diff = time - start
                    # total.append((start, time, diff))
                    total.append(diff)
                    inRun = False
                    inIdle = False
                elif "SCANNER RUNNING message" in line:
                    check_time = time - start
                    #peek next line
                    # next_line = f3.readline()
                    # next_line = f3.peek()
                    # if "[SCAN,SCANNING_SS] conveyor [RUNNING]" in next_line:
                    #     pass
                    # elif "SCANNER IDLE message" in next_line:
                    #     diff = check_time
                    #     total.append(diff)
                    inRun = True
                elif "SCANNER IDLE message" in line:
                    start = time
                    if inRun:
                        diff = check_time
                        total.append(diff)
                    inIdle = True
        print(total, len(total))
        plt.hist(total, bins=30)
        plt.show()

        range0to2 = []
        range2to3 = []
        range3to6 = []
        range6to9 = []
        range9toetc = []
        for num in total:
            if 0 < num and num <= 2:
                range0to2.append(num)
            elif 2 < num and num <= 3:
                range2to3.append(num)
            elif 3 < num and num <= 6:
                range3to6.append(num)
            elif 6 < num and num <= 9:
                range6to9.append(num)
            else:
                range9toetc.append(num)
        print(range0to2)
        print("0-2: ", range0to2, "\n2-3: ", range2to3, "\n3-6: ", range3to6, "\n6-9: ", range6to9, "\n9-etc: ", range9toetc)
        plt.bar(['0-2','2-3','3-6','6-9','9-etc'], height= [len(range0to2),len(range2to3),len(range3to6),len(range6to9),len(range9toetc)])
        plt.show()
                # if inRange and "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line:
                #     # modify time here and ()
                #     self.count += 1
                #     current_time = self.fake_idle_start_time + self.delay
                #     print(current_time, self.fake_idle_start_time)
                #     changed = True
                #     inRange = False
                #     # break

                # if "SCANNER RUNNING message" in line:
                #     if not changed:
                #         self.fake_idle_end_time = time
                #     else:
                #         self.fake_idle_end_time = current_time + (time - last_time)
                #     self.time_diff = self.fake_idle_end_time - self.fake_idle_start_time
                #     self.fake_total_stopped_time += self.time_diff,
                #     inRange = False
                #     inRun = True

                # elif "SCANNER IDLE message and disabling RTR" in line:
                #     if not changed:
                #         self.fake_idle_start_time = time
                #     else:
                #         self.fake_idle_start_time = current_time + (time - last_time)
                #     inRange = False
                #     inIdle = True

                # if (inIdle and inRun) and self.time_diff < 3:  # within the range, add delay to next conveyor running (idle_start_time + 3s)
                #     inRange = True
                #     print("in time diff: ", self.fake_idle_start_time)
                #     # changed = True
                # last_time = self.getDatetime(line.split(',')[0])


if __name__ == '__main__':
    s = Simulation(['C:/Users/wzhong/Documents/temp/logfiles/AnalogicStandaloneType2_20190623.log'])
     # print(line.replace(text_to_search, replacement_text), end='')
