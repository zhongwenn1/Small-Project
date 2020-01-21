import re
import os
from datetime import datetime
import numpy as np

class scanner:
    def __init__(self, filenames):
        self.filenames = filenames
        self.total_stopped_time = []
        self.total_running_time = []
        self.scanning_start_time = 0
        self.idle_time = 0
        self.cleanFile()

    def cleanFile(self):
        self.total_stopped_time = []
        with open('scanner.txt', 'w') as f2:
            for infile in self.filenames:
                with open(infile) as f:
                    for line in f:
                        if ("Sent SCANNER" in line) or (": scanner [" in line):
                            f2.write(line)
        # f2.close()

    def getDatetime(self, time):
        date_time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
        return datetime.timestamp(date_time)

    def scanningList(self, line):
        if "SCANNER RUNNING message" in line:
            self.scanning_start_time = self.getDatetime(line.split(',')[0])

        if "SCANNER IDLE message and disabling RTR" in line and self.scanning_start_time != 0:
            self.scanning_stop_time = self.getDatetime(line.split(',')[0])
            self.total_running_time += (self.scanning_stop_time - self.scanning_start_time),

        if "[IDLE,IDLE_SS]" in line and self.scanning_start_time != 0:
            self.scanning_stop_time = self.getDatetime(line.split(',')[0])
            self.total_running_time += (self.scanning_stop_time - self.scanning_start_time),



    def getStopDuration(self):
        inRun, inScan, inIdle = False, False, False
        with open('scanner.txt') as f3:
            for line in f3:
                self.scanningList(line)
                
                if "2019-06-23 10:00:05.744190" in line:
                    break

                """ Now it has [0.08461713790893555, 64.8680830001831, 51.69665718078613, 54.1710638999939, 74.23957180976868, 12.398500204086304]
                    this block of code ignore the running start state while it detected with [SCAN,SCANNING_SS]
                if "SCANNER RUNNING message" in line:
                    fixed_start_time = self.getDatetime(line.split(',')[0])
                    self.scanning_start_time = self.getDatetime(line.split(',')[0])
                    inRun = True

                if ("[IDLE,IDLE_SS]" in line) and (self.scanning_start_time != 0):
                    # print(line)
                    idle = self.getDatetime(line.split(',')[0])
                    if inRun and not inScan and not inIdle: # first time meet idle
                        self.total_running_time += (idle - fixed_start_time),
                        print("in first if: ", line)
                    if inRun and inIdle and not inScan: # meet another idle [SCAN,...]
                        pass
                    if inRun and not inIdle and inScan:
                        self.total_running_time += (idle - self.scanning_start_time),
                        print("in second if: ", line)
                    inIdle = True
                    inScan = False                
                if "[SCAN,SCANNING_SS]" in line:
                    # print(line)

                    self.scanning_start_time = self.getDatetime(line.split(',')[0])
                    inScan = True
                    inIdle = False
                if "2019-06-23 10:00:05.744190" in line:
                    break
                """

        

if __name__ == '__main__':
    sc = scanner(['C:/Users/wzhong/Documents/temp/logfiles/AnalogicStandaloneType2_20190623.log'])
    sc.getStopDuration()
    print(sc.total_running_time)
