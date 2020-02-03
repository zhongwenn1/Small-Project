import re
import os
from datetime import datetime
import matplotlib.pyplot as plt
import timeit
import pandas as pd
import seaborn as sns


class TimeMeasure:
    def __init__(self, delay):
        self.total_stopped_time = []
        self.total_running_time = []
        self.fake_total_stopped_time = []
        self.total_stopped_after_delay = []
        self.total_running_after_delay = []
        self.very_start_time = 0
        self.very_end_time = 0
        self.delay = delay
        self.count = 0
        self.acc = 0
        self.prevsrun = 0
        self.run = 0
        self.prev = 0
        self.idle_delay = 0
        self.first_time = 0
        self.last_time = 0
        # self.scanning_start_time = 0
        # self.starttime = 0

    def getDuration(self):
        self.inRun, self.inIdle = False, False
        self.inRund, self.inIdled = False, False
        self.inSRun, self.inScan = False, False
        self.is_first_srun = False
        first = True
        start = False
        self.update, self.inRun, self.inIdle = False, False, False
        # with open('runtime_big.txt') as f3:
        with open('test2.txt') as f3, open('simulate delay.txt', 'w') as self.f4:
            for line in f3:               
                self.simulateDelayTest(line, self.delay)


    def simulateDelayTest(self, line, delay):
        # self.f4.write(line)
        if "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line:
            self.srun = float(line.split(',')[0])
            # self.srun = self.getDatetime(line.split(',')[0])
            if not self.update:
                if not self.inSRun:
                    self.diff5 = self.srun - self.run
                    self.f4.write((str(self.prev + self.diff5)+','+(',').join(line.split(',')[1:])))                    
                    # print("not in", self.srun, self.prevsrun, self.prev)
                    self.prev = self.prev + self.diff5
                else:
                    self.diff4 = self.srun - self.prevsrun
                    self.f4.write((str(self.prev + self.diff4)+','+(',').join(line.split(',')[1:])))                    
                    # print("in srun", self.srun, self.prevsrun, self.prev, self.diff4)
                    self.prev = self.prev + self.diff4

            # self.inRun = False
            self.update = False
            self.inSRun = True
            # self.prevsrun = self.getDatetime(line.split(',')[0])
            self.prevsrun = float(line.split(',')[0])
        elif "Sent SCANNER IDLE" in line:
            self.idle = float(line.split(',')[0])
            # self.idle = self.getDatetime(line.split(',')[0])
            self.diff1 = self.idle - self.srun
            self.f4.write((str(self.prev + self.diff1)) +','+ (',').join(line.split(',')[1:]))
            self.prev = self.prev + self.diff1
            self.inSRun = False
        elif "Sent SCANNER RUNNING" in line:
            # self.inRun = True
            self.inSRun = False
            self.run = float(line.split(',')[0])
            # self.run = self.getDatetime(line.split(',')[0])
            self.diff2 = self.run - self.idle
            if self.diff2 <= delay:
                self.f4.write((str(self.prev + self.diff2)) + ','+ (',').join(line.split(',')[1:]))
                self.prev = self.prev + self.diff2
                self.update = True
            else:
                self.f4.write((str(self.prev + delay)) + ',' + " IDLE DELAY\n")
                self.f4.write((str(self.prev + self.diff2)) + ','+ (',').join(line.split(',')[1:]))
                self.prev = self.prev + self.diff2


    def runListDelay(self, line):
        inSRun, inRun, seen = False, False, False
        count = 0
        first = True
        check_time = 10000
        self.delay_start_time = 0
        self.delay_finish_time = 0
        with open('simulate delay.txt') as f5:
            for line in f5:
                if first:
                    self.delay_start_time = float(line.split(',')[0])
                    first = False
                if "SCANNER IDLE message and disabling RTR" in line:
                    idle = float(line.split(',')[0])
                    if check_time <= self.delay:                    # add check time (extend run time if in delay range)
                        self.total_running_after_delay += (idle - run),
                    elif inSRun:
                        self.total_running_after_delay += (idle - srun),
                    elif inRun:
                        self.total_running_after_delay += (idle - run),
                    inSRun = False
                    inRun = False
                    seen = False
                    count += 1
                elif "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line and not seen:  # only get the first SRUN if repeate
                    srun = float(line.split(',')[0])
                    inSRun = True
                    seen = True
                elif "SCANNER RUNNING message" in line:
                    run = float(line.split(',')[0])
                    check_time = run - idle                         # add check time (extend run time if in delay range)
                    inRun = True
                    inSRun = False                                  # try to follow the sequence sun - srun 
                    seen = False                                    # try to follow the sequence sun - srun 
                self.delay_finish_time = float(line.split(',')[0])
                # if count == 551:
                #     print(line)                
        # print(count)

    def stopListDelay(self, line):
        inIdle, inRun, inIdle = False, False, False
        # count = 0
        with open('simulate delay.txt') as f:
            for line in f:
                if "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line and (inIdle and inRun):
                    self.idle_end_time = float(line.split(',')[0])
                    if self.prev_time <= self.delay:                                # add check time to minimize stop time if is in range
                        self.total_stopped_after_delay += (self.prev_time),         # add check time to minimize stop time if is in range
                    else:                                                           # add check time to minimize stop time if is in range
                        self.total_stopped_after_delay += (self.idle_end_time - self.idle_start_time),
                    inIdle = False
                    inRun = False

                elif "SCANNER RUNNING message" in line:
                    self.prev_time = float(line.split(',')[0]) - self.idle_start_time
                    inRun = True

                elif "SCANNER IDLE message and disabling RTR" in line:
                    self.idle_start_time = float(line.split(',')[0])
                    if inRun:
                        self.total_stopped_after_delay += self.prev_time,
                    inIdle = True
                #     count += 1
                # if count == 13:
                #     print(line)
                #     print(self.total_stopped_after_delay[-1])
                

    def runList(self, line):
        inSRun, inRun, seen = False, False, False
        count = 0
        first = True
        self.org_start_time = 0
        self.org_finish_time = 0
        with open('test2.txt') as f5:
            for line in f5:
                if first:
                    self.org_start_time = float(line.split(',')[0])
                    first = False
                if "SCANNER IDLE message and disabling RTR" in line:
                    idle = float(line.split(',')[0])
                    if inSRun:
                        self.total_running_time += (idle - srun),
                    elif inRun:
                        self.total_running_time += (idle - run),
                    inSRun = False
                    inRun = False
                    seen = False
                    count += 1
                elif "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line and not seen:
                    srun = float(line.split(',')[0])
                    inSRun = True
                    seen = True
                elif "SCANNER RUNNING message" in line:
                    run = float(line.split(',')[0])
                    inRun = True
                    inSRun = False                                  # try to follow the sequence sun - srun 
                    seen = False                                    # try to follow the sequence sun - srun 
                self.org_finish_time = float(line.split(',')[0])
                # if count == 551:
                #     print(line)


    def stopList(self, line):
        inIdle, inRun, inIdle = False, False, False
        with open('test2.txt') as f:
            for line in f:
                if "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line and (inIdle and inRun):
                    self.idle_end_time = float(line.split(',')[0])
                    self.total_stopped_time += (self.idle_end_time - self.idle_start_time),
                    inIdle = False
                    inRun = False

                elif "SCANNER RUNNING message" in line:
                    self.prev_time = float(line.split(',')[0]) - self.idle_start_time
                    inRun = True

                elif "SCANNER IDLE message and disabling RTR" in line:
                    self.idle_start_time = float(line.split(',')[0])
                    if inRun:
                        self.total_stopped_time += self.prev_time,
                    inIdle = True
       

if __name__ == '__main__':

    sc = TimeMeasure(2)
    sc.getDuration()
    
    # test for run time -- completed (1/30 4:50) notes: PERFECT!!!!!
    sc.runList("")
    sc.stopList("")
    total_time = sc.org_finish_time - sc.org_start_time
    print("run:",len(sc.total_running_time), "sum:", sum(sc.total_running_time),"percentage:",sum(sc.total_running_time)/total_time * 100)
    print("stop:",len(sc.total_stopped_time), "sum:", sum(sc.total_stopped_time),"percentage:",sum(sc.total_stopped_time)/total_time * 100)
    print("total:",total_time, sum(sc.total_running_time)/total_time * 100 + sum(sc.total_stopped_time)/total_time * 100)

    print("\n---------------Add delay 2 seconds---------------\n")
    sc.runListDelay("")
    sc.stopListDelay("")
    total_time_after_delay = sc.delay_finish_time - sc.delay_start_time  
    print("run after delay:", len(sc.total_running_after_delay), "sum:", sum(sc.total_running_after_delay), "percentage:",sum(sc.total_running_after_delay) / total_time_after_delay * 100)
    print("stop after delay:",len(sc.total_stopped_after_delay), "sum:", sum(sc.total_stopped_after_delay), "percentage:",sum(sc.total_stopped_after_delay) / total_time_after_delay * 100)
    print("total:",total_time_after_delay, sum(sc.total_running_after_delay) / total_time_after_delay * 100 + sum(sc.total_stopped_after_delay) / total_time_after_delay * 100)


    print("run:",sc.total_running_after_delay)
    print("stop:", sc.total_stopped_after_delay)

    with open('stoplist.txt', 'w') as f:
        for i in range(len(sc.total_stopped_after_delay)):
            # if i == 13: break
            f.write(str(sc.total_stopped_after_delay[i])+'\n')

    for i in range(len(sc.total_running_after_delay)):
        if sc.total_running_time[i] == sc.total_running_after_delay[i]:
            continue
        else:
            print(i, sc.total_running_time[i], sc.total_running_after_delay[i])

