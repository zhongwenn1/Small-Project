import csv

class PreProc:
	def __init__(self, filenames):
		self.filenames = filenames
		self.entrance_events = 0
		self.misread_entrance = 0
		self.found_prev_bag = 0
		self.total_bins = 0
		self.scanner_linked_rfid = 0
		self.found_no_bag = 0
		self.found_prev_bag = 0
		self.exit_events = 0
		self.misread_exit = 0
		self.bag_already_sent = 0
		self.lost_track_crusty_bag = 0
		self.exit_read_unlinked = 0
		self.openFile()		# comment this for now, to test running time list and stop time list 1/21 9:57am

	# open files to read, and save to multiple separate files 
	def openFile(self):
		# all 
		with open('in_window_logfile.csv', 'w') as f2, open('machine_decision_logfile.csv', 'w') as f3, \
		open('not_in_window_logfile.csv', 'w') as f4:
			self.writer = csv.writer(f2)
			self.writer2 = csv.writer(f3)
			self.writer3 = csv.writer(f4)
			self.writer.writerow(['Time', 'RFID', 'BagID', 'Travel Distance', 'Beam Diff', 'Linked'])
			self.writer2.writerow(['BagID', 'Machine Decision'])
			self.writer3.writerow(['Time', 'RFID', 'BagID', 'Travel Distance', 'Beam Diff'])

			for infile in self.filenames:
				with open(infile) as f:
					for line in f:
						self.inWindow(line)
						self.machineDec(line)
						self.notInWindow(line)
						self.getBinNum(line)

		self.total_bins = self.entrance_events - self.misread_entrance - self.found_prev_bag

	def getBinNum(self, cmline):
		if "CREATED new bag" in cmline:
			self.entrance_events += 1
		elif "Unable to read RFID tag of bin at zone" in cmline:
			self.misread_entrance += 1
		elif "Read last RFID" in cmline:
			if "Did not find the bag" in cmline:
				self.found_no_bag += 1
			elif "found the previous bag" in cmline:
				self.found_prev_bag += 1
		elif "Linked internal bag_id" in cmline and "__I__" not in cmline:
			self.scanner_linked_rfid += 1
		elif "Zone[4]::OnEntry: call" in cmline:
			self.exit_events += 1
		elif "Zone 4::OnEntry: call" in cmline:
			self.exit_events += 1
		elif "OnEntry: Unable to read RFID tag" in cmline:
			self.misread_exit += 1
		elif "we already sent that bag to the next zone; moving it back" in cmline:
			self.bag_already_sent += 1
		elif "Removing crusty normal bag from front" in cmline:
			self.lost_track_crusty_bag += 1
		elif "is unlinked" in cmline and "__I__" not in cmline:
			self.exit_read_unlinked += 1


	def inWindow(self, line):
		if "is in the window to link" in line:
			line = line.split(',')
			time = line[0]			
			if len(line) == 7:	# linked bags data
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
	
	def notInWindow(self, line):
		if "is NOT in the window to link" in line:	# test for contain both real rfid and fake id
			self.writer3.writerow([line.split(',')[0], line.split(',')[3].split('[')[1].split(']')[0], \
				line.split(',')[3].split('[')[2].split(']')[0], line.split(',')[5].split(':')[1],\
				line.split(',')[6].split(' ')[2]])

	def machineDec(self, line):
		if "machine decision" in line:
			self.writer2.writerow([line.split(',')[3].split(' ')[4], line.split(',')[3].split(' ')[-1]])
