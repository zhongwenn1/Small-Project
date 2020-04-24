import os
from datetime import datetime
import config as cfg

class TimeMeasure:
    def __init__(self, delay):
        self.total_stopped_time = []
        self.total_running_time = []
        self.total_stopped_after_delay = []
        self.total_running_after_delay = []
        self.total_time_before_delay = 0
        self.total_time_after_delay = 0
        self.very_start_time = 0
        self.very_end_time = 0
        self.idle_start_time = 0
        self.idle_end_time = 0
        self.delay = delay
        self.count = 0
        self.prevsrun = 0
        self.run = 0
        self.prev = 0
        self.first_time = 0
        self.last_time = 0
        self.cur_path = os.getcwd()
        self.time_add = 0
        self.time_save = 0
        self.update, self.inRun, self.inIdle, self.inSRun, self.seen = False, False, False, False, False         # add check condition to prevent two or more "RUN" in a sequnce
        self.is_first_srun = False


    def get_duration(self):
        with open(os.path.join(self.cur_path, 'output' , cfg.files['stopRunTime'])) as f3, \
                open(os.path.join(self.cur_path, 'output', cfg.files['simulation']), 'w') as self.f4:
            for line in f3:
                self.simulate_delay(line, self.delay)


    def simulate_delay(self, line, delay):
        if "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line:
            self.srun = self.get_float_datetime(line.split(',')[0])
            if not self.update:
                if self.inIdle:                                                # add check for "RUN" - "SRUN" sequence
                    self.diff6 = self.srun - self.idle                         # add check for "RUN" - "SRUN" sequence
                    self.f4.write((self.get_format_datetime(self.prev + delay)) + ',' + " IDLE DELAY\n")
                    self.f4.write((self.get_format_datetime(self.prev + self.diff6 + delay)+','+(',').join(line.split(',')[1:])))    # add check for "RUN" - "SRUN" sequence
                elif not self.inSRun:
                    self.diff5 = self.srun - self.run
                    self.f4.write((self.get_format_datetime(self.prev + self.diff5)+','+(',').join(line.split(',')[1:])))
                    self.prev = self.prev + self.diff5
                else:
                    self.diff4 = self.srun - self.prevsrun
                    self.f4.write((self.get_format_datetime(self.prev + self.diff4)+','+(',').join(line.split(',')[1:])))
                    self.prev = self.prev + self.diff4
            else:                           # try to add update condition, record first srun and subtract until idle
                self.time_save += self.srun - self.run
                self.f4.write(self.get_format_datetime(self.prev) + ', scanner [SCAN,SCANNING_SS] conveyor [RUNNING]\n')
                self.count += 1           # here detect the duration that are in the delay range
                if self.is_first_srun:
                    self.first_srun = self.get_float_datetime(line.split(',')[0])
                    self.is_first_srun = False

                self.update = False           # add update condition, record first srun and subtract until idle
            self.inSRun = True
            self.inIdle = False               # add check for "RUN" - "SRUN" sequence
            self.seen = False                 # add check condition to prevent two or more "RUN" in a sequnce
            self.prevsrun = self.get_float_datetime(line.split(',')[0])
        elif "Sent SCANNER IDLE" in line:
            self.idle = self.get_float_datetime(line.split(',')[0])
            if self.update:
                self.diff1 = self.idle - self.first_srun

            else:
                self.diff1 = self.idle - self.srun
            self.diff11 = self.idle - self.run
            if self.inRun and not self.inSRun:  # add inRun check, special treat for run & not srun condition
                self.f4.write((self.get_format_datetime(self.prev + self.diff11)) + ',' + (',').join(line.split(',')[1:]))
                self.prev = self.prev + self.diff11
            elif self.inSRun:
                self.f4.write((self.get_format_datetime(self.prev + self.diff1)) + ',' + (',').join(line.split(',')[1:]))
                self.prev = self.prev + self.diff1

            self.is_first_srun = True
            self.inIdle = True              # add check for "RUN" - "SRUN" sequence
            self.inSRun = False
            self.inRun = False              # add inRun check, special treat for run & not srun condition
            self.update = False             # add update condition, record first srun and subtract until idle
            self.seen = False                                       # add check condition to prevent two or more "RUN" in a sequnce
        elif "Sent SCANNER RUNNING" in line and not self.seen:      # add check condition to prevent two or more "RUN" in a sequnce
            self.inRun = True               # add inRun check, special treat for run & not srun condition
            self.run = self.get_float_datetime(line.split(',')[0])
            self.diff2 = self.run - self.idle
            if self.diff2 <= delay:
                self.f4.write((self.get_format_datetime(self.prev + self.diff2)) + ','+ (',').join(line.split(',')[1:]))
                self.prev = self.prev + self.diff2
                self.update = True
                self.is_first_srun = True

            else:
                if self.inIdle:
                    self.f4.write((self.get_format_datetime(self.prev + delay)) + ',' + " IDLE DELAY\n")
                self.f4.write((self.get_format_datetime(self.prev + self.diff2 + delay)) + ','+ (',').join(line.split(',')[1:]))
                self.prev = self.prev + self.diff2 + delay
                self.time_add += self.delay
            self.inSRun = False
            self.inIdle = False                                     # add check for "RUN" - "SRUN" sequence
            self.seen = True                                        # add check condition to prevent two or more "RUN" in a sequnce

    def get_float_datetime(self, time):
        date_time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
        return datetime.timestamp(date_time)

    def get_format_datetime(self, time):
        return datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S.%f')

    def get_stop_list(self, fname):
        inIdle, inRun, start = False, False, True
        total_stopped_time = []
        with open(os.path.join(self.cur_path, 'output', fname)) as f:
            for line in f:
                if start:
                    self.first_time = self.get_float_datetime(line.split(',')[0])
                    start = False
                if "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line and (inIdle and inRun):
                    self.idle_end_time = self.get_float_datetime(line.split(',')[0])
                    total_stopped_time += (self.idle_end_time - self.idle_start_time),
                    inIdle = False
                    inRun = False

                elif "SCANNER RUNNING message" in line:
                    self.prev_time = self.get_float_datetime(line.split(',')[0]) - self.idle_start_time
                    inRun = True

                elif "SCANNER IDLE message and disabling RTR" in line:
                    if inRun:
                        total_stopped_time += self.get_float_datetime(line.split(',')[0]) - self.idle_start_time,
                    inIdle = True
                    inRun = False
                    self.idle_start_time = self.get_float_datetime(line.split(',')[0])

                self.last_time = self.get_float_datetime(line.split(',')[0])
        return total_stopped_time, self.last_time - self.first_time

    def get_summary(self):
        self.total_stopped_time, self.total_time_before_delay = self.get_stop_list(cfg.files['stopRunTime'])
        self.total_stopped_after_delay, self.total_time_after_delay = self.get_stop_list(cfg.files['simulation'])
