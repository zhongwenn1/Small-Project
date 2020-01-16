import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class DataProc:
  def __init__(self, in_window, machine_decision):
    self.in_window = in_window
    self.machine_decision = machine_decision
    self.processLines()

  def processLines(self):
   
    self.df = pd.read_csv(self.in_window)               # dataframe that all bags are in the window
    self.df['Time'] = pd.to_datetime(self.df['Time'])   # convert the 'Time' to datetime

    self.df2 = pd.read_csv(self.machine_decision)       # dataframe that store all machine decision for bags
    
    self.df2 = self.df2.drop_duplicates(keep='last')    # drop duplicate rows, keep the last one
    # print(self.df2, "\n")

    self.df3 = pd.read_csv('beam_diff_logfile.csv')     # dataframe that all bags NOT in the window to link with rfid
    # self.df3 = self.df3.sort_values(by=['Beam Diff'])
    self.df3 = self.df3.drop_duplicates(subset=['BagID'], keep='last')  # drop the duplicates internal bag_id, keep the last one
    # print(self.df3, "\n")

    self.dfinal = self.df.merge(self.df2, on="BagID", how='inner')      # final dataframe that merge machine decision column by selecting BagId
    # print(self.dfinal)

    self.linked = self.dfinal.loc[self.dfinal['Linked'] == 1]       # plot histogram for linked bags only based by beam_diff
    self.cut_oversized = self.dfinal.loc[self.dfinal['Machine Decision'] == 'BAG_NOT_ANALYZED']     # for those bag's are not analyzed (indicate cut/oversize bag)
    
    self.joinInfo()     # fill in blanks with another dataframe which has the needed infomation


    self.range151to200 = self.range151To200(self.dfinal)    # choose the range 151 to 200 from beam_diff (bags might splipping on belt..etc.)

    self.rangem1tom50 = self.rangeM1ToM50(self.dfinal)      # choose the range -1 to -50 from beam_diff (bags might pushed by operator..etc.)

    self.getDiffHistogram(self.linked)      # get histogram for all linked bags

  # filter range out, choose data that beam_diff in range 151 to 200
  def range151To200(self, df):
    return df[(df['Beam Diff'] >= 151) & (df['Beam Diff'] <= 200)]

  # choose data that beam_diff in range -1 to -50
  def rangeM1ToM50(self, df):
    return df[(df['Beam Diff'] <= -1) & (df['Beam Diff'] >= -50)]

  # fill in blanks inside dataframe with another dataframe which has the needed infomation
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


  # get histogram based on the beam_diff (for linked bags, see line 39)
  def getDiffHistogram(self, df):
    num_bins = len(df)      # bins that the histogram will display 
    fig = plt.figure()      # plt as a figure
    n, bins, pathches = plt.hist(df['Beam Diff'], 100, facecolor='blue', alpha=0.5)   # need a fixed '100' here, otherwise too small to see

    plt.xlabel("Attenuation Window")    # xlabel for plot
    plt.ylabel("Frequency")             # ylabel for plot
    plt.title("Bin Tracking Histogram", fontsize=15)    # title 

    total = len(self.dfinal.index)      # total number of scanned bags
    # linked = len(self.dfinal[self.haveRF].index)
    linked = len(self.linked.index)     # total number of linked bags
    unlinked = total - linked           # total number of unlinked bags
    cut_oversized = len(self.cut_oversized.index)   # cut or oversized bags
    co_percentage = (cut_oversized/total) * 100     # cut or oversized percentage
    percentage = (unlinked/(total)) * 100       # percentage for unlinked bags

    rate_range151to200 = len(self.range151to200.index) / total * 100    # percentage for special condition (eg. splipping on belt)
    print("Range from 151 to 200: \n", self.range151to200)
    print(len(self.range151to200.index) / total * 100, "%")

    rate_rangem1tom50 = len(self.rangem1tom50.index) / total * 100      # percentage for special condition (eg. pushed by operator)
    print("Range from -1 to -50: \n", self.rangem1tom50)
    print(len(self.rangem1tom50.index) / total * 100, "%")

    print("linked:", linked, "unlinked:", unlinked, "cut over:", cut_oversized, "total:", total)

    # infomations show in text on histogram
    plt.figtext(.49,.72,'Total bins: {0}\nTotal linked bags: {1}\nTotal unlinked bags: {2}\nPercentage of unlinked bags: {3:.2f} % \nPercentage of cut/oversized bags: {4:.2f} %'.format(total, \
        linked, unlinked, percentage, co_percentage),fontsize=9,ha='left')
    plt.figtext(.49,.65,'Range from 151 to 200: {0:.2f} %\nRange from -1 to -50: {1:.2f} %'.format(rate_range151to200, rate_rangem1tom50),fontsize=9,ha='left')

    fig.savefig('his.png')  # save figure


# if __name__ == '__main__':
#   fp = DataProc('')


    # print(self.df3.loc[self.df3['BagID'] == 55721].index[0], "\n")    # simple test on loc   
    # df.at[0, 'Machine Decision'] = 'fffd'

    # print(self.dfinal.loc[self.dfinal['BagID'] == 56402])

    # print(self.dfinal.loc[self.dfinal['BagID'] == 56403])
    # print(self.dfinal.loc[self.dfinal['BagID'] == 55723])