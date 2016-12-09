#!/usr/bin/python3

from statistics import mean,median,stdev
import numpy as np
import matplotlib.pyplot as plot

with open('human.txt', 'r') as inf:
    data = [i.split(',') for i in inf.readlines()]
    humanx = [d[0] for d in data]
    humany = [d[1] for d in data]
    hrandavg = [954 for d in data]
with open('random.txt', 'r') as inf:
    data = [i.split(',') for i in inf.readlines()]
    randomx = [d[0] for d in data]
    randomy = [d[1] for d in data]
    rrandavg = [954 for d in data]

fig = plot.figure()
plot.title('Human Input vs RNG (3 Asteroids)')
ax = fig.add_subplot(111)
ax.set_xlabel('Lines of Training Data')
ax.set_ylabel('Average Score')
#ax.plot(randomx, randomy, 'k', label='Trained by RNG', color='r')
ax.plot(humanx, humany, 'k--', label='Trained by Human', color='b')
ax.plot(humanx, hrandavg, 'k--', label='RNG Player Average', color='r')
ax.set_ylim(0)
# Now add the legend with some customizations.
legend = ax.legend(loc='lower center', shadow=True)

# The frame is matplotlib.patches.Rectangle instance surrounding the legend.
frame = legend.get_frame()
frame.set_facecolor('0.90')

plot.show()

fig = plot.figure()
plot.title('Random Input vs RNG (3 Asteroids)')
ax = fig.add_subplot(111)
ax.set_xlabel('Lines of Training Data')
ax.set_ylabel('Average Score')
ax.plot(randomx, randomy, 'k', label='Trained by RNG', color='b')
ax.plot(randomx, rrandavg, 'k', label='RNG Player Average', color='r')
#ax.plot(humanx, humany, 'k--', label='Trained by Human', color='b')
ax.set_ylim(0)

# Now add the legend with some customizations.
legend = ax.legend(loc='lower center', shadow=True)

# The frame is matplotlib.patches.Rectangle instance surrounding the legend.
frame = legend.get_frame()
frame.set_facecolor('0.90')

plot.show()
