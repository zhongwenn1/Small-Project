import pandas as pd
from preProc import PreProc
import config as cfg
import os
	
class DataProc(PreProc):
	def __init__(self, preProc):
		self.df = None
		self.df2 = None
		self.df3 = None
		self.dfinal = None
		self.linked = None
		self.unlinked = None
		self.cut_oversized = None
		self.slipping = None
		self.pushed = None
		self.unlinked_RFID = None
		self.preProc = preProc
		self.unlinked_list = None
		self.load_files()

	def load_files(self):
		try:
			cur_path = os.getcwd()
			self.df = pd.read_csv(os.path.join(cur_path, 'output', cfg.files['inWindow']))      # dataframe that all bags are in the window
			self.df['Time'] = pd.to_datetime(self.df['Time'])   # convert the 'Time' to datetime
			self.df2 = pd.read_csv(os.path.join(cur_path, 'output', cfg.files['machineDec']))  # dataframe that store all machine decision for bags

			self.df2 = self.df2.drop_duplicates(keep='last')    # drop duplicate rows, keep the last one
			self.df3 = pd.read_csv(os.path.join(cur_path, 'output', cfg.files['notInWindow']))     # dataframe that all bags NOT in the window to link with rfid
			self.df3 = self.df3.drop_duplicates(subset=['BagID'], keep='last')  # drop the duplicates internal bag_id, keep the last one
			self.dfinal = self.df.merge(self.df2, on="BagID", how='inner')      # final dataframe that merge machine decision column by selecting BagId

			self.join_info()     # fill in blanks with another dataframe which has the needed infomation

			self.linked = self.dfinal.loc[self.dfinal['Linked'] == 1]
			self.unlinked = self.dfinal.loc[self.dfinal['Linked'] == 0]		# unlinked internal bag

			self.unlinked_info()

			self.cut_oversized = self.dfinal.loc[self.dfinal['Machine Decision'] == 'BAG_NOT_ANALYZED']     # for those bag's are not analyzed (indicate cut/oversize bag)

		except FileNotFoundError:
			print("Did not find file")
			
	def get_df(self, df, lower, upper):
		return df[(df['Beam Diff'] >= lower) & (df['Beam Diff'] <= upper)]

	def join_info(self):
		if len(self.dfinal.index) != 0:
			for i, row in self.df3.iterrows():  	# iterate through the small dataframe, make the bag_id as the primary key to find the corresponding row
				bagID = row['BagID']    			# primary key
				rfID = row['RFID']      			# rows need to be updated
				travelDist = row['Travel Distance'] # ready to be updated
				beamDiff = row['Beam Diff'] 		# same as above
				dfinal_bagID_index = self.dfinal.loc[self.dfinal['BagID'] == bagID].index[0]    # find the corresponding row for particular bag Id
				if self.dfinal.loc[dfinal_bagID_index]['Linked'] == 0:      					# if the bag is unlinked (we only update unlinked bag info here)
					self.dfinal.at[dfinal_bagID_index, 'RFID'] = rfID       					# fill in the rfID into dataframe
					self.dfinal.at[dfinal_bagID_index, 'Travel Distance'] = travelDist  		# fill in the travelDist
					self.dfinal.at[dfinal_bagID_index, 'Beam Diff'] = beamDiff          		# fill in the beam_diff

	def unlinked_info(self):
		"""
		compare with unlinked dataframe(self.unlinked) with actual unlinked bins(self.unlinked_list)
		extract real unlinked bins information rows into new dataframe
		note: unlinked dataframe may contain info for linked bins, that's why we need to double check with actual unlinked bins
		"""
		c = 0
		self.unlinked_list = self.preProc.unlinked_list
		self.unlinked_RFID = pd.DataFrame(columns=['Time', 'RFID', 'BagID', 'Travel Distance', 'Beam Diff', 'Linked', 'Machine Decision'])
		for i, row in self.unlinked.iterrows():
			rfID = row['RFID']
			if self.unlinked_list and rfID in self.unlinked_list:
				while self.unlinked_list[0] != rfID:
					self.unlinked_list.append(self.unlinked_list.pop(0))
				self.unlinked_list.pop(0)
				self.unlinked_RFID.loc[c] = row
				c += 1