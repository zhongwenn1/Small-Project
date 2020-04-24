import pandas as pd
from datetime import datetime
	
class DataProc:
	def __init__(self):		
		self.processLines()

	def processLines(self):
		try:
			self.df = pd.read_csv('in_window_logfile.csv')      # dataframe that all bags are in the window
			self.df['Time'] = pd.to_datetime(self.df['Time'])   # convert the 'Time' to datetime
			self.df2 = pd.read_csv('machine_decision_logfile.csv')  # dataframe that store all machine decision for bags

			self.df2 = self.df2.drop_duplicates(keep='last')    # drop duplicate rows, keep the last one
			self.df3 = pd.read_csv('not_in_window_logfile.csv')     # dataframe that all bags NOT in the window to link with rfid
			self.df3 = self.df3.drop_duplicates(subset=['BagID'], keep='last')  # drop the duplicates internal bag_id, keep the last one
			self.dfinal = self.df.merge(self.df2, on="BagID", how='inner')      # final dataframe that merge machine decision column by selecting BagId

			self.joinInfo()     # fill in blanks with another dataframe which has the needed infomation

			self.linked = self.dfinal.loc[self.dfinal['Linked'] == 1]       # plot histogram for linked bags only based on beam_diff
			self.unlinked = self.dfinal.loc[self.dfinal['Linked'] == 0]

			self.cut_oversized = self.dfinal.loc[self.dfinal['Machine Decision'] == 'BAG_NOT_ANALYZED']     # for those bag's are not analyzed (indicate cut/oversize bag)

			self.slipping = self.range151To200(self.unlinked)    # choose the range 151 to 200 from beam_diff (bags might slipping on belt..etc.)

			self.pushed = self.rangeM1ToM50(self.unlinked)      # choose the range -1 to -50 from beam_diff (bags might pushed by operator..etc.)
		except FileNotFoundError:
			print("Did not find file")
			
	def range151To200(self, df):
		return df[(df['Beam Diff'] >= 151) & (df['Beam Diff'] <= 200)]

	def rangeM1ToM50(self, df):
		return df[(df['Beam Diff'] <= -1) & (df['Beam Diff'] >= -50)]

	def getDatetime(self, time):
		date_time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
		return datetime.timestamp(date_time)


	def joinInfo(self):
		if len(self.dfinal.index) != 0:
			for i, row in self.df3.iterrows():  # iterate through the small dataframe, make the bag_id as the primary key to find the corresponding row
				bagID = row['BagID']    # primary key
				rfID = row['RFID']      # rows need to be updated
				travelDist = row['Travel Distance'] # ready to be updated
				beamDiff = row['Beam Diff'] # same as above
				dfinal_bagID_index = self.dfinal.loc[self.dfinal['BagID'] == bagID].index[0]    # find the corresponding row for particular bag Id
				if self.dfinal.loc[dfinal_bagID_index]['Linked'] == 0:      # if the bag is unlinked (we only update unlinked bag info here)
					self.dfinal.at[dfinal_bagID_index, 'RFID'] = rfID       # fill in the rfID into dataframe
					self.dfinal.at[dfinal_bagID_index, 'Travel Distance'] = travelDist  # fill in the travelDist
					self.dfinal.at[dfinal_bagID_index, 'Beam Diff'] = beamDiff          # fill in the beam_diff
