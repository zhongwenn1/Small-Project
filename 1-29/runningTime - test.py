import re
import os
from datetime import datetime
import matplotlib.pyplot as plt
import timeit
import pandas as pd
import seaborn as sns
# from simulation import Simulation


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
        with open('runtime_.txt') as f3, open('simulate delay.txt', 'w') as self.f4:
            for line in f3:               
                # if line.split(',')[0] == '2019-06-17 04:08:47.478256':        # check if date to date time diff is not contain
                #     break
                # if line.split(',')[0] == '2019-06-16 19:28:05.609377':
                #     start = True                
                # if first:
                #     # self.very_start_time = self.getDatetime(line.split(',')[0])
                #     first = False

                self.simulateDelay(line, self.delay)
                # self.runList(line)
                # self.delayRunList(line, self.delay)
                # self.stopList(line)               
                # # self.fakestopList(line)            
                # self.delayStopList(line, self.delay)

        #         self.very_end_time = self.getDatetime(line.split(',')[0])
        # self.total_machine_running = self.very_end_time - self.very_start_time

    # def getRunTimeAfterDelay(self):     
    #     count = 0
    #     seen = False
    #     first = False
    #     with open('simulate delay.txt') as f5:
    #         for line in f5:
    #             if not first:
    #                 self.first_time = float(line.split(',')[0])
    #                 first = True
    #             # if count == 30:
    #             #     print(line)
    #             #     break                
    #             if "IDLE DELAY" in line:    
    #                 self.scanning_end_time = float(line.split(',')[0])
    #                 self.total_running_after_delay += (self.scanning_end_time - self.scanning_start_time),
    #                 seen = False
    #                 count += 1
    #             elif "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line and not seen:
    #                 self.scanning_start_time = float(line.split(',')[0])
    #                 seen = True
                
    #             self.last_time = float(line.split(',')[0])
    #     print(count)

    # def getStopTimeAfterDelay(self):
    #     count = 0
    #     seen, meet = False, False
    #     inSRun, inRun = False, False
    #     with open('simulate delay.txt') as f5:
    #         for line in f5:
    #             # if count == 30:
    #             #     break
    #             # if "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line and seen:
    #             #     self.idle_end_time = float(line.split(',')[0])
    #             #     self.total_stopped_after_delay += (self.idle_end_time - self.idle_start_time),
    #             #     seen = False
    #             # elif "IDLE DELAY" in line:
    #             #     self.idle_start_time = float(line.split(',')[0])
    #             #     seen = True
    #             # count += 1
    #             if "SCANNER IDLE message" in line and meet:
                    
    #                 if inRun and inSRun:
    #                     self.total_stopped_after_delay += (self.srun - self.idle_delay),
    #                     # print("innormal:",self.srun, self.idle_delay)
    #                 elif inRun and not inSRun:
    #                     self.total_stopped_after_delay += (self.run - self.idleS),
    #                     # print("insep:", self.run, self.idleS)
    #                 inSRun = False
    #                 inRun = False
    #                 seen = False
    #                 meet = False
    #                 self.idleS = float(line.split(',')[0])
    #                 count += 1

    #             elif "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line and (meet and not seen):
    #                 # print(line)
    #                 self.srun = float(line.split(',')[0])
    #                 seen = True
    #                 inSRun = True

    #             elif "IDLE DELAY" in line: 
    #                 self.idle_delay = float(line.split(',')[0])
    #                 meet = True

    #             elif "SCANNER RUNNING message" in line:
    #                 self.run = float(line.split(',')[0])
    #                 inRun = True
    #                 meet = True
                
    #     # print(count)

    # def simulateDelayTest(self, line, delay):
    #     # self.f4.write(line)
    #     if "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line:
    #         self.srun = float(line.split(',')[0])
    #         # self.srun = self.getDatetime(line.split(',')[0])
    #         if not self.update:
    #             if not self.inSRun:
    #                 self.diff5 = self.srun - self.run
    #                 self.f4.write((str(self.prev + self.diff5)+','+(',').join(line.split(',')[1:])))                    
    #                 # print("not in", self.srun, self.prevsrun, self.prev)
    #                 self.prev = self.prev + self.diff5
    #             else:
    #                 self.diff4 = self.srun - self.prevsrun
    #                 self.f4.write((str(self.prev + self.diff4)+','+(',').join(line.split(',')[1:])))                    
    #                 # print("in srun", self.srun, self.prevsrun, self.prev, self.diff4)
    #                 self.prev = self.prev + self.diff4

    #         # self.inRun = False
    #         self.update = False
    #         self.inSRun = True
    #         # self.prevsrun = self.getDatetime(line.split(',')[0])
    #         self.prevsrun = float(line.split(',')[0])
    #     elif "Sent SCANNER IDLE" in line:
    #         self.idle = float(line.split(',')[0])
    #         # self.idle = self.getDatetime(line.split(',')[0])
    #         self.diff1 = self.idle - self.srun
    #         self.f4.write((str(self.prev + self.diff1)) +','+ (',').join(line.split(',')[1:]))
    #         self.prev = self.prev + self.diff1
    #         self.inSRun = False
    #     elif "Sent SCANNER RUNNING" in line:
    #         # self.inRun = True
    #         self.inSRun = False
    #         self.run = float(line.split(',')[0])
    #         # self.run = self.getDatetime(line.split(',')[0])
    #         self.diff2 = self.run - self.idle
    #         if self.diff2 <= delay:
    #             self.f4.write((str(self.prev + self.diff2)) + ','+ (',').join(line.split(',')[1:]))
    #             self.prev = self.prev + self.diff2
    #             self.update = True
    #         else:
    #             self.f4.write((str(self.prev + delay)) + ',' + " IDLE DELAY\n")
    #             self.f4.write((str(self.prev + self.diff2)) + ','+ (',').join(line.split(',')[1:]))
    #            self.prev = self.prev + self.diff2

    def simulateDelay(self, line, delay):
        # self.f4.write(line)
        if "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line:
            # self.srun = float(line.split(',')[0])
            self.srun = self.getDatetime(line.split(',')[0])
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
            else:                           # try to add update condition, record first srun and subtract until idle
                if self.is_first_srun:
                    self.first_srun = self.getDatetime(line.split(',')[0])
                    self.is_first_srun = False

            # self.update = False           # try to add update condition, record first srun and subtract until idle
            self.inSRun = True
            self.prevsrun = self.getDatetime(line.split(',')[0])
            # self.prevsrun = float(line.split(',')[0])
        elif "Sent SCANNER IDLE" in line:
            # self.idle = float(line.split(',')[0])
            self.idle = self.getDatetime(line.split(',')[0])
            if self.update:
                self.diff1 = self.idle - self.first_srun
            else:
                self.diff1 = self.idle - self.srun
            self.diff11 = self.idle - self.run
            if self.inSRun:
                self.f4.write((str(self.prev + self.diff1)) +','+ (',').join(line.split(',')[1:]))
                self.prev = self.prev + self.diff1
            elif self.inRun:                # add inRun check, special treat for run & not srun condition
                self.f4.write((str(self.prev + self.diff11)) +','+ (',').join(line.split(',')[1:]))
                self.prev = self.prev + self.diff11
            
            self.inSRun = False
            self.inRun = False              # add inRun check, special treat for run & not srun condition
            self.update = False             # try to add update condition, record first srun and subtract until idle
        elif "Sent SCANNER RUNNING" in line:
            self.inRun = True               # add inRun check, special treat for run & not srun condition
            # self.run = float(line.split(',')[0])
            self.run = self.getDatetime(line.split(',')[0])
            self.diff2 = self.run - self.idle
            if self.diff2 <= delay:
                self.f4.write((str(self.prev + self.diff2)) + ','+ (',').join(line.split(',')[1:]))
                self.prev = self.prev + self.diff2
                self.update = True
                self.is_first_srun = True
            else:
                self.f4.write((str(self.prev + delay)) + ',' + " IDLE DELAY\n")
                self.f4.write((str(self.prev + self.diff2)) + ','+ (',').join(line.split(',')[1:]))
                self.prev = self.prev + self.diff2



    def getDatetime(self, time):
        date_time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
        return datetime.timestamp(date_time)

    def runListDelay(self, line):
        inSRun, inRun, seen = False, False, False
        count = 0
        first = True
        self.delay_start_time = 0
        self.delay_finish_time = 0
        with open('simulate delay.txt') as f5:
            for line in f5:
                if first:
                    self.delay_start_time = float(line.split(',')[0])
                    # self.delay_start_time = self.getDatetime(line.split(',')[0])
                    first = False
                if "SCANNER IDLE message and disabling RTR" in line:
                    idle = float(line.split(',')[0])
                    # idle = self.getDatetime(line.split(',')[0])
                    if inSRun:
                        self.total_running_after_delay += (idle - srun),
                    elif inRun:
                        self.total_running_after_delay += (idle - run),
                    inSRun = False
                    inRun = False
                    seen = False
                    count += 1
                elif "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line and not seen:  # only get the first SRUN if repeate
                    srun = float(line.split(',')[0])
                    # srun = self.getDatetime(line.split(',')[0])
                    inSRun = True
                    seen = True
                elif "SCANNER RUNNING message" in line:
                    run = float(line.split(',')[0])
                    # run = self.getDatetime(line.split(',')[0])
                    inRun = True
                    inSRun = False                                  # try to follow the sequence sun - srun 
                    seen = False                                    # try to follow the sequence sun - srun 
                self.delay_finish_time = float(line.split(',')[0])
                # self.delay_finish_time = self.getDatetime(line.split(',')[0])
                # if count == 551:
                #     print(line)                
        print(count)

    def stopListDelay(self, line):
        inIdle, inRun, inIdle = False, False, False
        # count = 0
        with open('simulate delay.txt') as f:
            for line in f:
                if "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line and (inIdle and inRun):
                    # self.idle_end_time = self.getDatetime(line.split(',')[0])
                    self.idle_end_time = float(line.split(',')[0])
                    self.total_stopped_after_delay += (self.idle_end_time - self.idle_start_time),
                    inIdle = False
                    inRun = False

                elif "SCANNER RUNNING message" in line:
                    # self.prev_time = self.getDatetime(line.split(',')[0]) - self.idle_start_time
                    self.prev_time = float(line.split(',')[0]) - self.idle_start_time
                    inRun = True

                elif "SCANNER IDLE message and disabling RTR" in line:
                    # self.idle_start_time = self.getDatetime(line.split(',')[0])
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
        with open('runtime_.txt') as f5:
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
                # self.org_finish_time = float(line.split(',')[0])
                # if count == 551:
                #     print(line)

        print(count)
        # if "Sent SCANNER IDLE" in line:
        #     self.scanning_end_time = float(line.split(',')[0])
        #     # self.scanning_end_time = self.getDatetime(line.split(',')[0])
        #     self.total_running_time += (self.scanning_end_time - self.scanning_start_time),
        # elif "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line or "Sent SCANNER RUNNING" in line:
        #     self.scanning_start_time = float(line.split(',')[0])
        #     # self.scanning_start_time = self.getDatetime(line.split(',')[0])

    def stopList(self, line):
        inIdle, inRun, inIdle = False, False, False
        with open('runtime_.txt') as f:
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



    # def delayRunList(self, line, delay):
    #     pass

    #     # time = float(line.split(',')[0])
    #     # if "Sent SCANNER RUNNING" in line:
    #     #     self.checktime = time - self.prevtime
    #     #     if self.checktime <= 2:
    #     #         self.total_running_after_delay += (self.runtime + self.checktime),
    #     #         # self.count3 += 1
    #     #     else:
    #     #         self.total_running_after_delay += (self.runtime + delay),
    #     #         # self.count4 += 1
    #     # if "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line or "Sent SCANNER RUNNING" in line:
    #     #     self.starttime = time
    #     # elif "Sent SCANNER IDLE" in line:
    #     #     self.prevtime = time
    #     #     self.runtime = time - self.starttime






    # def delayStopList(self, line, delay):
    #     time = float(line.split(',')[0])
    #     if "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line and (self.inIdled and self.inRund):
    #         if self.check_time <= delay:
    #             # diff = delay
    #             diff = self.check_time      # this should be the fake stop time not delay as the delay will be cancelled if it receiveds the fake stop before delay
    #         else:
    #             # diff = time - self.start
    #             diff = time - self.start + delay    # add the delay to this also. It will be added to all trays with a greater than 2 second delay
    #         self.total_stopped_after_delay.append(diff)
    #         self.inRund = False
    #         self.inIdled = False
    #     elif "SCANNER RUNNING message" in line:
    #         self.check_time = time - self.start
    #         self.inRund = True
    #     elif "SCANNER IDLE message" in line:
    #         self.start = time
    #         if self.inRund:
    #             diff = self.check_time
    #             self.total_stopped_after_delay.append(diff)
    #         self.inIdled = True

    # def fakestopList(self, line):
    #     if "SCANNER RUNNING message" in line:
    #         self.fake_idle_end_time = self.getDatetime(line.split(',')[0])
    #         self.fake_total_stopped_time += (self.fake_idle_end_time - self.fake_idle_start_time),

    #     elif "SCANNER IDLE message and disabling RTR" in line:
    #         self.fake_idle_start_time = self.getDatetime(line.split(',')[0])

    # def showDistribution(self, total_lst, name):
    #     bin_edges = 50
    #     plt.hist(total_lst, bins=bin_edges,
    #               # density=False,
    #               # histtype='bar',
    #               color='b', edgecolor='k', alpha=0.5)
    #     # plt.plot(total_stopped)
    #     plt.xlabel("Timestamp (seconds)")    # xlabel for plot
    #     plt.ylabel("Frequency")             # ylabel for plot
    #     plt.title(name, fontsize=15)    # title 
    #     # plt.savefig('running_time_distribution')
    #     plt.show()

    # def showStopDistribution(self, range0To2, range2To3, range3To6, range6To9, total_stopped_inrange, total):
    #     plt.bar(['0s - 2s','2s - 3s', '3s - 6s','6s - 9s'], [len(range0To2),len(range2To3),len(range3To6),len(range6To9)], label="Stop time")
    #     print("Stopped: \nrange 0s - 2s: ", round(len(range0To2)/len(total) * 100, 2), "%\nnums in 0-2: ", len(range0To2), " out of total: ", len(total))
    #     print("nums in 2-3: ", len(range2To3), " out of total: ", len(total))
    #     print("nums in 3-6: ", len(range3To6), " out of total: ", len(total))
    #     print("nums in 6-9: ", len(range6To9), " out of total: ", len(total))

    #     plt.legend()
    #     plt.xlabel("Timestamp (seconds)")    # xlabel for plot
    #     plt.ylabel("Frequency")             # ylabel for plot
    #     plt.title("Total time stopped", fontsize=15)    # title 
    #     plt.savefig('stop_time_distribution')
    #     plt.show()

    # def showRunDistribution(self, range0To2, range2To3, range3To6, range6To9, total_stopped_inrange, total):
    #     plt.bar(['0s - 2s','2s - 3s', '3s - 6s','6s - 9s'], [len(range0To2),len(range2To3),len(range3To6),len(range6To9)], label="Run time")
    #     print("Running: \nrange 0s - 2s: ", round(len(range0To2)/len(total) * 100, 2), "%\nnums in 0-2: ", len(range0To2), " out of total: ", len(total))
    #     print("nums in 2-3: ", len(range2To3), " out of total: ", len(total))
    #     print("nums in 3-6: ", len(range3To6), " out of total: ", len(total))
    #     print("nums in 6-9: ", len(range6To9), " out of total: ", len(total))
    #     print("nums in 9-20: ", len(self.range9To20), " out of total: ", len(total))
    #     plt.legend()
    #     plt.xlabel("Timestamp (seconds)")    # xlabel for plot
    #     plt.ylabel("Frequency")             # ylabel for plot
    #     plt.title("Total time running", fontsize=15)    # title 
    #     plt.savefig('running_time_distribution')
    #     plt.show()

    # def getCertainRangeList(self, total_time_lst):
    #     self.ready_to_plot_lst = []
    #     self.range0To2 = []
    #     self.range2To3 = []
    #     self.range3To6 = []
    #     self.range6To9 = []
    #     self.range9To20 = []
    #     for item in total_time_lst:
    #       if 0 < item and item <= 2:
    #         # print("in 0-3: ", item)
    #         self.ready_to_plot_lst.append(int(item))
    #         self.range0To2.append(item)
    #       elif 2 < item and item <= 3:
    #         self.ready_to_plot_lst.append(int(item))
    #         self.range2To3.append(item)
    #       elif 3 < item and item <= 6:
    #         # print("in 3-6: ", item)
    #         self.ready_to_plot_lst.append(int(item))
    #         self.range3To6.append(item)
    #       elif 6 < item and item <= 9:
    #         # print("in 6-9: ", item)       
    #         self.range6To9.append(item)
    #         self.ready_to_plot_lst.append(int(item))
    #       elif 9 < item and item <= 20:
    #         self.range9To20.append(item)        

if __name__ == '__main__':

    sc = TimeMeasure(2)
    sc.getDuration()

    # print("run:",sc.total_running_time, len(sc.total_running_time), "sum:", sum(sc.total_running_time), "percentage:",sum(sc.total_running_time) / 57600 * 100)
   
    # print("stop:",sc.total_stopped_time, "sum:", sum(sc.total_stopped_time), "percentage:",sum(sc.total_stopped_time) / 57600 * 100)
    
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
 
    # sc.showDistribution(sc.total_running_after_delay, "total runnning after delay")   
    # sc.showDistribution(sc.total_stopped_after_delay, "total stopped after delay")

    with open('stoplist.txt', 'w') as f:
        for i in range(len(sc.total_stopped_after_delay)):
            # if i == 13: break
            f.write(str(sc.total_stopped_after_delay[i])+'\n')

    for i in range(len(sc.total_running_after_delay)):
        if sc.total_running_time[i] == sc.total_running_after_delay[i]:
            continue
        else:
            print(i, sc.total_running_time[i], sc.total_running_after_delay[i])

    # # small test
    # print("stop:",sc.total_stopped_time, "sum:", sum(sc.total_stopped_time), "percentage:",sum(sc.total_stopped_time) / 57600 * 100)
    # print("after delay:",sc.total_stopped_after_delay, "sum:",sum(sc.total_stopped_after_delay),"percentage:",sum(sc.total_stopped_after_delay)/57600*100)
    # print("run:",sc.total_running_time, "sum:", sum(sc.total_running_time), "percentage:",sum(sc.total_running_time) / 57600 * 100)
    # print("after delay:",sc.total_running_after_delay, "sum:",sum(sc.total_running_after_delay),"percentage:",sum(sc.total_running_after_delay)/57600*100)


                # if not self.inRun:
                #     self.f4.write("not in run" + (str(self.srun)+(',').join(line.split(',')[1:])))
                #     self.prev = self.srun
                # elif self.inSRun:
                #     self.diff4 = self.srun - self.prev
                #     self.f4.write(("in run"+str(self.srun + self.diff4)+(',').join(line.split(',')[1:])))
                #     self.prev = self.srun + self.diff4

                
                # elif self.inRun:
                #     self.diff3 = self.srun - self.prev
                #     print("in run", self.diff3, self.srun, self.prev, self.run)
                #     self.f4.write((str(self.prev + self.diff3)) + (',').join(line.split(',')[1:]))
                #     self.prev = self.prev + self.diff3
            # else:

                # if self.inScan:
                #     self.diff3 = self.srun - self.prevsrun
                #     print("in run", self.diff3, self.srun, self.prevsrun)
                #     self.f4.write((str(self.prev + self.diff3)) + (',').join(line.split(',')[1:]))
                #     self.prev = self.prev + self.diff3