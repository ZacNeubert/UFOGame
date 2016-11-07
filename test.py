#!/usr/bin/python

from numpy import matrix

m = matrix([[1, 2], [3, 4]])
print m
m[1,1] = 5
print m[1,0]

