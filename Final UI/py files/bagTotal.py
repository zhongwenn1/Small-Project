"""
This file is to output counts for entrance/exit events
	entrance_events, misread_at_entrance, read_last_rfid(found_previous_bag & found_no_bag), rfid_at_entrance

		rfid_at_entrance satisfy the calculation below:
			rfid_at_entrance = entrance_events - (misread_at_entrance + read_last_rfid)

		one way to ensure that rfid_at_entrance is actual rfid count:
			actual_rfid_at_entrance = rfid_at_entrance + found_no_bag
			(reads last rfid just exit at zone 4, reads same rfid at entrance again)

	exit_events, misread_at_exit, rfid_read_moveback, crusty_bag_removed, rfid_at_exit
		
		rfid_at_exit satisfy the calculation below:
			rfid_at_exit = exit_events - misread_at_exit

		if want to satisfy the counts are the same for entrance/exit rfid read:
			assumption: rfid reads at entrance should be same as reads at exit
			solution: take other action as consideration, such as 
						rfid read but bag already sent to next zone(results in less counts, so we need to add it back), 
						and removing crusty bag from front(results in more counts, subtract this counts)
				actual_rfid_at_exit = actual_rfid_at_entrance + rfid_read_moveback - crusty_bag_removed

		now we have actual_rfid_at_entrance = actual_rfid_at_exit

running instruction:
	python xxx.py log_file_path

additional information:
2020-01-14 15:06:57.745186, INFO, BHS_INTF, BagTotals: { "attenuation_events": 3, "entrance events": 3, "exit events": 3, "cleared": 0, 
"rejected": 0, "lost_tracking": 0, “unlinked”: 0, "entrance_rfid_misreads": 0, "exit_rfid_misreads": 0, "oversize_bags": 0, "cut_bags": 0, }

"attenuation_events" : AvanconSystem/Command/AttenuationCommand.cpp ln20 - ln 20
"entrance events" : AvanconSystem/Zone/AvanconZoneEntrance.cpp ln130 - ln129
"exit events" : AvanconSystem/Zone/AvanconZoneExitWithRfid.cpp ln148 - ln136
"cleared" : AvanconSystem/Zone/AvanconZoneExitWithRfid.cpp ln520 - ln493
            AvanconSystem/Command/PvsDecisionWithDirverterCommand.cpp ln89 - ln89
"rejected" : AvanconSystem/Zone/AvanconZoneExitWithRfid.cpp ln534 - ln504
            AvanconSystem/Command/PvsDecisionWithDiverterCommand.cpp ln98 - ln97
"lost_tracking" : AvanconSystem/Zone/AvanconZoneExitWithRfid.cpp ln359 - ln346
“unlinked” : AvanconSystem/Zone/AvanconZoneExitWithRfid.cpp ln470 - ln445
"entrance_rfid_misreads" : AvanconSystem/Zone/AvanconZoneEntrance.cpp ln96 - ln96
"exit_rfid_misreads" : AvanconSystem/Zone/AvanconZoneExitWithRfid.cpp ln77 - ln77
"oversize_bags" : 
"cut_bags":
"lost tracking": AvanconSystem/AvaconSystem.cpp ln890 - ln900
"""

import re
import ast
import json

class BagTotal:
	def __init__(self, filename, type):
		self.filename = filename
		self.type = type
		self.atten_events = 0
		self.entrance_events = 0
		self.misread_entrance = 0
		self.found_prev_bag = 0
		self.found_no_bag = 0
		self.rfid_entrance = 0
		self.exit_events = 0
		self.misread_exit = 0
		self.rfid_exit = 0
		self.rfid_read_moveback = 0
		self.crusty_bag_removed = 0
		self.lost_tracking = 0
		self.queue = []
		self.unlinked = []
		self.zone4 = []
		self.linked_count = 0
		self.total_bins = 0		
		self.readLine()
		self.readInfo()


	def readLine(self):
		# i = 0
		self.notallow = False
		with open(self.filename) as f:
			for line in f:
				# cmline = line.split(',')
				# if len(cmline) >= 3:
				if len(line.split(','))<3:
					continue
				line = line.split(',')[3]
				# print(line)
				self.getBagCount(line)
				self.getUnlinkedBag(line)

		print(self.filename)
		print("%s: %d"% ("entrance_events",self.entrance_events))
		print("%s: %d"% ("entrance_rfid_misread",self.misread_entrance))
		print("%s: %d, %s: %d"% ("\tread last RFID:\t(found previous bag)",self.found_prev_bag,"\n\t\t\t(Did not find bag in next zone, allow this read as is)",self.found_no_bag))
		print("%s: %d"% ("RFID at entrance",self.rfid_entrance))
		print("%s: %d"% ("Attenutaion events",self.atten_events))
		print("%s: %d"% ("exit_events",self.exit_events))
		print("%s: %d"% ("exit_rfid_misreads",self.misread_exit))
		print("%s: %d"% ("\tRFID read but bag already sent to next zone",self.rfid_read_moveback))
		print("%s: %d"% ("\tRemoving crusty normal bag from front",self.crusty_bag_removed))
		print("%s: %d"% ("RFID at exit",self.rfid_exit))
		print("%s: %d"% ("Lost tracking",self.lost_tracking))

		print("----------------------")
		unlinked_count = len(self.unlinked)+len(self.queue)
		print("Total bins:",self.total_bins)
		print("Total unlinked by queue calculation:",unlinked_count)
		print("Total linked:",self.linked_count)
		print("Total unlinked by substract from total_bins - linked_count:",self.total_bins-self.linked_count)

		print("\n")
		print("Actual rfid reads entrance = RFID at entrance + allowed bag")
		print("Actual rfid reads exit = RFID at exit + crusty bag - move back bag")
		print("Loose bags = exit misreads - crusty bag + move back bag")

	def getBagCount(self, cmline):
		if "CREATED new bag" in cmline:
			self.entrance_events += 1
		elif "Unable to read RFID tag of bin at zone" in cmline:		# get rid of __I__ bag
			self.misread_entrance += 1
		elif "Read last RFID" in cmline:
			if "found the previous bag" in cmline:
				self.found_prev_bag += 1
			elif "Did not find the bag" in cmline:
				self.found_no_bag += 1
		elif "RFID tag read at the entrance" in cmline:
			self.rfid_entrance += 1
		elif "is in the window to link" in cmline:
			self.atten_events += 1
		elif "Zone[4]::OnEntry: call" in cmline or "Zone 4::OnEntry: call" in cmline:
			self.exit_events += 1
		elif "OnEntry: Unable to read RFID tag" in cmline:
			self.misread_exit += 1
		elif "Zone[4]::OnEntry: Read tag" in cmline or "Zone 4::OnEntry: Read tag" in cmline:
			self.rfid_exit += 1
		elif "we already sent that bag to the next zone; moving it back" in cmline:
			self.rfid_read_moveback += 1
		elif "Removing crusty normal bag from front" in cmline:
			self.crusty_bag_removed += 1
		# elif "Lost Tracking" in cmline[-1]:
			self.lost_tracking += 1

	def getUnlinkedBag(self, line):

		if re.search("CREATED new bag", line) and not re.search("__I__", line):		# real rfid events
			self.total_bins += 1

			if not self.notallow:
				if self.type == 2:
					self.queue.append(line.split(' ')[4])
				elif self.type == 5:
					self.queue.append(line.split(' ')[5])
			self.notallow = False

		elif re.search("found the previous bag", line):			# read duplicate rfid, remove from total bin counts
			self.total_bins -= 1
			self.notallow = True
		elif re.search("Linked internal bag_id", line) and not re.search("__I__", line):
			self.linked_count += 1
			while self.queue[0] != line.split(' ')[7]:		# no need to check empty, bag always appears before this linked cmd
				self.unlinked.append(self.queue.pop(0))
			self.queue.pop(0)

		elif re.search("is unlinked", line) and not re.search("__I__", line):
			if self.type == 2:
				self.zone4.append(line.split(' ')[4])
			elif self.type == 5:
				self.zone4.append(line.split(' ')[5])

	def readInfo(self):
		num, num1, num2, num3, num4, num5, num6, num7, num8, num9, num10 = -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1
		self.dic = { "attenuation_events": 0, "entrance events": 0, "exit events": 0, "cleared": 0, "rejected": 0, "lost_tracking": 0, \
		"unlinked": 0, "entrance_rfid_misreads": 0, "exit_rfid_misreads": 0, "oversize_bags": 0, "cut_bags": 0 }
		with open('bagTotals.txt') as f:
			for line in f:
				line = line.split('BagTotals: ')[1]
				dic_temp = ast.literal_eval(line)

				cur = dic_temp['attenuation_events']
				num = self.getCount(cur, num, 'attenuation_events')

				cure = dic_temp['entrance events']
				num1 = self.getCount(cure, num1, 'entrance events')

				curee = dic_temp['exit events']
				# print(curee)
				num2 = self.getCount(curee, num2, 'exit events')

				curnm = dic_temp['entrance_rfid_misreads']
				num3 = self.getCount(curnm, num3, 'entrance_rfid_misreads')

				curem = dic_temp['exit_rfid_misreads']
				num4 = self.getCount(curem, num4, 'exit_rfid_misreads')

				curul = dic_temp['unlinked']
				num5 = self.getCount(curul, num5, 'unlinked')

				curc = dic_temp['cleared']
				num6 = self.getCount(curc, num6, 'cleared')

				currj = dic_temp['rejected']
				num7 = self.getCount(currj, num7, 'rejected')

				curlt = dic_temp['lost_tracking']
				num8 = self.getCount(curlt, num8, 'lost_tracking')

				curo = dic_temp['oversize_bags']
				num9 = self.getCount(curo, num9, 'oversize_bags')

				curcb = dic_temp['cut_bags']
				num10 = self.getCount(curcb, num10, 'cut_bags')


		if num != 0:
			self.dic['attenuation_events'] += num
			num = 0
		if num1 != 0:
			self.dic['entrance events'] += num1
			num1 = 0
		if num2 != 0:
			self.dic['exit events'] += num2
			num2 = 0
		if num3 != 0:
			self.dic['entrance_rfid_misreads'] += num3
			num3 = 0
		if num4 != 0:
			self.dic['exit_rfid_misreads'] += num4
			num4 = 0
		if num5 != 0:
			self.dic['unlinked'] += num5
			num5 = 0
		if num6 != 0:
			self.dic['cleared'] += num6
			num6 = 0
		if num7 != 0:
			self.dic['rejected'] += num7
			num7 = 0
		if num8 != 0:
			self.dic['lost_tracking'] += num8
			num8 = 0
		if num9 != 0:
			self.dic['oversize_bags'] += num9
			num9 = 0
		if num10 != 0:
			self.dic['cut_bags'] += num10
			num10 = 0
		print("\nBagTotals read:",json.dumps(self.dic,indent=4))

	def getCount(self, cur, num, key):

		if cur >= num:
			num = cur
		else:
			# print("in else",num, "to", key)
			self.dic[key] += num
			num = 0
		return num

if __name__ == '__main__':
	try:
		# filename = sys.argv[1]
		filename = 'C:/Users/wzhong/Documents/temp/logfiles/AnalogicStandaloneType5_20200312.log'
		type = filename.split('_')[0][-1]

		# set check statement for Type2 and Type5
		if int(type) == 2:
			rt = BagTotal(filename, 2)
		elif int(type) == 5:
			rt = BagTotal(filename, 5)
			print(">>.")

	except FileNotFoundError:
		print("Invalid file. Please try again.")

