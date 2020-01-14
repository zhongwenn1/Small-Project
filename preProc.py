import re

count = 0
with open("AnalogicStandaloneType2_20190623.log") as origin_file:
    for line in origin_file:
        # (?# line = re.findall(r'should have reached attenuation', line))
        # if line:
        #    line = line[0].split('')[1]
           # line = line
        if 'should have reached attenuation' in line:
          count += 1
          print (line)
print(count)