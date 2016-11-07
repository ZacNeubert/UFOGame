#!/usr/bin/python

import os

for n in range(360/5):
	m = n*5
	os.system("convert -distort SRT -%r blackmaster.png black%r.png" % (m, m))
