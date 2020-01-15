import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class DataProc:
  def __init__(self, in_window, machine_decision):
    self.in_window = in_window
    self.machine_decision = machine_decision
    self.processLines()

  def processLines(self):
   
    self.df = pd.read_csv(self.in_window)
    self.df['Time'] = pd.to_datetime(self.df['Time'])

    self.df2 = pd.read_csv(self.machine_decision)
    self.df2 = self.df2.drop_duplicates()

    self.dfinal = self.df.merge(self.df2, on="BagID", how='inner')
    
    self.haveRF = pd.notnull(self.dfinal['RFID'])
    self.getDiffHistogram(self.dfinal[self.haveRF])


  def getDiffHistogram(self, df):
    num_bins = len(df) 
    fig = plt.figure()
    n, bins, pathches = plt.hist(df['Beam Diff'], 100, facecolor='blue', alpha=0.5)   # need a fixed '100' here, otherwise too small to see

    plt.xlabel("Attenuation Window")
    plt.ylabel("Frequency")
    plt.title("Bin Tracking Histogram", fontsize=15)

    total = len(self.dfinal.index)
    linked = len(self.dfinal[self.haveRF].index)
    unlinked = total - linked
    percentage = (unlinked/(total)) * 100
    plt.figtext(.52,.75,'Total bins: {0} \nTotal linked bags: {1} \nTotal unlinked bags: {2}\nPercentage of unlinked bags: {3:.2f} %'.format(total, linked, unlinked, percentage),fontsize=9,ha='left')

    fig.savefig('his.png')


# if __name__ == '__main__':
#   fp = DataProc('linked_bags.txt')
