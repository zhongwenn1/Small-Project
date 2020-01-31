import re
import os
import csv
from datetime import datetime
import numpy as np

class PreProc:
	def __init__(self, filenames):
		self.filenames = filenames
		self.openFile()		# comment this for now, to test running time list and stop time list 1/21 9:57am

	# open files to read, and save to multiple 
	def openFile(self):
		# all 
		with open('in_window_logfile.csv', 'w') as f2, open('machine_decision_logfile.csv', 'w') as f3, \
			open('not_in_window_logfile.csv', 'w') as f4, open('runtime_.txt', 'w') as self.f5:
			self.writer = csv.writer(f2)
			self.writer2 = csv.writer(f3)
			self.writer3 = csv.writer(f4)
			self.writer.writerow(['Time', 'RFID', 'BagID', 'Travel Distance', 'Beam Diff', 'Linked'])
			self.writer2.writerow(['BagID', 'Machine Decision'])
			self.writer3.writerow(['Time', 'RFID', 'BagID', 'Travel Distance', 'Beam Diff'])
			for infile in self.filenames:
				running, idle = False, False
				with open(infile) as f:
					for line in f:
						time, rfID, bagID, travelDist, beamDiff, linked = "", "", "", 0, 0, 0
						# self.inWindow(line)
						# self.machineDec(line)
						# self.notInWindow(line)
						self.stopRunTime(line)


	def inWindow(self, line):
		if "is in the window to link" in line:
			line = line.split(',')
			time = line[0]			
			if len(line) == 7:	# linked bags data
				rfID = line[3].split("[")[1].split("]")[0]
				bagID = line[3].split("[")[2].split("]")[0]
				# machineDec = " "	# will append this col after join df
				travelDist = line[5].split(":")[1]
				beamDiff = line[6].split(":")[1].split(" ")[1]
				linked = 1
			else:
				rfID = ""
				bagID = line[3].split("[")[1].split("]")[0]
				# machineDec = " "	# will append this col after join df
				travelDist = ""
				beamDiff = ""
				linked = 0
			self.writer.writerow([time, rfID, bagID, travelDist, beamDiff, linked])
	
	def notInWindow(self, line):
		# fake_Rfid = "__I__"
		if "is NOT in the window" in line:	# test for contain both real rfid and fake id
			self.writer3.writerow([line.split(',')[0], line.split(',')[3].split('[')[1].split(']')[0], \
				line.split(',')[3].split('[')[2].split(']')[0], line.split(',')[5].split(':')[1],\
				line.split(',')[6].split(' ')[2]])

	def machineDec(self, line):
		if "machine decision" in line:
			self.writer2.writerow([line.split(',')[3].split(' ')[4], line.split(',')[3].split(' ')[-1]])

	def stopRunTime(self, line):
		if "[SCAN,SCANNING_SS] conveyor [RUNNING]" in line or "Sent SCANNER" in line:
			self.f5.write(line)  

if __name__ == '__main__':
  fp = PreProc(['C:/Users/wzhong/Documents/temp/logfiles/AnalogicStandaloneType2_20190624.log'])