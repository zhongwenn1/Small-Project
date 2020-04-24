import csv
import os
import config as cfg

class PreProc:
    def __init__(self, filenames, ui):
        self.filenames = filenames
        self.ui = ui
        self.step = 0
        self.entrance_events = 0
        self.misread_entrance = 0
        self.found_prev_bag = 0
        self.total_bins = 0
        self.scanner_linked_RFID = 0
        self.found_no_bag = 0
        self.found_prev_bag = 0
        self.exit_events = 0
        self.misread_exit = 0
        self.bag_already_sent = 0
        self.lost_track_crusty_bag = 0
        self.exit_read_unlinked = 0
        self.writer = None
        self.writer2 = None
        self.writer3 = None
        self.f5 = None
        self.unlinked_list = []
        self.allow = False
        self.queue = []
        self.open_file()

    # Open files to read, and save to multiple separate files
    def open_file(self):
        cur_path = os.getcwd()
        self.ui.loading_dialog.pbar.setRange(0, len(self.filenames))
        self.ui.loading_dialog.pbar.setValue(self.step)
        self.ui.app.processEvents()
        dir_name = os.path.join(cur_path, "output")
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

        with open(os.path.join(dir_name, cfg.files['inWindow']), 'w') as f2, \
                open(os.path.join(dir_name, cfg.files['machineDec']), 'w') as f3, \
                open(os.path.join(dir_name, cfg.files['notInWindow']), 'w') as f4, \
                open(os.path.join(dir_name, cfg.files['stopRunTime']), 'w') as self.f5:
            self.writer = csv.writer(f2)
            self.writer2 = csv.writer(f3)
            self.writer3 = csv.writer(f4)
            self.writer.writerow(['Time', 'RFID', 'BagID', 'Travel Distance', 'Beam Diff', 'Linked'])
            self.writer2.writerow(['BagID', 'Machine Decision'])
            self.writer3.writerow(['Time', 'RFID', 'BagID', 'Travel Distance', 'Beam Diff'])

            for infile in self.filenames:
                with open(infile) as f:
                    for line in f:
                        self.in_window(line)
                        self.machine_decision(line)
                        self.not_in_window(line)
                        self.get_bin_num(line)
                        self.stop_run_time(line)
                        self.get_unlinked_list(line)
                    self.step = self.step + 1
                    self.ui.loading_dialog.pbar.setValue(self.step)
                    self.ui.app.processEvents()

        self.total_bins = self.entrance_events - self.misread_entrance - self.found_prev_bag
        self.unlinked_list.extend(self.queue)       # add remaining RFID in queue into unlinked list

    def get_unlinked_list(self, cline):
        if len(cline.split(',')) > 3:
            line = cline.split(',')[3]

            if "CREATED new bag" in line and "__I__" not in line:  # real rfid events
                if self.ui.type == '2':
                    if self.allow:
                        self.queue.append(line.split(' ')[cfg.type2['index']])
                        self.allow = False
                    elif len(self.queue) == 0 or (len(self.queue) != 0 and self.queue[-1] != line.split(' ')[cfg.type2['index']]):     # expect found previous bag, append into queue
                        self.queue.append(line.split(' ')[cfg.type2['index']])
                elif self.ui.type == '5':
                    if self.allow:
                        self.queue.append(line.split(' ')[cfg.type5['index']])
                        self.allow = False
                    elif len(self.queue) == 0 or (len(self.queue) != 0 and self.queue[-1] != line.split(' ')[cfg.type5['index']]):     # expect found previous bag, append into queue
                        self.queue.append(line.split(' ')[cfg.type5['index']])

            elif "Did not find the bag in the next zone" in line:
                self.allow = True

            elif "Linked internal bag_id" in line and ("__I__" not in line):
                while self.queue[0] != line.split(' ')[7]:
                    self.unlinked_list.append(self.queue.pop(0))
                self.queue.pop(0)

            elif "is unlinked" in line and ("__I__" not in line):
                self.allow = True

    def get_bin_num(self, line):
        if "CREATED new bag" in line:
            self.entrance_events += 1
        elif "Unable to read RFID tag of bin at zone" in line:
            self.misread_entrance += 1
        elif "Read last RFID" in line:
            if "Did not find the bag" in line:
                self.found_no_bag += 1
            elif "found the previous bag" in line:
                self.found_prev_bag += 1
        elif "Linked internal bag_id" in line and "__I__" not in line:
            self.scanner_linked_RFID += 1
        elif "Zone[4]::OnEntry: call" in line:
            self.exit_events += 1
        elif "Zone 4::OnEntry: call" in line:
            self.exit_events += 1
        elif "OnEntry: Unable to read RFID tag" in line:
            self.misread_exit += 1
        elif "we already sent that bag to the next zone; moving it back" in line:
            self.bag_already_sent += 1
        elif "Removing crusty normal bag from front" in line:
            self.lost_track_crusty_bag += 1
        elif "is unlinked" in line and "__I__" not in line:
            self.exit_read_unlinked += 1

    def in_window(self, line):
        if "is in the window to link" in line:
            line = line.split(',')
            time = line[0]
            if len(line) == 7:  # linked bags data
                rfID = line[3].split("[")[1].split("]")[0]
                bagID = line[3].split("[")[2].split("]")[0]
                travelDist = line[5].split(":")[1]
                beamDiff = line[6].split(":")[1].split(" ")[1]
                linked = 1
            else:
                rfID = ""
                bagID = line[3].split("[")[1].split("]")[0]
                travelDist = ""
                beamDiff = ""
                linked = 0
            self.writer.writerow([time, rfID, bagID, travelDist, beamDiff, linked])

    def not_in_window(self, line):
        if "is NOT in the window to link" in line:  # test for contain both real rfid and fake id
            self.writer3.writerow([line.split(',')[0], line.split(',')[3].split('[')[1].split(']')[0],
                                line.split(',')[3].split('[')[2].split(']')[0], line.split(',')[5].split(':')[1],
                                line.split(',')[6].split(' ')[2]])

    def machine_decision(self, line):
        if "machine decision" in line:
            self.writer2.writerow([line.split(',')[3].split(' ')[4], line.split(',')[3].split(' ')[-1]])

    def stop_run_time(self, line):
        if "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line or "Sent SCANNER" in line:
            self.f5.write(line)