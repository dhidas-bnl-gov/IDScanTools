#!/usr/bin/env python

import sys
from datetime import datetime
import numpy
from array import *

from ROOT import TCanvas, TH1F, TGraph

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
  Time = datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S.%f")
  if StartTime == datetime(2000, 1, 1):
    StarTime = Time

  V = map(float, V)
  

  X.append( (Time - StartTime).total_seconds() )
  Y0.append( V[1])
  Y1.append( V[2] - V[1]/1e6 )
  Y2.append( V[4] - V[3] )



c1 = TCanvas()
c1.Divide(1, 3)

c1.cd(1)
g1 = TGraph( len(X), array('d', X), array('d', Y0))
g1.SetTitle('GapSet')
g1.GetXaxis().SetTitle('Time [s]')
g1.GetYaxis().SetTitle('GapSet')
g1.Draw("Al")

c1.cd(2)
g2 = TGraph( len(X), array('d', X), array('d', Y1))
g2.SetTitle('GapSet - Gap Measured')
g2.GetXaxis().SetTitle('Time [s]')
g2.GetYaxis().SetTitle('GapSet - Measured Gap [mm]')
g2.Draw("Al")

c1.cd(3)
g3 = TGraph( len(X), array('d', X), array('d', Y2))
g3.SetTitle('Taper')
g3.GetXaxis().SetTitle('Time [s]')
g3.GetYaxis().SetTitle('Taper [mm]')
g3.Draw("Al")

c1.SaveAs("test.pdf")



hGapDiff = TH1F('GapDiff', 'GapSet - Gap Measured', 50, -0.002, 0.002)
hGapDiff.GetXaxis().SetTitle('GapSet - Gap Measured [mm]')
for y in Y2:
  hGapDiff.Fill(y)

c2 = TCanvas()
c2.cd()
hGapDiff.Draw('hist')
c2.SaveAs('test2.pdf')
exit(0)


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
