from datetime import datetime

class BagInfo:
	def __init__(self, filename):
		self.fname = filename
		# self.getTime()


	def getDatetime(self, time):
		date_time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
		return datetime.timestamp(date_time)

	def getTime(self):
		timelst = []
		Start = False
		start, end = 0, 0
		with open(self.fname) as f:
			for line in f:
				if Start and "BAG_END" in line:
					end = self.getDatetime(line.split(',')[0])
					timelst.append(end - start)
					Start = False
				elif "BAG_START" in line:
					start = self.getDatetime(line.split(',')[0])
					Start = True
		# print(timelst, len(timelst))


	def getCount(self):
		dic = {}
		with open('bagUpdate.txt') as f:
			for line in f:
				# print(line.split('\n')[0])
				line = line.split('\n')[0]
				if line in dic:
					# print("fdsfsdfsfdagasf")
					dic[line] += 1
				else:
					dic[line] = 1
		print(dic, len(dic))
		for i, k in dic.items():
			if k != 2:
				print(i)

if __name__ == '__main__':
	b = BagInfo('bag_info.txt')
	b.getCount()