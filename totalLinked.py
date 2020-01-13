from dataProc import DataProc
import re

class FileProc:
  def __init__(self, filenames):
    self.filenames = filenames  # assume we have filenames as a list here
    self.linked_bags = []
    self.linked_phrases = "is in the window"
    self.ignore_phrases = "WARNING" # might have some more
    self.unlinked_phrases = "{null}/"
    self.unlinked_bags = set()


  def getLinkedBags(self):
    for infile in self.filenames:
      with open(infile) as f:
        f = f.readlines()
      for line in f:
        if self.linked_phrases in line and self.ignore_phrases not in line:
          self.linked_bags.append(line)     

    return self.linked_bags  


  def getUnlinkedBags(self):
    for infile in self.filenames:
      with open(infile) as f:
        f = f.readlines()
      for line in f:
        if "is NOT in the window" in line:
          self.unlinked_bags.add(line)
    return self.unlinked_bags
    # for infile in self.filenames:
    #   with open(infile) as f:
    #     f = f.readlines()
    #   for line in f:
    #     # obj = re.search(r'(.*){null}(.*?)', line)
    #     if self.unlinked_phrases in line:
    #       self.unlinked_bags.add(line.split("/")[1].split("]")[0])
    # return self.unlinked_bags

  # def checkWithLinkedBags(self):
  #   for bags in self.unlinked_bags:     

  def getLinkedBagsNum(self):
    return len(self.linked_bags)

  def getUnlinkedBagsNum(self):
    return len(self.unlinked_bags)

  def getTotalBags(self):
    return self.getLinkedBagsNum() + self.getUnlinkedBagsNum()
    
if __name__ == '__main__':
  fp = FileProc(["AnalogicStandaloneType2_20190620.log"])
  linked_bag = fp.getLinkedBags()
  # print(linked_bag, fp.getLinkedBagsNum())
  unlinked_bag = fp.getUnlinkedBags()
  # print(unlinked_bag)
  for bag in unlinked_bag:
    print(bag)
  print("Total Bins: ", fp.getTotalBags())
  print("Total Linked Bins: ", fp.getLinkedBagsNum())
  print("Total Unlinked Bins: ", fp.getUnlinkedBagsNum())
  print("Percent of Unlinked Bins: ", fp.getUnlinkedBagsNum() / fp.getTotalBags() * 100, "%")
  # s = ["2019-05-06 11:34:08.892368, INFO, BHS_INTF, Zone[-1]::OnExit: Moving bag [{null}/__I__5917067] into next zone"]
  # for line in s:
  #   if "{null}" in line:
  #     print(line.split("/")[1].split("]")[0])
  # for i in s:
  #   print(re.search(r'(.*){null}/(.*?).*', s, flags=re.I))