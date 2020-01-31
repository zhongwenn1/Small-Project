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
        self.very_start_time = 0
        self.very_end_time = 0
        self.delay = delay
        self.count = 0
        self.count2 = 0
        self.total_time_save = 0
        self.total_time_add = 0

    def getDuration(self):
        self.inRun, self.inIdle = False, False
        self.inRund, self.inIdled = False, False
        first = True
        start = False
        with open('runtime_.txt') as f3:
        # with open('test.txt') as f3:
            for line in f3:               
                # if line.split(',')[0] == '2019-06-17 04:08:47.478256':        # check if date to date time diff is not contain
                #     break
                # if line.split(',')[0] == '2019-06-16 19:28:05.609377':
                #     start = True                
                if first:
                    # self.very_start_time = self.getDatetime(line.split(',')[0])
                    first = False

                # self.runList(line)
                self.stopList(line)               
                self.fakestopList(line)            
                self.delayStopList(line, self.delay)
        #         self.very_end_time = self.getDatetime(line.split(',')[0])
        # self.total_machine_running = self.very_end_time - self.very_start_time

    def getDatetime(self, time):
        date_time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
        return datetime.timestamp(date_time)

    def runList(self, line):
        if "Sent SCANNER IDLE" in line:
            self.scanning_end_time = self.getDatetime(line.split(',')[0])
            self.total_running_time += (self.scanning_end_time - self.scanning_start_time),
        elif "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line:
            self.scanning_start_time = self.getDatetime(line.split(',')[0])

    def fakestopList(self, line):
        if "SCANNER RUNNING message" in line:
            self.fake_idle_end_time = self.getDatetime(line.split(',')[0])
            self.fake_total_stopped_time += (self.fake_idle_end_time - self.fake_idle_start_time),

        elif "SCANNER IDLE message and disabling RTR" in line:
            self.fake_idle_start_time = self.getDatetime(line.split(',')[0])


    def stopList(self, line):
        
        if "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line and (self.inIdle and self.inRun):
            # SCANNER RUNNING message" in line:
            self.idle_end_time = self.getDatetime(line.split(',')[0])
            self.total_stopped_time += (self.idle_end_time - self.idle_start_time),
            self.inIdle = False
            self.inRun = False

        elif "SCANNER RUNNING message" in line:
            self.prev_time = self.getDatetime(line.split(',')[0]) - self.idle_start_time
            self.inRun = True

        elif "SCANNER IDLE message and disabling RTR" in line: # or "[IDLE,IDLE_SS]" in line) and self.idle_start_time != 0:
            self.idle_start_time = self.getDatetime(line.split(',')[0])
            if self.inRun:
                self.total_stopped_time += self.prev_time,
            self.inIdle = True

    def delayStopList(self, line, delay):
        time = self.getDatetime(line.split(',')[0])
        if "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line and (self.inIdled and self.inRund):
            # print("in")
            if self.check_time <= delay:                
                # diff = delay
                diff = self.check_time      # this should be the fake stop time not delay as the delay will be cancelled if it receiveds the fake stop before delay
                self.count += 1
                self.total_time_save += (time - self.start - diff)
            else:
                # diff = time - self.start
                diff = time - self.start + delay    # add the delay to this also. It will be added to all trays with a greater than 2 second delay
                self.count2 += 1
                self.total_time_add += delay
            self.total_stopped_after_delay.append(diff)
            self.inRund = False
            self.inIdled = False
        elif "SCANNER RUNNING message" in line:
            self.check_time = time - self.start
            self.inRund = True
            # self.inIdled = False
        elif "SCANNER IDLE message" in line:
            self.start = time
            if self.inRund:
                diff = self.check_time
                self.total_stopped_after_delay.append(diff)
                self.count2 += 1
                self.total_time_add += delay            
            self.inIdled = True
            # self.inRund = False

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

    def showStopDistribution(self, range0To2, range2To3, range3To6, range6To9, total_stopped_inrange, name, total):
        plt.bar(['0s - 2s','2s - 3s', '3s - 6s','6s - 9s'], [len(range0To2),len(range2To3),len(range3To6),len(range6To9)], label="Stop time")
        print(name, ": \nrange 0s - 2s: ", round(len(range0To2)/len(total) * 100, 2), "%\nnums in 0-2: ", len(range0To2), " out of total: ", len(total))
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

    start_time = timeit.default_timer()
    # code you want to evaluate
    sc = TimeMeasure(2.0)
    sc.getDuration()
    # print(sc.total_stopped_after_delay)
    # sm = Simulation(2)
    # total_stopped_after_delay = sm.openFile()
    # # print(sc.total_stopped_time, len(sc.total_stopped_time))
    sc.showDistribution(sc.fake_total_stopped_time, 'Fake total time stopped')
    sc.getCertainRangeList(sc.fake_total_stopped_time)
    sc.showStopDistribution(sc.range0To2, sc.range2To3, sc.range3To6, sc.range6To9, sc.ready_to_plot_lst, "fake total time", sc.fake_total_stopped_time)     

    sc.showDistribution(sc.total_stopped_time, 'Total time stopped')
    sc.getCertainRangeList(sc.total_stopped_time)
    sc.showStopDistribution(sc.range0To2, sc.range2To3, sc.range3To6, sc.range6To9, sc.ready_to_plot_lst, "stop total time", sc.total_stopped_time)  
    print("stop:",len(sc.total_stopped_time), "sum:", sum(sc.total_stopped_time), "percentage:",sum(sc.total_stopped_time) / 57600 * 100)

    sc.showDistribution(sc.total_stopped_after_delay, 'Total time stopped after delay')
    sc.getCertainRangeList(sc.total_stopped_after_delay)
    sc.showStopDistribution(sc.range0To2, sc.range2To3, sc.range3To6, sc.range6To9, sc.ready_to_plot_lst, "stop total time after 2s delay", sc.total_stopped_after_delay)
    print("after delay:",len(sc.total_stopped_after_delay), "sum:",sum(sc.total_stopped_after_delay),"percentage:",sum(sc.total_stopped_after_delay)/57600*100)
    print("total time save:",sc.total_time_save,"on",sc.count,"items")
    print("total time add:",sc.total_time_add,"on",sc.count2,"items")
    # sc.showDistribution(sc.total_running_time, 'Total time running')
    # sc.getCertainRangeList(sc.total_running_time)
    # sc.showRunDistribution(sc.range0To2, sc.range2To3, sc.range3To6, sc.range6To9, sc.ready_to_plot_lst, sc.total_running_time)

    # kwargs = dict(alpha=0.5, bins=100)
    
    # # histogram for frequency
    # plt.hist(sc.total_stopped_time, **kwargs, label='actual stop')
    # plt.hist(sc.fake_total_stopped_time, **kwargs, label='request to run')

    # # histogram for density with curve line   
    # kwargs = dict(hist_kws={'alpha':.6}, kde_kws={'linewidth':2})
    # sns.distplot(sc.total_stopped_time, **kwargs, label='actual stop')   
    # sns.distplot(sc.fake_total_stopped_time, **kwargs, label='request to run')

    # # density with shade
    # sns.distplot(sc.total_stopped_time, hist = False, kde = True, kde_kws = {'shade': True, 'linewidth': 3}, label = 'actual stop')    
    # sns.distplot(sc.fake_total_stopped_time, hist = False, kde = True, kde_kws = {'shade': True, 'linewidth': 3}, label = 'fake stop')

    # plt.legend(prop={'size': 12})
    # plt.title('request to run VS actual stop')
    # plt.xlabel('timestamp (seconds)')
    # plt.ylabel('Density')
    # plt.show()

    # density with shade
    sns.distplot(sc.total_stopped_time, hist = False, kde = True, kde_kws = {'shade': True, 'linewidth': 3}, label = 'before delay')    
    sns.distplot(sc.total_stopped_after_delay, hist = False, kde = True, kde_kws = {'shade': True, 'linewidth': 3}, label = 'after delay')

    plt.legend(prop={'size': 12})
    plt.title('stop time distribution')
    plt.xlabel('timestamp (seconds)')
    plt.ylabel('Density')
    plt.show()   

    # print('fake:',len(sc.fake_total_stopped_time),sum(sc.fake_total_stopped_time) / 57600 * 100)
    # print('stop:',len(sc.total_stopped_time),sum(sc.total_stopped_time) / 57600 * 100)
    # print('add delay:',len(sc.total_stopped_after_delay),sum(sc.total_stopped_after_delay) / 57600 * 100)
    # print('run:',len(sc.total_running_time),sum(sc.total_running_time) / 57600 * 100)
    # print('effective with delay:',sc.count)

    # small test
    
   
    # print('stopped time before delay:', sum(sc.total_stopped_time), 'Percentage of stopped time before delay / total:', round((sum(sc.total_stopped_time) / sc.total_machine_running * 100),2), "%")
    # print('stopped time after delay:', sum(sc.total_stopped_after_delay), 'Percentage of stopped time after delay / total:', round((sum(sc.total_stopped_after_delay) / sc.total_machine_running * 100),2), "%")
    # print('running time:', sum(sc.total_running_time), 'Percentage of running time / total:', round((sum(sc.total_running_time) / sc.total_machine_running * 100),2), "%")

    # not sure if below is correct
    # kwargs = dict(alpha=0.5, bins=100)
    # plt.hist(sc.total_stopped_time, **kwargs, color='g', label='Stop')
    # plt.hist(sc.total_running_time, **kwargs, color='b', label='Running')
    # plt.gca().set(title='Frequency Histogram', ylabel='Frequency')
    # plt.xlim(50,75)
    # plt.legend()
    # plt.show()

    elapsed = timeit.default_timer() - start_time
    # print("time for reading file and clean: ", elapsed)
    
  
    # start_time1 = timeit.default_timer()
    # sc.getStopDuration()
    # elapsed1 = timeit.default_timer() - start_time1
    

    # start_time4 = timeit.default_timer()
    # print(sc.total_running_time)
    # elapsed4 = timeit.default_timer() - start_time4
    # print("time for reading file and clean: ", elapsed)
    # print("time for get stop duration: ", elapsed1)
    # print("time for printing list: ", elapsed4)

    # # print(sc.total_running_time)
    # start_time2 = timeit.default_timer()
    # sc.showStopDistribution(sc.total_running_time)
    # elapsed2 = timeit.default_timer() - start_time2
    # print("time for get stop histogram: ", elapsed2)

    # this block get variables from ini file and update value back into ini file
    # config = configparser.ConfigParser()
    # config.read('example.ini')
    # config.set('Conveyor', 'total_time_running', '666')
    # with open('example.ini', 'w') as configfile:
    #     config.write(configfile)
    # print(config['Conveyor']['total_time_running'])



    # start_time = timeit.default_timer()
    # plt.bar([2,4,6,8,10],[8,6,2,5,6], label="Example two", color='g')
    # plt.legend()
    # plt.xlabel('bar number')
    # plt.ylabel('bar height')

    # plt.title('Epic Graph\nAnother Line! Whoa')
    
    # elapsed = timeit.default_timer() - start_time
    # print("time for reading file and clean: ", elapsed)
    # plt.show()