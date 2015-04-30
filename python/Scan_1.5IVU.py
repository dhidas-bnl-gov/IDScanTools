#!/usr/bin/env python

import time
from datetime import datetime

# Library version specification required for dls libraries
from pkg_resources import require
require('cothread')

import cothread
from cothread.catools import *


Device = 'SR:C5-ID:G1{IVU21:1-'


Closed    =    6.510
Open      =    7.010
StepSize  =    0.001 
Speed     =  0.2     # in mm/s
SleepTime =  1.1     # Time to wait between moves (in seconds)
SleepBetweenCycles = 10

# Open file for writing data
DTNow = datetime.now().strftime('%Y%m%d.%H%M%S')
OutFileName = 'ScanTest_1.5IVU_' + DTNow + '.dat'
fout = open(OutFileName, 'w')

PV_GapSet      = Device + 'Mtr:2}Pos'
PV_GapSetPos   = Device + 'Mtr:2}Inp:Pos'
PV_GapGO       = Device + 'Mtr:2}Sw:Go'
PV_GapEncoder  = Device + 'LEnc}Gap'
PV_Ready       = Device + 'MtrC}Ready'
PV_GapUS       = Device + 'LEnc}Gap:US'
PV_GapDS       = Device + 'LEnc}Gap:DS'
PV_GapSpeed    = Device + 'Mtr:1}S'
PV_TaperError  = Device + 'MtrC}TaperErr'
PV_CorrFunc    = Device + 'MtrC}AdjSta:RB'
PV_EnableCorr  = Device + 'MtrC}EnaAdj:out'
PV_DisableCorr = Device + 'MtrC}DisAdj:out'



# Values to caget and write to data file after move complete
PV_ValuesToRecord = [PV_GapSetPos, PV_GapSet, PV_GapEncoder, PV_GapUS, PV_GapDS, PV_Ready, PV_GapSpeed, PV_CorrFunc]

# Record field names on first line of file
fout.write( '# Time(s) ' + ' '.join( map(str, PV_ValuesToRecord) ) + '\n')

# Record variables of the scan
fout.write( '# StepSize: ' + str(StepSize)
          + ' Speed: ' + str(Speed)
          + ' Open: ' + str(Open)
          + ' Closed: ' + str(Closed)
          + ' SleepTime: ' + str(SleepTime)
          + ' SleepBetweenCycles: ' + str(SleepBetweenCycles)
          + ' CorrectionFunction(0=enabled): ' + str(caget(PV_CorrFunc))
          )

Comment = raw_input('Enter a comment here: ')
fout.write( '# Comment: ' + Comment)




# Start with the gap closed
caput(PV_GapSpeed, Speed, wait=True)

ThisGap = Closed


iCycle = 0

#caput(PV_DisableCorr, 1, wait=True)

while True:
  iCycle += 1

  print datetime.now(), 'Closing gap'
  caput(PV_EnableCorr, 1, wait=True)
  ThisGap = Closed
  caput(PV_GapSetPos, ThisGap, wait=True, timeout=600)
  caput(PV_GapGO, 1, wait=True, timeout=600)
  #caput(PV_DisableCorr, 1, wait=True)
  while caget(PV_Ready) != 0:
    time.sleep(0.2)
  print datetime.now(), 'Done closing gap'
  time.sleep(SleepTime)



  while ThisGap < Open:
    ThisGap += StepSize
    print ThisGap
    caput(PV_GapSetPos, ThisGap, wait=True, timeout=100)
    caput(PV_GapGO, 1, wait=True, timeout=600)
    while caget(PV_Ready) != 0:
      time.sleep(0.2)
    time.sleep(SleepTime)

    MyOut =  str(str(datetime.now()) + ' ' + ' '.join( map(str, caget(PV_ValuesToRecord))))
    print MyOut
    fout.write(MyOut + '\n')

    TaperErrorFlags = caget(PV_TaperError)
    if TaperErrorFlags != 0:
      fout.write('TaperError: ' + str(TaperErrorFlags))
      exit(1)

  while ThisGap > Closed:
    ThisGap -= StepSize
    caput(PV_GapSetPos, ThisGap, wait=True, timeout=100)
    caput(PV_GapGO, 1, wait=True, timeout=600)
    while caget(PV_Ready) != 0:
      time.sleep(0.2)
    time.sleep(SleepTime)

    MyOut =  str(str(datetime.now()) + ' ' + ' '.join( map(str, caget(PV_ValuesToRecord))))
    print MyOut
    fout.write(MyOut + '\n')

    TaperErrorFlags = caget(PV_TaperError)
    if TaperErrorFlags != 0:
      fout.write('TaperError: ' + str(TaperErrorFlags))
      exit(1)

  print 'Done with cycle', iCycle
  print 'Resting', SleepBetweenCycles, 'seconds'
  time.sleep(SleepBetweenCycles)



  print datetime.now(), 'Opening gap'
  caput(PV_EnableCorr, 1, wait=True)
  ThisGap = Open
  caput(PV_GapSetPos, ThisGap, wait=True, timeout=600)
  caput(PV_GapGO, 1, wait=True, timeout=600)
  #caput(PV_DisableCorr, 1, wait=True)
  while caget(PV_Ready) != 0:
    time.sleep(0.2)
  print datetime.now(), 'Done opening gap'
  time.sleep(SleepTime)


  while ThisGap > Closed:
    ThisGap -= StepSize
    caput(PV_GapSetPos, ThisGap, wait=True, timeout=100)
    caput(PV_GapGO, 1, wait=True, timeout=600)
    while caget(PV_Ready) != 0:
      time.sleep(0.2)
    time.sleep(SleepTime)

    MyOut =  str(str(datetime.now()) + ' ' + ' '.join( map(str, caget(PV_ValuesToRecord))))
    print MyOut
    fout.write(MyOut + '\n')

    TaperErrorFlags = caget(PV_TaperError)
    if TaperErrorFlags != 0:
      fout.write('TaperError: ' + str(TaperErrorFlags))
      exit(1)


  while ThisGap < Open:
    ThisGap += StepSize
    caput(PV_GapSetPos, ThisGap, wait=True, timeout=100)
    caput(PV_GapGO, 1, wait=True, timeout=600)
    while caget(PV_Ready) != 0:
      time.sleep(0.2)
    time.sleep(SleepTime)

    MyOut =  str(str(datetime.now()) + ' ' + ' '.join( map(str, caget(PV_ValuesToRecord))))
    print MyOut
    fout.write(MyOut + '\n')

    TaperErrorFlags = caget(PV_TaperError)
    if TaperErrorFlags != 0:
      fout.write('TaperError: ' + str(TaperErrorFlags))
      exit(1)

  print 'Done with cycle', iCycle
  print 'Resting', SleepBetweenCycles, 'seconds'
  time.sleep(SleepBetweenCycles)





