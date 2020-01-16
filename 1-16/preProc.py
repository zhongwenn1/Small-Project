import re
import os
import csv

class PreProc:
	def __init__(self, filenames):
		self.filenames = filenames
		self.openFile()

	# open files to read, and save to multiple 
	def openFile(self):
		# all 
		with open('in_window_logfile.csv', 'w') as f2, open('machine_decision_logfile.csv', 'w') as f3, \
			open('beam_diff_logfile.csv', 'w') as f4:
			self.writer = csv.writer(f2)
			self.writer2 = csv.writer(f3)
			self.writer3 = csv.writer(f4)
			self.writer.writerow(['Time', 'RFID', 'BagID', 'Travel Distance', 'Beam Diff', 'Linked'])
			self.writer2.writerow(['BagID', 'Machine Decision'])
			self.writer3.writerow(['Time', 'RFID', 'BagID', 'Travel Distance', 'Beam Diff'])
			for infile in self.filenames:
				with open(infile) as f:
					for line in f:
						time, rfID, bagID, travelDist, beamDiff, linked = "", "", "", 0, 0, 0
						self.inWindow(line)

						# machineStr = str(bagID) + " machine decision"
						machineStr = "machine decision"
						if machineStr in line:
							self.writer2.writerow([line.split(',')[3].split(' ')[4], line.split(',')[3].split(' ')[-1]])

						unlinked_msg = "is NOT in the window"
						fake_Rfid = "__I__"
						if unlinked_msg in line and str(bagID) in line and fake_Rfid not in line:
							self.writer3.writerow([line.split(',')[0], line.split(',')[3].split('[')[1].split(']')[0], \
								line.split(',')[3].split('[')[2].split(']')[0], line.split(',')[5].split(':')[1],\
								line.split(',')[6].split(' ')[2]])


	def inWindow(self, line):
		if "is in the window to link" in line:
			line = line.split(',')
			time = line[0]			
			if len(line) == 7:	# linked bags data
				rfID = line[3].split("[")[1].split("]")[0]
				bagID = line[3].split("[")[2].split("]")[0]
				# machineDec = " "
				travelDist = line[5].split(":")[1]
				beamDiff = line[6].split(":")[1].split(" ")[1]
				linked = 1
			else:
				rfID = ""
				bagID = line[3].split("[")[1].split("]")[0]
				# machineDec = " "
				travelDist = ""
				beamDiff = ""
				linked = 0
			self.writer.writerow([time, rfID, bagID, travelDist, beamDiff, linked])
