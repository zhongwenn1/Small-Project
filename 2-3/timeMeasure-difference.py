import re
import os
from datetime import datetime
import matplotlib.pyplot as plt
import timeit
import pandas as pd
import seaborn as sns


class TimeMeasure:
    def __init__(self, filename, delay):
        self.total_stopped_time = []
        self.total_running_time = []
        self.fake_total_stopped_time = []
        self.total_stopped_after_delay = []
        self.total_running_after_delay = []
        self.very_start_time = 0
        self.very_end_time = 0
        self.filename = filename
        self.delay = delay
        self.count = 0
        self.count2 = 0
        self.count3 = 0
        self.count4 = 0
        self.total_time_save = 0
        self.total_time_add = 0


    def getDuration(self):
        self.inRun, self.inIdle, self.inSRun, self.seen = False, False, False, False
        self.inRund, self.inIdled = False, False
        first = True
        with open(self.filename) as f3:
            for line in f3:           
                if first:
                    # self.very_start_time = self.getDatetime(line.split(',')[0])
                    first = False

                # self.runList(line)
                # self.delayRunList(line, self.delay)
                # self.stopList(line)               
                # self.fakestopList(line)            
                # self.delayStopList(line, self.delay)
        #         self.very_end_time = self.getDatetime(line.split(',')[0])
        # self.total_machine_running = self.very_end_time - self.very_start_time

    def getDatetime(self, time):
        date_time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
        return datetime.timestamp(date_time)

    def runList(self, line):
        inSRun, inRun, seen = False, False, False
        count = 0
        first = True
        self.org_start_time = 0
        self.org_finish_time = 0
        with open(self.filename) as f5:
            for line in f5:
                if first:
                    self.org_start_time = self.getDatetime(line.split(',')[0])
                    # self.org_start_time = float(line.split(',')[0])
                    first = False
                if "SCANNER IDLE message and disabling RTR" in line:
                    # idle = float(line.split(',')[0])
                    idle = self.getDatetime(line.split(',')[0])
                    if inSRun:
                        self.total_running_time += (idle - srun),
                    elif inRun:
                        self.total_running_time += (idle - run),
                    inSRun = False
                    inRun = False
                    seen = False
                    count += 1
                elif "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line and not seen:
                    # srun = float(line.split(',')[0])
                    srun = self.getDatetime(line.split(',')[0])
                    inSRun = True
                    seen = True
                elif "SCANNER RUNNING message" in line:
                    # run = float(line.split(',')[0])
                    run = self.getDatetime(line.split(',')[0])
                    inRun = True
                    inSRun = False                                  # try to follow the sequence sun - srun 
                    seen = False                                    # try to follow the sequence sun - srun 
                self.org_finish_time = self.getDatetime(line.split(',')[0])


    def stopList(self, line):
        inIdle, inRun, inIdle = False, False, False
        with open(self.filename) as f:
            for line in f:
                if "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line and (inIdle and inRun):
                    self.idle_end_time = self.getDatetime(line.split(',')[0])
                    # self.idle_end_time = float(line.split(',')[0])
                    self.total_stopped_time += (self.idle_end_time - self.idle_start_time),
                    inIdle = False
                    inRun = False

                elif "SCANNER RUNNING message" in line:
                    self.prev_time = self.getDatetime(line.split(',')[0]) - self.idle_start_time
                    # self.prev_time = float(line.split(',')[0]) - self.idle_start_time
                    inRun = True

                elif "SCANNER IDLE message and disabling RTR" in line:
                    self.idle_start_time = self.getDatetime(line.split(',')[0])
                    # self.idle_start_time = float(line.split(',')[0])
                    if inRun:
                        self.total_stopped_time += self.prev_time,
                    inIdle = True        


    def delayRunList(self, line, delay):
        inSRun, inRun, seen = False, False, False
        count = 0
        first = True
        check_time = 10000
        self.dly_start_time = 0
        self.dly_finish_time = 0
        with open(self.filename) as f5:
            for line in f5:
                # if first:
                #     # self.dly_start_time = self.getDatetime(line.split(',')[0])
                #     # self.dly_start_time = float(line.split(',')[0])
                #     first = False
                if "SCANNER IDLE message and disabling RTR" in line:
                    # idle = float(line.split(',')[0])
                    idle = self.getDatetime(line.split(',')[0])

                    if inSRun:
                        self.total_running_after_delay += (idle - srun),
                    elif inRun:
                        self.total_running_after_delay += (idle - run),
                    inSRun = False
                    inRun = False
                    seen = False
                    count += 1
                elif "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line and not seen:
                    # srun = float(line.split(',')[0])
                    srun = self.getDatetime(line.split(',')[0])
                    # if check_time <= delay:
                    #     self.total_time_add += (srun - run)
                    inSRun = True
                    seen = True
                # elif "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line and seen:
                #     curr_srun = self.getDatetime(line.split(',')[0])
                #     self.total_time_add = (curr_srun - srun)
                #     print(self.total_time_add, line)

                elif "SCANNER RUNNING message" in line:
                    # run = float(line.split(',')[0])
                    run = self.getDatetime(line.split(',')[0])
                    # check_time = run - idle
                    inRun = True
                    seen = False                                        # update seen, refresh by run
                # self.dly_finish_time = self.getDatetime(line.split(',')[0])
                # if count == 16:
                #     print(line, self.total_running_after_delay[-1])
        # print(self.total_time_add)


    def delayStopList(self, line, delay):
        inIdle, inRun, inIdle = False, False, False
        count = 0
        with open(self.filename) as f:
            for line in f:
                time = self.getDatetime(line.split(',')[0])
                if "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line and (inIdle and inRun):
                    # print("in")
                    if self.check_time <= delay:                
                        # diff = delay
                        diff = self.check_time      # this should be the fake stop time not delay as the delay will be cancelled if it receiveds the fake stop before delay
                        # self.count += 1
                        # self.total_time_save += (time - self.start - diff)
                    else:
                        # diff = time - self.start
                        diff = time - self.start# + delay    # add the delay to this also. It will be added to all trays with a greater than 2 second delay
                        # self.count2 += 1
                        # self.total_time_add += delay
                    self.total_stopped_after_delay.append(diff)
                    inRun = False
                    inIdle = False
                    count += 1
                elif "SCANNER RUNNING message" in line:
                    self.check_time = time - self.start
                    inRun = True
                    # self.inIdled = False
                elif "SCANNER IDLE message" in line:
                    self.start = time
                    if inRun:
                        diff = self.check_time
                        self.total_stopped_after_delay.append(diff)
                        # self.count2 += 1
                        # self.total_time_add += delay            
                        count += 1
                    inIdle = True

                # if count == 111:
                #     print(line, self.total_stopped_after_delay[-1])

    def getIgnoreSequenceTime(self):
        first = True
        second = False
        inRun = False
        with open(self.filename) as f:
            for line in f:
                time = self.getDatetime(line.split(',')[0])
                if "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line and first:
                    srun = time
                    second = True
                    first = False
                    inRun = False
                elif "SCANNER RUNNING message" in line and second:
                    inRun = True
                elif "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line and (second and inRun):
                    self.total_time_add += (time - srun)
                    first = True
                    second = False
                    inRun = False
                else:
                    first = True
                    second = False
                    inRun = False
        print(self.total_time_add)
    # def fakestopList(self, line):
    #     if "SCANNER RUNNING message" in line:
    #         self.fake_idle_end_time = self.getDatetime(line.split(',')[0])
    #         self.fake_total_stopped_time += (self.fake_idle_end_time - self.fake_idle_start_time),

    #     elif "SCANNER IDLE message and disabling RTR" in line:
    #         self.fake_idle_start_time = self.getDatetime(line.split(',')[0])     

if __name__ == '__main__':

    start_time = timeit.default_timer()

    sc = TimeMeasure('runtime_1.txt',2.0)
    # sc.getDuration()

    sc.runList("")
    sc.delayRunList("",2)
    sc.stopList("")
    sc.delayStopList("",2)
    total_time = sc.org_finish_time - sc.org_start_time
    for i in range(len(sc.total_running_after_delay)):
        if sc.total_running_time[i] != sc.total_running_after_delay[i]:
            sc.total_time_add += abs(sc.total_running_time[i] - sc.total_running_after_delay[i])
    for i in range(len(sc.total_stopped_after_delay)):
        if sc.total_stopped_time[i] != sc.total_stopped_after_delay[i]:
            sc.total_time_save += abs(sc.total_stopped_time[i] - sc.total_stopped_after_delay[i])
    print("before:", sc.total_time_save)
    sc.getIgnoreSequenceTime()
    print("after:", sc.total_time_add)
    dly_total_time = total_time - sc.total_time_save + sc.total_time_add #sc.dly_finish_time - sc.dly_start_time # might want to change to run time + stop time
    print("total:",total_time, "total after delay:",dly_total_time)

    print("run:",len(sc.total_running_time), "sum:", sum(sc.total_running_time), "percentage:",sum(sc.total_running_time) / total_time * 100)  
    print("stop:",len(sc.total_stopped_time), "sum:", sum(sc.total_stopped_time), "percentage:",sum(sc.total_stopped_time) / total_time * 100)

    print("\n---------------Add delay 2 seconds---------------\n")


    print("run after delay:",len(sc.total_running_after_delay), "sum:", sum(sc.total_running_after_delay), "percentage:",sum(sc.total_running_after_delay) / dly_total_time * 100) 
    print("stop after delay:",len(sc.total_stopped_after_delay), "sum:",sum(sc.total_stopped_after_delay),"percentage:",sum(sc.total_stopped_after_delay)/dly_total_time*100)

    count = 0
    with open('runlist.txt') as f:
        for line in f:
            # if float(line) == sc.total_stopped_after_delay[count]:
            #     continue
            # else:
            # print(count, float(line), sc.total_stopped_after_delay[count])
            if float(line) != sc.total_running_after_delay[count]:
                print("not the same", line, sc.total_running_after_delay[count], count)
            count += 1

    # for i in range(len(sc.total_running_after_delay)):
    #     if sc.total_running_time[i] == sc.total_running_after_delay[i]:
    #         continue
    #     else:
    #         print(i, sc.total_running_time[i], sc.total_running_after_delay[i])