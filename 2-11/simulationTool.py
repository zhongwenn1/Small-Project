import re
import os
from datetime import datetime
import matplotlib.pyplot as plt
import timeit
import pandas as pd


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
        self.update, self.inRun, self.inIdle, self.seen = False, False, False, False         # add check condition to prevent two or more "RUN" in a sequnce
        # with open('runtime_big.txt') as f3:
        with open(self.filename) as f3, open('simulate delay.txt', 'w') as self.f4:
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


    def simulateDelay(self, line, delay):
        # self.f4.write(line)
        if "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line:
            # self.srun = float(line.split(',')[0])
            self.srun = self.getDatetime(line.split(',')[0])
            if not self.update:
                if self.inIdle:                                                                 # add check for "RUN" - "SRUN" sequence
                    self.diff6 = self.srun - self.idle                                              # add check for "RUN" - "SRUN" sequence
                    self.f4.write((str(self.prev + self.diff6)+','+(',').join(line.split(',')[1:])))    # add check for "RUN" - "SRUN" sequence
                elif not self.inSRun:
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
            self.inIdle = False                                                 # add check for "RUN" - "SRUN" sequence
            self.seen = False                                                   # add check condition to prevent two or more "RUN" in a sequnce
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
            
            self.inIdle = True                                                 # add check for "RUN" - "SRUN" sequence
            self.inSRun = False
            self.inRun = False              # add inRun check, special treat for run & not srun condition
            self.update = False             # try to add update condition, record first srun and subtract until idle
            self.seen = False                                                   # add check condition to prevent two or more "RUN" in a sequnce
        elif "Sent SCANNER RUNNING" in line and not self.seen:      # add check condition to prevent two or more "RUN" in a sequnce
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
            self.inIdle = False                                                 # add check for "RUN" - "SRUN" sequence
            self.seen = True                                        # add check condition to prevent two or more "RUN" in a sequnce



    def getDatetime(self, time):
        date_time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
        return datetime.timestamp(date_time)

    def runListDelay(self, line):
        inSRun, inRun, seen, inDelay = False, False, False, False
        count = 0
        ccc = 0
        first = True
        check_time = 10000
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
                    if check_time <= self.delay:                    # add check time (extend run time if in delay range)
                        self.total_running_after_delay += (idle - run),
                        ccc += 1
                        # print(line)
                    elif inSRun:
                        self.total_running_after_delay += (idle - srun),
                    elif inRun:
                        self.total_running_after_delay += (idle - run),
                    inSRun = False
                    inRun = False
                    seen = False
                    inDelay = False
                    count += 1
                elif "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line and not seen:  # only get the first SRUN if repeate
                    srun = float(line.split(',')[0])
                    # srun = self.getDatetime(line.split(',')[0])
                    inSRun = True
                    seen = True
                elif "SCANNER RUNNING message" in line:
                    run = float(line.split(',')[0])
                    # run = self.getDatetime(line.split(',')[0])
                    check_time = run - idle                         # add check time (extend run time if in delay range)

                    inRun = True
                    inSRun = False                                  # try to follow the sequence sun - srun 
                    seen = False                                    # try to follow the sequence sun - srun 

                self.delay_finish_time = float(line.split(',')[0])
                # self.delay_finish_time = self.getDatetime(line.split(',')[0])
                # if count == 103:
                #     print(line, self.total_running_after_delay[-1])                
        # # print("run c:", count)
        # print("ccc:",ccc)

    def stopListDelay(self, line):
        inIdle, inRun, inIdle, inDelay = False, False, False, False
        count = 0
        with open('simulate delay.txt') as f:
            for line in f:
                if "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line and (inIdle and inRun):
                    self.idle_end_time = float(line.split(',')[0])
                    if not inDelay:                                                      # add check condition to minimize stop time if is in range
                        self.total_stopped_after_delay += (self.prev_time),         # add check time to minimize stop time if is in range
                    else:                                                           # add check time to minimize stop time if is in range
                        self.total_stopped_after_delay += (self.idle_end_time - self.idle_start_time),
                    # self.idle_end_time = float(line.split(',')[0])
                    # self.total_stopped_after_delay += (self.idle_end_time - self.idle_start_time),
                    inIdle = False
                    inRun = False
                    inDelay = False
                    count += 1

                elif "SCANNER RUNNING message" in line:
                    # self.prev_time = self.getDatetime(line.split(',')[0]) - self.idle_start_time
                    self.prev_time = float(line.split(',')[0]) - self.idle_start_time
                    inRun = True

                elif "SCANNER IDLE message and disabling RTR" in line:
                    # self.idle_start_time = self.getDatetime(line.split(',')[0])
                    self.idle_start_time = float(line.split(',')[0])
                    if inRun:
                        self.total_stopped_after_delay += self.prev_time,
                        count += 1
                    inIdle = True
                    
                elif "IDLE DELAY" in line:
                    inDelay = True
                #     count += 1
        #         if count == 111:
        #             # print(line)
        #             print(line, self.total_stopped_after_delay[-1])
        # print("stop c:", count)

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
                # self.org_finish_time = float(line.split(',')[0])
                # if count == 551:
                #     print(line)


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


    def fakestopList(self):
        with open(self.filename) as f:
            for line in f:
                if "SCANNER RUNNING message" in line:
                    self.fake_idle_end_time = self.getDatetime(line.split(',')[0])
                    self.fake_total_stopped_time += (self.fake_idle_end_time - self.fake_idle_start_time),

                elif "SCANNER IDLE message and disabling RTR" in line:
                    self.fake_idle_start_time = self.getDatetime(line.split(',')[0])


    def getCertainRangeList(self, total_time_lst):
        # self.ready_to_plot_lst = []
        delaylist = []
        range0To2 = []
        range2To3 = []
        range3To6 = []
        range6To9 = []
        range9To20 = []
        for item in total_time_lst:
            if item <= self.delay:
                delaylist.append(item)
            if 0 < item and item <= 2:
                # print("in 0-3: ", item)
                # ready_to_plot_lst.append(int(item))
                range0To2.append(item)
            elif 2 < item and item <= 3:
                # ready_to_plot_lst.append(int(item))
                range2To3.append(item)
            elif 3 < item and item <= 6:
                # print("in 3-6: ", item)
                # ready_to_plot_lst.append(int(item))
                range3To6.append(item)
            elif 6 < item and item <= 9:
                # print("in 6-9: ", item)       
                range6To9.append(item)
                # ready_to_plot_lst.append(int(item))
            elif 9 < item and item <= 20:
                range9To20.append(item)  
        # print("\nDelay list / total: {0:.2f}%".format(len(delaylist)/len(total_time_lst)*100))
        # plt.bar(['0s - 2s','2s - 3s', '3s - 6s','6s - 9s'], [len(range0To2),len(range2To3),len(range3To6),len(range6To9)], label="Run time")
        # print("\nDelay range 0s - 2s: ", round(len(range0To2)/len(total_time_lst) * 100, 2), "%\nnums in 0-2: ", len(range0To2), " out of total: ", len(total_time_lst))
        # print("nums in 2-3: ", len(range2To3), " out of total: ", len(total_time_lst))
        # print("nums in 3-6: ", len(range3To6), " out of total: ", len(total_time_lst))
        # print("nums in 6-9: ", len(range6To9), " out of total: ", len(total_time_lst))
        # print("nums in 9-20: ", len(range9To20), " out of total: ", len(total_time_lst))
        # plt.legend()
        # plt.xlabel("Timestamp (seconds)")    # xlabel for plot
        # plt.ylabel("Frequency")             # ylabel for plot
        # plt.title("Total time running", fontsize=15)    # title 
        # plt.savefig('running_time_distribution')
        # plt.show()          
        return delaylist 

# if __name__ == '__main__':

#     sc = TimeMeasure('C:/Users/wzhong/Documents/temp/2-4/files/runtime_.txt', 2)
#     sc.getDuration()
    
#     # test for run time -- completed (1/30 4:50) notes: PERFECT!!!!!
#     sc.runList("")
#     sc.stopList("")
#     total_time = sc.org_finish_time - sc.org_start_time

#     print("run:",len(sc.total_running_time), "sum:", sum(sc.total_running_time),"percentage:",sum(sc.total_running_time)/total_time * 100)
#     print("stop:",len(sc.total_stopped_time), "sum:", sum(sc.total_stopped_time),"percentage:",sum(sc.total_stopped_time)/total_time * 100)
#     print("total:",total_time, sum(sc.total_running_time)/total_time * 100 + sum(sc.total_stopped_time)/total_time * 100)

#     print("\n---------------Add delay 2 seconds---------------\n")
#     sc.runListDelay("")
#     sc.stopListDelay("")
#     total_time_after_delay = sc.delay_finish_time - sc.delay_start_time
#     print("run after delay:", len(sc.total_running_after_delay), "sum:", sum(sc.total_running_after_delay), "percentage:",sum(sc.total_running_after_delay) / total_time_after_delay * 100)
#     print("stop after delay:",len(sc.total_stopped_after_delay), "sum:", sum(sc.total_stopped_after_delay), "percentage:",sum(sc.total_stopped_after_delay) / total_time_after_delay * 100)
#     print("total:",total_time_after_delay, sum(sc.total_running_after_delay) / total_time_after_delay * 100 + sum(sc.total_stopped_after_delay) / total_time_after_delay * 100)


#     sc.fakestopList()
#     delaylist = sc.getCertainRangeList(sc.fake_total_stopped_time)
#     print("\nSummary:")
#     print("Before delay XRAY_MIN / total: 100% ----> After delay XRAY_MIN / total: {0:.2f}%".format((len(sc.fake_total_stopped_time)-len(delaylist))/len(sc.fake_total_stopped_time)*100))
#     print("Before delay total time: 100% ----> After delay total time: {0:.2f}%".format(total_time_after_delay/total_time*100))
    

#     with open('runlist.txt', 'w') as f:
#         for i in range(len(sc.total_running_after_delay)):
#             # if i == 13: break
#             f.write(str(sc.total_running_after_delay[i])+'\n')



    # print(sc.total_running_after_delay[-1])
    # print(sc.total_stopped_after_delay[-1])

    # for i in range(len(sc.total_running_after_delay)):
    #     if sc.total_running_time[i] == sc.total_running_after_delay[i]:
    #         continue
    #     else:
    #         print(i, sc.total_running_time[i], sc.total_running_after_delay[i])
