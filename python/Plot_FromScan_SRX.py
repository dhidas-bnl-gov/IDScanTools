#!/usr/bin/env python

import sys
from datetime import datetime

import numpy as numpy
import matplotlib.pyplot as plt

f = open(sys.argv[1], 'r')

Labels = f.readline().split()
Labels.pop(0)
print Labels
print f.readline().strip()


X = []
DT = []
Y0 = []
Y1 = []
Y2 = []

StartTime = datetime(2000, 1, 1)

for line in f:
  line.strip()
  V = line.strip().split(' ')
  timestr = V.pop(0) + ' ' + V.pop(0)
  Time = datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S.%f")
  if StartTime == datetime(2000, 1, 1):
    StarTime = Time

  V = map(float, V)
  

  X.append( (Time - StartTime).total_seconds() )
  if len(X) > 1:
    DT.append(X[-1] -X[-2])
  Y0.append( V[1])
  Y1.append( V[2] - V[1]/1e6 )
  Y2.append( V[4] - V[3] )




plt.subplot(311)
plt.plot(X, Y0)
plt.ylabel('GapSet')
plt.xlabel("Time (seconds)")

plt.subplot(312)
plt.plot(X, Y1)
#plt.ylim([-0.0005, 0.0005])
plt.ylabel('GapSet - GapMeasured (mm)')
plt.xlabel("Time (seconds)")

plt.subplot(313)
plt.plot(X, Y2)
plt.ylabel('Taper (mm)')
plt.xlabel("Time (seconds)")



Name = sys.argv[1][:-4] + '_Summary.png'
plt.savefig(Name)


plt.cla()
plt.figure()
plt.hist(Y1)
mean = numpy.mean(Y1)
std  = numpy.std(Y1)
print mean, std
plt.xlabel("Gapset - Measured Gap [mm]")
Name = sys.argv[1][:-4] + '_DaltaGap.png'
plt.savefig(Name)



plt.cla()
plt.figure()
plt.hist(Y2)
mean = numpy.mean(Y2)
std  = numpy.std(Y2)
print mean, std
plt.xlabel("Taper [mm]")
Name = sys.argv[1][:-4] + '_Taper.png'
plt.savefig(Name)



plt.cla()
plt.figure()
plt.hist(DT)
plt.xlabel("Time between moves [s]")
Name = sys.argv[1][:-4] + '_Time.png'
plt.savefig(Name)

