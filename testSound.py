#!/usr/bin/python

import time
from sound import play

threads = []
def pw(s,d=.1):
	threads.append(play(s))
	time.sleep(d)

laz = "lazers/"
base = "base laser+"
a="1.1"
b="4.1"
c="6.2"
w=".wav"
t="trunc"
la = laz+base+a+w
lb = laz+base+b+w
lc = laz+base+c+w
lat = laz+base+a+t+w
lbt = laz+base+b+t+w
lct = laz+base+c+t+w
de=.4
pw(la,de)
pw(lb,de)
pw(lc,de)
pw(lbt,de/2)
pw(lat,de/2)
pw(lat,de/2)
pw(lbt,de/2)
pw(lc,de)
pw(lb,de)

for th in threads:
	th.join()
