import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def getFileContent(file_name):
  lines, data = [], []
  beam_diff_lst, dist_lst, RFID_lst, bagID_lst, time_lst, file_tag_lst = [], [], [], [], [], []
  with open(file_name) as fp:
    line = fp.readline()
    while line:
      line = line.split(",")
      if line[0][0] == 'A': # check if starts with time
          file_tag_lst.append(getFileTag(line[0]))
          time_lst.append(line[0][line[0].index(":")+1:])
      else:
          time_lst.append(getTime(line[0])) 
      RFID_lst.append(getRFID(line[3]))
      bagID_lst.append(getBagID(line[3]))
      dist_lst.append(getDist(line[5]))       
      beam_diff_lst.append(getDiffNum(line[6]))        
      #data.append(line)
      line = fp.readline()
  return lines, data, file_tag_lst, time_lst, RFID_lst, bagID_lst, beam_diff_lst, dist_lst

def getFileTag(filetag):
    return filetag[:filetag.index(":")]
    
def getTime(time):
    return time

def getRFID(bag_info):
    return bag_info.split("[")[1].split("]")[0]

def getBagID(bag_info):
    return bag_info.split("[")[2].split("]")[0]

def getDist(dist):
  return float(dist.split(":")[1])

def getDiffNum(beam_diff):
  return float(beam_diff.split(":")[1].split(" ")[1])

def getDiffBarChart(df):
    num_bins = len(df) 
    n, bins, pathches = plt.hist(df['Diff'], num_bins, facecolor='blue', alpha=0.5)
#    df['Diff'].value_counts().plot('bar')
    plt.xlabel("Beam Diff")
    plt.ylabel("Number of appearance")
    plt.show()
    
def getHistogram(lst):
  num_bins = 10 
  n, bins, pathches = plt.hist(lst, num_bins, facecolor='blue', alpha=0.5)
  #plt.bar(range(num_bins), lst)
  plt.show()
  
def getUnacceptedID(data, val):
  out = []
  for i in data:
    diff = getDiffNum(i[6])
    if diff > val:
      out.append((diff, i[3]))
  return out

#fname = '/home/wzhong/linked_bags2.txt'
while True:
  print ("Enter the file name: ('q' to quit)")
  fname = input()
  if fname == 'q':
    break
  try:
    fp = open(fname, 'r').read()
    if fp:
      lines, data, file_tag_lst, time_lst, RFID_lst, bagID_lst, beam_diff_lst, dist_lst = getFileContent(fname)
      if len(file_tag_lst) != 0:
          dic = {'File': file_tag_lst, 'Time':time_lst, 'RFID':RFID_lst, 'BagID':bagID_lst, 'Dist':dist_lst, 'Diff':beam_diff_lst}
      else:
          dic = {'Time':time_lst, 'RFID':RFID_lst, 'BagID':bagID_lst, 'Dist':dist_lst, 'Diff':beam_diff_lst}
      df = pd.DataFrame(dic)
      df['Time'] = pd.to_datetime(df['Time'])
      print (df)
      print (df.info())
      getDiffBarChart(df)
      
      #getHistogram(lines)
      break
  except IOError:
    print ("No such file, please try again.")
"""
lines, data = getFileContent(fname)
getHistogram(lines)
IDinfo =  getUnacceptedID(data, 90)
print IDinfo, len(IDinfo)
"""
