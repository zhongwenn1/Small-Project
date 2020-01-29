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
        # self.scanning_start_time = 0
        # self.starttime = 0

    def getDuration(self):
        self.inRun, self.inIdle = False, False
        self.inRund, self.inIdled = False, False
        first = True
        start = False
        self.update, self.inRun, self.inIdle = False, False, False
        # with open('runtime_big.txt') as f3:
        with open('test.txt') as f3, open('simulate delay.txt', 'w') as self.f4:
            for line in f3:               
                # if line.split(',')[0] == '2019-06-17 04:08:47.478256':        # check if date to date time diff is not contain
                #     break
                # if line.split(',')[0] == '2019-06-16 19:28:05.609377':
                #     start = True                
                if first:
                    # self.very_start_time = self.getDatetime(line.split(',')[0])
                    first = False

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
            self.srun = float(line.split(',')[0])
            if self.update:
                pass
            else:
                # self.acc = self.srun
                self.f4.write((str(self.srun) + "," + (',').join(line.split(',')[1:])))
            # self.inRun = False

        elif "Sent SCANNER IDLE" in line:
            self.idle = float(line.split(',')[0])
            self.diff1 = self.idle - self.srun
            if self.update:
                self.acc = self.run + self.diff1
                self.f4.write((str(self.run + self.diff1) + "," + (',').join(line.split(',')[1:])))
            else:
                # self.acc += self.idle
                self.f4.write((str(self.idle) + "," + (',').join(line.split(',')[1:])))
            self.inIdle = True
            self.inRun = False
            self.update = False
        elif "Sent SCANNER RUNNING" in line:
            self.run = float(line.split(',')[0])
            self.diff2 = self.run - self.idle
            if self.diff2 <= delay and self.inIdle:
                self.acc = self.diff2
                self.f4.write((str(self.diff2) + "," + (',').join(line.split(',')[1:])))
                self.update = True
            else:
                print(self.acc)
                self.acc += delay
                self.f4.write((str(self.acc) + "," + " IDLE delay\n"))
                print(self.run - self.idle, " run", self.run)
                self.acc += (self.run - self.idle)
                self.f4.write((str(self.acc) + "," + (',').join(line.split(',')[1:])))
            self.inRun = True
            self.inIdle = False



    def getDatetime(self, time):
        date_time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
        return datetime.timestamp(date_time)

    def runList(self, line):
        if "Sent SCANNER IDLE" in line:
            self.scanning_end_time = float(line.split(',')[0])
            self.total_running_time += (self.scanning_end_time - self.scanning_start_time),
        elif "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line or "Sent SCANNER RUNNING" in line:
            self.scanning_start_time = float(line.split(',')[0])

    def delayRunList(self, line, delay):
        time = float(line.split(',')[0])
        if "Sent SCANNER RUNNING" in line:
            self.checktime = time - self.prevtime
            if self.checktime <= 2:
                self.total_running_after_delay += (self.runtime + self.checktime),
                # self.count3 += 1
            else:
                self.total_running_after_delay += (self.runtime + delay),
                # self.count4 += 1
        if "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line or "Sent SCANNER RUNNING" in line:
            self.starttime = time
        elif "Sent SCANNER IDLE" in line:
            self.prevtime = time
            self.runtime = time - self.starttime

    def fakestopList(self, line):
        if "SCANNER RUNNING message" in line:
            self.fake_idle_end_time = self.getDatetime(line.split(',')[0])
            self.fake_total_stopped_time += (self.fake_idle_end_time - self.fake_idle_start_time),

        elif "SCANNER IDLE message and disabling RTR" in line:
            self.fake_idle_start_time = self.getDatetime(line.split(',')[0])

    def stopList(self, line):
        
        if "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line:
            if self.inIdle and self.inRun: #SCANNER RUNNING message" in line:
                self.idle_end_time = float(line.split(',')[0])
                self.total_stopped_time += (self.idle_end_time - self.idle_start_time),
                self.inIdle = False
                self.inRun = False

        elif "SCANNER IDLE message and disabling RTR" in line: # or "[IDLE,IDLE_SS]" in line) and self.idle_start_time != 0:
            self.idle_start_time = float(line.split(',')[0])
            self.inIdle = True
        elif "SCANNER RUNNING message" in line:
            self.inRun = True


    def delayStopList(self, line, delay):
        time = float(line.split(',')[0])
        if "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line and (self.inIdled and self.inRund):
            if self.check_time <= delay:
                # diff = delay
                diff = self.check_time      # this should be the fake stop time not delay as the delay will be cancelled if it receiveds the fake stop before delay
            else:
                # diff = time - self.start
                diff = time - self.start + delay    # add the delay to this also. It will be added to all trays with a greater than 2 second delay
            self.total_stopped_after_delay.append(diff)
            self.inRund = False
            self.inIdled = False
        elif "SCANNER RUNNING message" in line:
            self.check_time = time - self.start
            self.inRund = True
        elif "SCANNER IDLE message" in line:
            self.start = time
            if self.inRund:
                diff = self.check_time
                self.total_stopped_after_delay.append(diff)
            self.inIdled = True


    def showDistribution(self, total_lst, name):
        bin_edges = 50
        plt.hist(total_lst, bins=bin_edges,
                  # density=False,
                  # histtype='bar',
                  color='b', edgecolor='k', alpha=0.5)
        # plt.plot(total_stopped)
        plt.xlabel("Timestamp (seconds)")    # xlabel for plot
        plt.ylabel("Frequency")             # ylabel for plot
        plt.title(name, fontsize=15)    # title 
        # plt.savefig('running_time_distribution')
        plt.show()

    def showStopDistribution(self, range0To2, range2To3, range3To6, range6To9, total_stopped_inrange, total):
        plt.bar(['0s - 2s','2s - 3s', '3s - 6s','6s - 9s'], [len(range0To2),len(range2To3),len(range3To6),len(range6To9)], label="Stop time")
        print("Stopped: \nrange 0s - 2s: ", round(len(range0To2)/len(total) * 100, 2), "%\nnums in 0-2: ", len(range0To2), " out of total: ", len(total))
        print("nums in 2-3: ", len(range2To3), " out of total: ", len(total))
        print("nums in 3-6: ", len(range3To6), " out of total: ", len(total))
        print("nums in 6-9: ", len(range6To9), " out of total: ", len(total))

        plt.legend()
        plt.xlabel("Timestamp (seconds)")    # xlabel for plot
        plt.ylabel("Frequency")             # ylabel for plot
        plt.title("Total time stopped", fontsize=15)    # title 
        plt.savefig('stop_time_distribution')
        plt.show()

    def showRunDistribution(self, range0To2, range2To3, range3To6, range6To9, total_stopped_inrange, total):
        plt.bar(['0s - 2s','2s - 3s', '3s - 6s','6s - 9s'], [len(range0To2),len(range2To3),len(range3To6),len(range6To9)], label="Run time")
        print("Running: \nrange 0s - 2s: ", round(len(range0To2)/len(total) * 100, 2), "%\nnums in 0-2: ", len(range0To2), " out of total: ", len(total))
        print("nums in 2-3: ", len(range2To3), " out of total: ", len(total))
        print("nums in 3-6: ", len(range3To6), " out of total: ", len(total))
        print("nums in 6-9: ", len(range6To9), " out of total: ", len(total))
        print("nums in 9-20: ", len(self.range9To20), " out of total: ", len(total))
        plt.legend()
        plt.xlabel("Timestamp (seconds)")    # xlabel for plot
        plt.ylabel("Frequency")             # ylabel for plot
        plt.title("Total time running", fontsize=15)    # title 
        plt.savefig('running_time_distribution')
        plt.show()

    def getCertainRangeList(self, total_time_lst):
        self.ready_to_plot_lst = []
        self.range0To2 = []
        self.range2To3 = []
        self.range3To6 = []
        self.range6To9 = []
        self.range9To20 = []
        for item in total_time_lst:
          if 0 < item and item <= 2:
            # print("in 0-3: ", item)
            self.ready_to_plot_lst.append(int(item))
            self.range0To2.append(item)
          elif 2 < item and item <= 3:
            self.ready_to_plot_lst.append(int(item))
            self.range2To3.append(item)
          elif 3 < item and item <= 6:
            # print("in 3-6: ", item)
            self.ready_to_plot_lst.append(int(item))
            self.range3To6.append(item)
          elif 6 < item and item <= 9:
            # print("in 6-9: ", item)       
            self.range6To9.append(item)
            self.ready_to_plot_lst.append(int(item))
          elif 9 < item and item <= 20:
            self.range9To20.append(item)        

if __name__ == '__main__':

    sc = TimeMeasure(2)
    sc.getDuration()

    # # small test
    # print("stop:",sc.total_stopped_time, "sum:", sum(sc.total_stopped_time), "percentage:",sum(sc.total_stopped_time) / 57600 * 100)
    # print("after delay:",sc.total_stopped_after_delay, "sum:",sum(sc.total_stopped_after_delay),"percentage:",sum(sc.total_stopped_after_delay)/57600*100)
    # print("run:",sc.total_running_time, "sum:", sum(sc.total_running_time), "percentage:",sum(sc.total_running_time) / 57600 * 100)
    # print("after delay:",sc.total_running_after_delay, "sum:",sum(sc.total_running_after_delay),"percentage:",sum(sc.total_running_after_delay)/57600*100)
