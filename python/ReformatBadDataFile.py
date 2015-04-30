#!/usr/bin/env python

import sys

fi = open(sys.argv[1], 'r')
fo = open(sys.argv[2], 'w')

fo.write(fi.readline())
fo.write(fi.readline())

for l in fi:
  newl = l[:26] + ' ' + l[26:]
  fo.write(newl)
