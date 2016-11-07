#!/usr/bin/python
import os

for n in range(90/5):
	m=n*5
	os.system("convert -distort SRT %r ufomastershield.png ufoshield%r.png" %(m,m))
