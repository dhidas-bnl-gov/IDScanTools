#!/usr/bin/env python

import time
from datetime import datetime

# Library version specification required for dls libraries
from pkg_resources import require
require('cothread')

import cothread
from cothread.catools import *


Device = 'SR:C21-ID:G1A{EPU:1-'


Closed    =  26000
Open      =  27000
StepSize  =    100
Speed     =  0.3     # in mm/s
SleepTime =  2.0     # Time to wait between moves (in seconds)

# Open file for writing data
DTNow = datetime.now().strftime('%Y%m%d.%H%M%S')
OutFileName = 'ScanTest_ESMEPU_' + DTNow + '.dat'
fout = open(OutFileName, 'w')

PV_GapSet      = Device + 'Ax:Gap}S-SP'
PV_Gap         = Device + 'LEnc}Gap'
PV_GapUS       = Device + 'LEnc}Gap:US'
PV_GapDS       = Device + 'LEnc}Gap:DS'



# Values to caget and write to data file after move complete
PV_ValuesToRecord = [PV_GapSetPos, PV_GapSet, PV_Gap, PV_GapUS, PV_GapDS, PV_GapSpeed]

# Record field names on first line of file
fout.write( '# Time(s) ' + ' '.join( map(str, PV_ValuesToRecord) ) + '\n')

# Record variables of the scan
fout.write( '# StepSize: ' + str(StepSize)
          + ' Speed: ' + str(Speed)
          + ' Open: ' + str(Open)
          + ' Closed: ' + str(Closed)
          + ' SleepTime: ' + str(SleepTime)
          + ' SleepBetweenCycles: ' + str(SleepBetweenCycles)
          )

Comment = raw_input('Enter a comment here: ')
fout.write( '# Comment: ' + Comment)




# Start with the gap closed
caput(PV_GapSpeed, Speed, wait=True)

ThisGap = Closed


iCycle = 0


while True:

  if ThisGap >= OpenGap:
    ThisGap -= StepSize
  else:
    ThisGap += StepSize

  caput(PV_GapSetPos, ThisGap, wait=True, timeout=600)
  while abs(caget(PV_Gap) - ThisGap) > 0.010:
    time.sleep(1)
  time.sleep(1)
  time.sleep(SleepTime)

  MyOut =  str(str(datetime.now()) + ' ' + ' '.join( map(str, caget(PV_ValuesToRecord))))
  print MyOut
  fout.write(MyOut + '\n')



