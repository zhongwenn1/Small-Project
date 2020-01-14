from dataProc import DataProc

class FileProc:
  def __init__(self, filenames):
    self.filenames = filenames  # assume we have filenames as a list here
    self.linked_bags = []
    self.linked_phrases = "is in the window"
    self.ignore_phrases = "WARNING" # might have some more
    self.unlinked_bags = []

    # self.getLinkedBags()

  def getLinkedBags(self):
    for infile in self.filenames:
      with open(infile) as f:
        f = f.readlines()
      for line in f:
        if self.linked_phrases in line and self.ignore_phrases not in line:
          self.linked_bags.append(line)
          # maybe direct to DataProc to take care of data, avoid multiple iterate          

    return self.linked_bags  # just for test here, will change later

  def getUnlinkedBags(self):
    for infile in self.filenames:
      with open(infile) as f:
        f = f.readlines()
      for line in f:
        if "No bag is in the window" in line:
          self.unlinked_bags.append(line)
    return self.unlinked_bags

  def getLinkedBagsNum(self):
    return len(self.linked_bags)

  def getUnlinkedBagsNum(self):
    return len(self.unlinked_bags)

  def getTotalBags(self):
    return self.getLinkedBagsNum() + self.getUnlinkedBagsNum()

# if __name__ == '__main__':
#   fp = FileProc(['AnalogicStandaloneType2_20190506.log', 'AnalogicStandaloneType2_20190506.log'])
#   print(fp.getLinkedBags(), fp.getLinkedBagsNum())

# infile = r"AnalogicStandaloneType2_20190506.log"

# linked_bags = []
# keep_phrases = ["is in the window"]
# ignore_phrases = "WARNING"
# with open(infile) as f:
#   f = f.readlines()
# for line in f:
#   for phrase in keep_phrases:
#     if phrase in line and ignore_phrases not in line:
#       linked_bags.append(line)
#       break
# print(linked_bags, len(linked_bags))