import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class FileProc:
  def __init__(self, filenames):
    self.filenames = filenames
    self.processFile()

  def processFile(self):
    # single file (example .txt)
    try:
      fp = open(self.filenames, 'r').read()
      if fp:
        lines, data, file_tag_lst, time_lst, RFID_lst, bagID_lst, beam_diff_lst, \
        dist_lst = self.getFileContent(self.filenames)
        if len(file_tag_lst) != 0:
          dic = {'File': file_tag_lst, 'Time':time_lst, 'RFID':RFID_lst, 'BagID':bagID_lst, 'Dist':dist_lst, 'Diff':beam_diff_lst}
        else:
          dic = {'Time':time_lst, 'RFID':RFID_lst, 'BagID':bagID_lst, 'Dist':dist_lst, 'Diff':beam_diff_lst}
       
        df = pd.DataFrame(dic)
        df['Time'] = pd.to_datetime(df['Time'])
        
        num_bins = len(df) 
        fig = plt.figure()
        n, bins, pathches = plt.hist(df['Diff'], num_bins, facecolor='blue', alpha=0.5)   
        plt.xlabel("Attenuation Window")
        plt.ylabel("Frequency")
        # plt.show()
        fig.savefig('his.png')
    
    except IOError:
      print("Catch Error, please try again.")

  def getFileContent(self, file_name):
    lines, data = [], []
    beam_diff_lst, dist_lst, RFID_lst, bagID_lst, time_lst, file_tag_lst = [], [], [], [], [], []
    with open(file_name) as fp:
      line = fp.readline()
      while line:
        line = line.split(",")
        if line[0][0] == 'A': # check if starts with time
            file_tag_lst.append(self.getFileTag(line[0]))
            time_lst.append(line[0][line[0].index(":")+1:])
        else:
            time_lst.append(self.getTime(line[0])) 
        RFID_lst.append(self.getRFID(line[3]))
        bagID_lst.append(self.getBagID(line[3]))
        dist_lst.append(self.getDist(line[5]))       
        beam_diff_lst.append(self.getDiffNum(line[6]))        
        line = fp.readline()
    return lines, data, file_tag_lst, time_lst, RFID_lst, bagID_lst, beam_diff_lst, dist_lst  

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
#   fp = FileProc('linked_bags.txt')
