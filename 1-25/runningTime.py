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
        self.count2 = 0
        self.count3 = 0
        self.count4 = 0
        self.total_time_save = 0
        self.total_time_add = 0


    def getDuration(self):
        self.inRun, self.inIdle, self.inSRun, self.seen = False, False, False, False
        self.inRund, self.inIdled = False, False
        first = True
        with open('runtime_.txt') as f3:
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
        # if "Sent SCANNER IDLE" in line:
        #     self.scanning_end_time = self.getDatetime(line.split(',')[0])
        #     self.total_running_time += (self.scanning_end_time - self.scanning_start_time),
        # elif "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line or "Sent SCANNER RUNNING" in line:
        #     self.scanning_start_time = self.getDatetime(line.split(',')[0])

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
        # if "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line and (self.inIdle and self.inRun):
        #     self.idle_end_time = self.getDatetime(line.split(',')[0])
        #     self.total_stopped_time += (self.idle_end_time - self.idle_start_time),
        #     self.inIdle = False
        #     self.inRun = False

        # elif "SCANNER RUNNING message" in line:
        #     self.prev_time = self.getDatetime(line.split(',')[0]) - self.idle_start_time
        #     self.inRun = True

        # elif "SCANNER IDLE message and disabling RTR" in line:
        #     self.idle_start_time = self.getDatetime(line.split(',')[0])
        #     if self.inRun:
        #         self.total_stopped_time += self.prev_time,
        #     self.inIdle = True

    def delayRunList(self, line, delay):
        inSRun, inRun, seen = False, False, False
        count = 0
        first = True
        self.dly_start_time = 0
        self.dly_finish_time = 0
        with open('runtime_.txt') as f5:
            for line in f5:
                if first:
                    # self.dly_start_time = self.getDatetime(line.split(',')[0])
                    # self.dly_start_time = float(line.split(',')[0])
                    first = False
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
                    inSRun = True
                    seen = True
                elif "SCANNER RUNNING message" in line:
                    # run = float(line.split(',')[0])
                    run = self.getDatetime(line.split(',')[0])
                    inRun = True
                # self.dly_finish_time = self.getDatetime(line.split(',')[0])
        # time = self.getDatetime(line.split(',')[0])
        # if "Sent SCANNER RUNNING" in line:
        #     self.checktime = time - self.prevtime
        #     if self.checktime <= 2:
        #         self.total_running_after_delay += (self.runtime + self.checktime),
        #         self.count3 += 1
        #     else:
        #         self.total_running_after_delay += (self.runtime + delay),
        #         self.count4 += 1
        # if "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line or "Sent SCANNER RUNNING" in line:
        #     self.starttime = time
        # elif "Sent SCANNER IDLE" in line:
        #     self.prevtime = time
        #     self.runtime = time - self.starttime


    # def fakestopList(self, line):
    #     if "SCANNER RUNNING message" in line:
    #         self.fake_idle_end_time = self.getDatetime(line.split(',')[0])
    #         self.fake_total_stopped_time += (self.fake_idle_end_time - self.fake_idle_start_time),

    #     elif "SCANNER IDLE message and disabling RTR" in line:
    #         self.fake_idle_start_time = self.getDatetime(line.split(',')[0])


    def delayStopList(self, line, delay):
        inIdle, inRun, inIdle = False, False, False
        with open('runtime_.txt') as f:
            for line in f:
                time = self.getDatetime(line.split(',')[0])
                if "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line and (inIdle and inRun):
                    # print("in")
                    if self.check_time <= delay:                
                        # diff = delay
                        diff = self.check_time      # this should be the fake stop time not delay as the delay will be cancelled if it receiveds the fake stop before delay
                        # self.count += 1
                        self.total_time_save += (time - self.start - diff)
                    else:
                        # diff = time - self.start
                        diff = time - self.start# + delay    # add the delay to this also. It will be added to all trays with a greater than 2 second delay
                        # self.count2 += 1
                        self.total_time_add += delay
                    self.total_stopped_after_delay.append(diff)
                    inRun = False
                    inIdle = False
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
                        self.total_time_add += delay            
                    inIdle = True
                # if "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line and (inIdle and inRun):
                #     self.idle_end_time = self.getDatetime(line.split(',')[0])
                #     # self.idle_end_time = float(line.split(',')[0])
                #     if self.prev_time <= delay:
                #         self.total_stopped_after_delay += (self.prev_time),
                #     else:
                #         self.total_stopped_after_delay += (self.idle_end_time - self.idle_start_time),
                #     inIdle = False
                #     inRun = False

                # elif "SCANNER RUNNING message" in line:
                #     self.prev_time = self.getDatetime(line.split(',')[0]) - self.idle_start_time
                #     # self.prev_time = float(line.split(',')[0]) - self.idle_start_time
                #     inRun = True

                # elif "SCANNER IDLE message and disabling RTR" in line:
                #     self.idle_start_time = self.getDatetime(line.split(',')[0])
                #     # self.idle_start_time = float(line.split(',')[0])
                #     if inRun:
                #         self.total_stopped_after_delay += self.prev_time,
                #     inIdle = True


        # time = self.getDatetime(line.split(',')[0])
        # if "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line and (self.inIdled and self.inRund):
        #     # print("in")
        #     if self.check_time <= delay:                
        #         # diff = delay
        #         diff = self.check_time      # this should be the fake stop time not delay as the delay will be cancelled if it receiveds the fake stop before delay
        #         self.count += 1
        #         self.total_time_save += (time - self.start - diff)
        #     else:
        #         # diff = time - self.start
        #         diff = time - self.start# + delay    # add the delay to this also. It will be added to all trays with a greater than 2 second delay
        #         self.count2 += 1
        #         self.total_time_add += delay
        #     self.total_stopped_after_delay.append(diff)
        #     self.inRund = False
        #     self.inIdled = False
        # elif "SCANNER RUNNING message" in line:
        #     self.check_time = time - self.start
        #     self.inRund = True
        #     # self.inIdled = False
        # elif "SCANNER IDLE message" in line:
        #     self.start = time
        #     if self.inRund:
        #         diff = self.check_time
        #         self.total_stopped_after_delay.append(diff)
        #         self.count2 += 1
        #         self.total_time_add += delay            
        #     self.inIdled = True

    # def showDistribution(self, total_lst, name, num):
    #     bin_edges = 50
    #     plt.subplot(2, 1, num)
    #     plt.hist(total_lst, bins=bin_edges,
    #               density=False,
    #               histtype='bar',
    #               color='b', edgecolor='k', alpha=0.5)
    #     # plt.plot(total_stopped)
    #     # plt.xlabel("Timestamp (seconds)")    # xlabel for plot
    #     plt.ylabel("Frequency")             # ylabel for plot
    #     plt.title(name, fontsize=15)    # title 
    #     # plt.savefig('running_time_distribution')
    #     # plt.show()

    # def showStopDistribution(self, range0To2, range2To3, range3To6, range6To9, total_stopped_inrange, total, num):
    #     plt.subplot(2, 1, num)
    #     plt.bar(['0s - 2s','2s - 3s', '3s - 6s','6s - 9s'], [len(range0To2),len(range2To3),len(range3To6),len(range6To9)], label="Stop time")
    #     print("\nrange 0s - 2s: ", round(len(range0To2)/len(total) * 100, 2), "%\nnums in 0-2: ", len(range0To2), " out of total: ", len(total))
    #     print("nums in 2-3: ", len(range2To3), " out of total: ", len(total))
    #     print("nums in 3-6: ", len(range3To6), " out of total: ", len(total))
    #     print("nums in 6-9: ", len(range6To9), " out of total: ", len(total))

    #     plt.legend()
    #     plt.xlabel("Timestamp (seconds)")    # xlabel for plot
    #     plt.ylabel("Frequency")             # ylabel for plot
    #     # plt.title("Total time stopped", fontsize=15)    # title 
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
    #         self.ready_to_plot_lst.append(int(item))
    #         self.range0To2.append(item)
    #       elif 2 < item and item <= 3:
    #         self.ready_to_plot_lst.append(int(item))
    #         self.range2To3.append(item)
    #       elif 3 < item and item <= 6:
    #         self.ready_to_plot_lst.append(int(item))
    #         self.range3To6.append(item)
    #       elif 6 < item and item <= 9:
    #         self.range6To9.append(item)
    #         self.ready_to_plot_lst.append(int(item))
    #       elif 9 < item and item <= 20:
    #         self.range9To20.append(item)        

if __name__ == '__main__':

    start_time = timeit.default_timer()

    sc = TimeMeasure(2.0)
    # sc.getDuration()

    sc.runList("")
    sc.delayRunList("",2)
    sc.stopList("")
    sc.delayStopList("",2)
    total_time = sc.org_finish_time - sc.org_start_time
    dly_total_time = total_time - sc.total_time_save #sc.dly_finish_time - sc.dly_start_time # might want to change to run time + stop time
    # sc.showDistribution(sc.fake_total_stopped_time, 'Fake total time stopped')
    # sc.getCertainRangeList(sc.fake_total_stopped_time, 1)
    # sc.showStopDistribution(sc.range0To2, sc.range2To3, sc.range3To6, sc.range6To9, sc.ready_to_plot_lst, sc.fake_total_stopped_time, 2)  
    # sc.showDistribution(sc.total_running_time, 'Total time running', 1)
    # sc.getCertainRangeList(sc.total_running_time)
    # sc.showStopDistribution(sc.range0To2, sc.range2To3, sc.range3To6, sc.range6To9, sc.ready_to_plot_lst, sc.total_running_time, 2)  
    print("run:",len(sc.total_running_time), "sum:", sum(sc.total_running_time), "percentage:",sum(sc.total_running_time) / total_time * 100) 

    # sc.showDistribution(sc.total_stopped_time, 'Total time stopped', 1)
    # sc.getCertainRangeList(sc.total_stopped_time)
    # sc.showStopDistribution(sc.range0To2, sc.range2To3, sc.range3To6, sc.range6To9, sc.ready_to_plot_lst, sc.total_stopped_time, 2)  
    print("stop:",len(sc.total_stopped_time), "sum:", sum(sc.total_stopped_time), "percentage:",sum(sc.total_stopped_time) / total_time * 100)

    print("\n---------------Add delay 2 seconds---------------\n")

    # sc.showDistribution(sc.total_running_after_delay, 'Total time running after delay', 1)
    # sc.getCertainRangeList(sc.total_running_after_delay)
    # sc.showStopDistribution(sc.range0To2, sc.range2To3, sc.range3To6, sc.range6To9, sc.ready_to_plot_lst, sc.total_running_after_delay, 2) 
    # print(sc.total_running_after_delay) 
    print("run after delay:",len(sc.total_running_after_delay), "sum:", sum(sc.total_running_after_delay), "percentage:",sum(sc.total_running_after_delay) / dly_total_time * 100) 
    # print("total time save on", sc.count3, "items")
    # print("total time added on", sc.count4, "items")

    # sc.showDistribution(sc.total_stopped_after_delay, 'Total time stopped after delay', 1)
    # sc.getCertainRangeList(sc.total_stopped_after_delay)
    # sc.showStopDistribution(sc.range0To2, sc.range2To3, sc.range3To6, sc.range6To9, sc.ready_to_plot_lst, sc.total_stopped_after_delay, 2)
    # print(sc.total_stopped_after_delay)
    print("stop after delay:",len(sc.total_stopped_after_delay), "sum:",sum(sc.total_stopped_after_delay),"percentage:",sum(sc.total_stopped_after_delay)/dly_total_time*100)
    # print("total time save:",sc.total_time_save,"on",sc.count,"items")
    # print("total time add:",sc.total_time_add,"on",sc.count2,"items")

    # print(sc.total_time_add)
    # print(sc.total_time_save)
    # print(total_time - sc.total_time_save)
    count = 0
    with open('stoplist.txt') as f:
        for line in f:
            # if float(line) == sc.total_stopped_after_delay[count]:
            #     continue
            # else:
            # print(count, float(line), sc.total_stopped_after_delay[count])
            if float(line) != sc.total_stopped_after_delay[count]:
                print("not the same")
            count += 1

    # # density with shade
    # sns.distplot(sc.total_stopped_time, hist = False, kde = True, kde_kws = {'shade': True, 'linewidth': 3}, label = 'before delay')    
    # sns.distplot(sc.total_stopped_after_delay, hist = False, kde = True, kde_kws = {'shade': True, 'linewidth': 3}, label = 'after delay')

    # plt.legend(prop={'size': 12})
    # plt.title('stop time distribution')
    # plt.xlabel('timestamp (seconds)')
    # plt.ylabel('Density')
    # plt.show()   
