#!/usr/bin/env python

import sys
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt

f = open(sys.argv[1], 'r')

Labels = f.readline().split()
Labels.pop(0)
print Labels
print f.readline().strip()


X = []
Y0 = []
Y1 = []
Y2 = []

StartTime = datetime(2000, 1, 1)

for line in f:
  line.strip()
  V = line.strip().split(' ')
  timestr = V.pop(0) + ' ' + V.pop(0)
  print timestr, V
  Time = datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S.%f")
  if StartTime == datetime(2000, 1, 1):
    StarTime = Time

  V = map(float, V)
  print V

  X.append( (Time - StartTime).total_seconds() )
  Y0.append( V[0])
  Y1.append( V[1] - V[0] )
  Y2.append( V[3] - V[2] )

  if len(X) > 20:
    break



plt.subplot(311)
plt.plot(X, Y0)
plt.ylabel('GapSet')
plt.xlabel("Time (seconds)")

plt.subplot(312)
plt.plot(X, Y1)
plt.ylim([-0.0005, 0.0005])
plt.ylabel('GapSet - GapMeasured (mm)')
plt.xlabel("Time (seconds)")

plt.subplot(313)
plt.plot(X, Y2)
plt.ylabel('Taper (mm)')
plt.xlabel("Time (seconds)")

plt.show()
