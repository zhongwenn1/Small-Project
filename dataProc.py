import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class DataProc:
  def __init__(self, lines, unlinked_bags):
    self.unlinked_bags = unlinked_bags
    self.lines = lines
    self.file_tag_lst = []
    self.time_lst = []
    self.RFID_lst = []
    self.bagID_lst = []
    self.beam_diff_lst = []
    self.dist_lst = []
    self.processLines()

  def processLines(self):
    # single file (example .txt)
    # try:
    #   fp = open(self.lines, 'r').read()
    #   if fp:
        # get file content
    self.getLineContent()
   
    dic = {'Time':self.time_lst, 'RFID':self.RFID_lst, 'BagID':self.bagID_lst, 'Dist':self.dist_lst, 'Diff':self.beam_diff_lst}
    df = pd.DataFrame(dic)
    df['Time'] = pd.to_datetime(df['Time'])
    
    self.getDiffHistogram(df)
    
    # except IOError:
    #   print("Catch Error, please try again.")

  def getLineContent(self):

    for line in self.lines:
      # starts here, line goes below
      line = line.split(",")

      self.time_lst.append(self.getTime(line[0])) 
      self.RFID_lst.append(self.getRFID(line[3]))
      self.bagID_lst.append(self.getBagID(line[3]))
      self.dist_lst.append(self.getDist(line[5]))       
      self.beam_diff_lst.append(self.getDiffNum(line[6]))        


  def getDiffHistogram(self, df):
    num_bins = len(df) 
    # fig, ax = plt.subplots()
    # ax.plot("fdsfsfsd")
    fig = plt.figure()
    # fig = plt.figure(figsize=(6.4, 4.8), dpi=1000)
    n, bins, pathches = plt.hist(df['Diff'], 100, facecolor='blue', alpha=0.5)   # need a fixed '100' here, otherwise too small to see
    plt.xlabel("Attenuation Window")
    plt.ylabel("Frequency")
    plt.title("Bin Tracking Histogram", fontsize=15)
    total = len(self.lines)+len(self.unlinked_bags)
    linked = len(self.lines)
    unlinked = len(self.unlinked_bags)
    percentage = ((len(self.unlinked_bags)/(len(self.lines)+len(self.unlinked_bags))) * 100)
    plt.figtext(.52,.75,'Total bins: {0} \nTotal linked bags: {1} \nTotal unlinked bags: {2}\nPercentage of unlinked bags: {3:.2f} %'.format(total, linked, unlinked, percentage),fontsize=9,ha='left')
    # plt.title('Total bins: {0} \nTotal linked bags: {1} \nTotal unlinked bags: {2}\nPercentage of unlinked bags: {3:.2f} %'.format(total, linked, unlinked, percentage))
    print('Total bins: {0} \nTotal linked bags: {1} \nTotal unlinked bags: {2}\nPercentage of unlinked bags: {3:.2f} %'.format(total, linked, unlinked, percentage))
    # plt.show()
    # plt.legend("Linked bags: ")
    fig.savefig('his.png')

  def getFileTag(self, filetag):
      return filetag[:filetag.index(":")]
      
  def getTime(self, time):
      return time

  def getRFID(self, bag_info):
      return bag_info.split("[")[1].split("]")[0]

  def getBagID(self, bag_info):
      return bag_info.split("[")[2].split("]")[0]

  def getDist(self, dist):
    return float(dist.split(":")[1])

  def getDiffNum(self, beam_diff):
    return float(beam_diff.split(":")[1].split(" ")[1])

# if __name__ == '__main__':
#   fp = DataProc('linked_bags.txt')
