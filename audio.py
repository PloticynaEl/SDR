import os

devices = os.popen("arecord -l")
device_string = devices.read()
device_string = device_string.split("\n")
for i in range(1,len(device_string),3):
 print(device_string[i])

for line in device_string:
 if(line.find("card") != -1):
  print("hw:" + line[line.find("card")+5] + "," + line[line.find("device")+7])
 if(line.find("карта") != -1):
  print("hw:" + line[line.find("карта")+6] + "," + line[line.find("устройство")+11])



