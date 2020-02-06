import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
# from timeMeasure-simulation import TimeMeasure
	
class DataProc:
	def __init__(self):		
		self.processLines()

	def processLines(self):
		self.df = pd.read_csv('in_window_logfile.csv')      # dataframe that all bags are in the window
		self.df['Time'] = pd.to_datetime(self.df['Time'])   # convert the 'Time' to datetime

		self.df2 = pd.read_csv('machine_decision_logfile.csv')  # dataframe that store all machine decision for bags

		self.df2 = self.df2.drop_duplicates(keep='last')    # drop duplicate rows, keep the last one

		self.df3 = pd.read_csv('not_in_window_logfile.csv')     # dataframe that all bags NOT in the window to link with rfid
		# self.df3 = self.df3.sort_values(by=['Beam Diff'])
		self.df3 = self.df3.drop_duplicates(subset=['BagID'], keep='last')  # drop the duplicates internal bag_id, keep the last one

		self.dfinal = self.df.merge(self.df2, on="BagID", how='inner')      # final dataframe that merge machine decision column by selecting BagId

		self.joinInfo()     # fill in blanks with another dataframe which has the needed infomation

		self.linked = self.dfinal.loc[self.dfinal['Linked'] == 1]       # plot histogram for linked bags only based by beam_diff
		self.unlinked = self.dfinal.loc[self.dfinal['Linked'] == 0]

		self.cut_oversized = self.dfinal.loc[self.dfinal['Machine Decision'] == 'BAG_NOT_ANALYZED']     # for those bag's are not analyzed (indicate cut/oversize bag)

		self.range151to200 = self.range151To200(self.dfinal)    # choose the range 151 to 200 from beam_diff (bags might splipping on belt..etc.)

		self.rangem1tom50 = self.rangeM1ToM50(self.dfinal)      # choose the range -1 to -50 from beam_diff (bags might pushed by operator..etc.)

		self.getDiffHistogram(self.linked)      # get histogram for all linked bags
		self.linkedBar(self.dfinal)
		self.unlinkedBar(self.unlinked)

		# sc = TimeMeasure(2)
		# sc.getDuration()
  #   	# density with shade
		# sns.distplot(sc.total_stopped_time, hist = False, kde = True, kde_kws = {'shade': True, 'linewidth': 3}, label = 'actual stop')    
		# sns.distplot(sc.fake_total_stopped_time, hist = False, kde = True, kde_kws = {'shade': True, 'linewidth': 3}, label = 'fake stop')

		# plt.legend(prop={'size': 12})
		# plt.title('request to run VS actual stop')
		# plt.xlabel('timestamp (seconds)')
		# plt.ylabel('Density')
		# plt.savefig('fake stop vs actual stop')
		# plt.close()

		# # density with shade
		# sns.distplot(sc.total_stopped_time, hist = False, kde = True, kde_kws = {'shade': True, 'linewidth': 3}, label = 'before delay')    
		# sns.distplot(sc.total_stopped_after_delay, hist = False, kde = True, kde_kws = {'shade': True, 'linewidth': 3}, label = 'after delay')

		# plt.legend(prop={'size': 12})
		# plt.title('stop time distribution')
		# plt.xlabel('timestamp (seconds)')
		# plt.ylabel('Density')
		# plt.savefig('stop time distribution after delay')
		# plt.show()   

		# print('stopped time before delay:', sum(sc.total_stopped_time), 'Percentage of stopped time before delay / total:', round((sum(sc.total_stopped_time) / sc.total_machine_running * 100),2), "%")
		# print('stopped time after delay:', sum(sc.total_stopped_after_delay), 'Percentage of stopped time after delay / total:', round((sum(sc.total_stopped_after_delay) / sc.total_machine_running * 100),2), "%")
		# print('running time:', sum(sc.total_running_time), 'Percentage of running time / total:', round((sum(sc.total_running_time) / sc.total_machine_running * 100),2), "%")


	def linkedBar(self, df):
		fig = plt.figure()      # plt as a figure
		self.linked[['Beam Diff']].plot(kind='hist',bins=100,facecolor='blue',alpha=0.5)
		plt.title("Linked Bags",fontsize=15)
		plt.xlabel("Attenuation Window")
		plt.savefig('link.png')
		plt.close()

	def unlinkedBar(self, df):
		fig = plt.figure()      # plt as a figure
		self.unlinked[['Beam Diff']].plot(kind='hist',bins=100,facecolor='blue',alpha=0.5)
		plt.title("Unlinked Bags",fontsize=15)
		plt.xlabel("Attenuation Window")
		plt.savefig('unlink.png')
		plt.close()

	def range151To200(self, df):
		return df[(df['Beam Diff'] >= 151) & (df['Beam Diff'] <= 200)]

	def rangeM1ToM50(self, df):
		return df[(df['Beam Diff'] <= -1) & (df['Beam Diff'] >= -50)]

	def joinInfo(self):
		for i, row in self.df3.iterrows():  # iterate through the small dataframe, make the bag_id as the primary key to find the corresponding row
			bagID = row['BagID']    # primary key
			rfID = row['RFID']      # rows need to be updated
			travelDist = row['Travel Distance'] # ready to be updated
			beamDiff = row['Beam Diff'] # same as above
			# print(bagID)
			dfinal_bagID_index = self.dfinal.loc[self.dfinal['BagID'] == bagID].index[0]    # find the corresponding row for particular bag Id
			if self.dfinal.loc[dfinal_bagID_index]['Linked'] == 0:      # if the bag is unlinked (we only update unlinked bag info here)
				self.dfinal.at[dfinal_bagID_index, 'RFID'] = rfID       # fill in the rfID into dataframe
				self.dfinal.at[dfinal_bagID_index, 'Travel Distance'] = travelDist  # fill in the travelDist
				self.dfinal.at[dfinal_bagID_index, 'Beam Diff'] = beamDiff          # fill in the beam_diff

	def getDiffHistogram(self, df):
		num_bins = len(df)      # bins that the histogram will display 
		fig = plt.figure()      # plt as a figure
		# n, bins, pathches = plt.hist(df['Beam Diff'], 100, facecolor='blue', alpha=0.5)   # need a fixed '100' here, otherwise too small to see
		df['Beam Diff'].plot(kind='hist',bins=100,facecolor='blue',alpha=0.5)

		plt.xlabel("Attenuation Window")    # xlabel for plot
		# plt.ylabel("Frequency")             # ylabel for plot
		plt.title("Bin Tracking Histogram", fontsize=15)    # title 

		total = len(self.dfinal.index)      # total number of scanned bags
		# linked = len(self.dfinal[self.haveRF].index)
		linked = len(self.linked.index)     # total number of linked bags
		unlinked = total - linked           # total number of unlinked bags
		cut_oversized = len(self.cut_oversized.index)   # cut or oversized bags
		co_percentage = (cut_oversized/total) * 100     # cut or oversized percentage
		percentage = (unlinked/(total)) * 100       # percentage for unlinked bags

		rate_range151to200_total = len(self.range151to200.index) / total * 100    # percentage for special condition (eg. splipping on belt)
		rate_range151to200_unlinked = len(self.range151to200.index) / unlinked * 100
		# print("Range from 151 to 200: \n", self.range151to200)
		# print(len(self.range151to200.index) / total * 100, "%")
		# print(len(self.range151to200.index) / unlinked * 100, "%")

		rate_rangem1tom50_total = len(self.rangem1tom50.index) / total * 100      # percentage for special condition (eg. pushed by operator)
		rate_rangem1tom50_unlinked = len(self.rangem1tom50.index) / unlinked * 100
		# print("Range from -1 to -50: \n", self.rangem1tom50)
		# print(len(self.rangem1tom50.index) / total * 100, "%")
		# print(len(self.rangem1tom50.index) / unlinked * 100, "%")

		# print("linked:", linked, "unlinked:", unlinked, "cut over:", cut_oversized, "total:", total)

		# infomations show in text on histogram
		plt.figtext(.49,.72,'Total bins: {0}\nTotal linked bags: {1}\nTotal unlinked bags: {2}\nPercentage of unlinked bags: {3:.2f} % \nPercentage of cut/oversized bags: {4:.2f} %'.format(total, \
		    linked, unlinked, percentage, co_percentage),fontsize=9,ha='left')
		plt.figtext(.49,.66,'Slipping bags (151 to 200) / total: {0:.2f} % \nSlipping bag / unlinked: {1:.2f} %'.format(rate_range151to200_total, rate_range151to200_unlinked),fontsize=9,ha='left')
		plt.figtext(.49,.60,'Pushed bags (-1 to -50) / total: {0:.2f} % \nPushed bag / unlinked: {1:.2f} %'.format(rate_rangem1tom50_total, rate_rangem1tom50_unlinked),fontsize=9,ha='left')
		# plt.figtext(.49,.54,'Loose bags / total: {0:.2f} % \nLoose bags / unlinked: {1:.2f} %'.format(rate_loosebag_total, rate_loosebag_unlinked),fontsize=9,ha='left')

		fig.savefig('his.png')  # save figure
		# plt.show()
		plt.close()     # avoid show multiple graphs		
		
# if __name__ == '__main__':
# 	dp = DataProc()