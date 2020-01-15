import re
import os
import csv
import pandas as pd

class PreProc:
	def __init__(self, filenames):
		self.filenames = filenames
		self.openFile()

	def openFile(self):
		for infile in self.filenames:
			with open(infile) as f, open('in_window_logfile.csv', 'w') as f2, open('machine_decision_logfile.csv', 'w') as f3:
				self.writer = csv.writer(f2)
				self.writer2 = csv.writer(f3)
				self.writer.writerow(['Time', 'RFID', 'BagID', 'Travel Distance', 'Beam Diff', 'Linked'])
				self.writer2.writerow(['BagID', 'Machine Decision'])
				for line in f:
					time, rfID, bagID, travelDist, beamDiff, linked = "", "", "", 0, 0, 0
					
					self.inWindow(line)

							# writer.writerow([time, rfID, bagID, machineDec, travelDist, beamDiff, linked])

					machineStr = str(bagID) + " machine decision"
					if machineStr in line:
						# print(line.split(',')[3].split(' ')[4], line.split(',')[3].split(' ')[-1])
						self.writer2.writerow([line.split(',')[3].split(' ')[4], line.split(',')[3].split(' ')[-1]])

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

"""
df = pd.read_csv('in_window_logfile.csv')
df['Time'] = pd.to_datetime(df['Time'])
# print(df)

# seeking for machine decision for each bagID
# df.at[0, 'Machine Decision'] = 'fffd'
print(df)
print(df.loc[df['BagID'] == 55717])

df2 = pd.read_csv('machine_decision_logfile.csv')
print(df2)
# df2 = df2.groupby(['BagID'])['Machine Decision'].apply(', '.join).reset_index()
df2 = df2.drop_duplicates()	# takes slow, need to find another way to take care of duplicate rows
print(df2)

dfinal = df.merge(df2, on="BagID", how='inner')
print(dfinal)
"""

# for i, row in df.iterrows():
# 	bagID = row['BagID']
# 	with open(r"AnalogicStandaloneType2_20190623.log") as f:
# 		infile = f.readlines()
# 	for line in infile:
# 		if str(bagID) + " machine decision" in line:
# 			print(line)

	# print(bagID)
	# if i == 10:
	# 	break

		# machineStr = str(bagID) + " machine decision"
		# if machineStr in line:
		# 	row = df.loc[df['BagID'] == bagID]
		# 	df.at[row, 'Machine Decision'] = line.split(',')[3].split(' ')[4]
			# print(line)

# noRF = pd.isnull(df['RFID'])	# seeking for bag_id without rfid
# print(df[noRF])
# haveRF = pd.notnull(df['RFID'])	# seeking for bag_id with rfid
# print(df[haveRF])

# null_data = df[df.isnull().any(axis=1)]
# print(df.dtypes)

# print(df.iloc[2])

# # use regex to match relevant log lines
# scanned_regex = re.compile(r".*is in the window to link.*$")

# # output file, all matched line will write into this file
# output_filename = os.path.normpath("small.log")

# # with concurrent.futures.ProcessPoolExecutor() as executor:

# # write to the output file
# with open(output_filename, "w") as out_file:
# 	out_file.write("")

# with open(output_filename, "a") as out_file:	
# 	with open("AnalogicStandaloneType2_20190623.log") as origin_file:
# 	    for line in origin_file:
# 	    	# out_file.write(line)
# 	    	if scanned_regex.search(line):
# 	        # if 'should have reached attenuation' in line:
# 	          # print (line)

# 	          out_file.write(line)
