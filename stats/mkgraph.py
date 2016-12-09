#!/usr/bin/python3

from statistics import mean,median,stdev
import numpy as np
import matplotlib.pyplot as plot

with open('asteroidcount.txt', 'r') as inf:
    data = [i.split(',') for i in inf.readlines()]

x = [d[0] for d in data]
rng = [d[1] for d in data]
classifier = [d[2] for d in data]

fig = plot.figure()
plot.title('Results by Asteroid Count')
plot.xticks([1,2,3,4,5])
ax = fig.add_subplot(111)
ax.set_xlabel('Number of Asteroids')
ax.set_ylabel('Average Score')
ax.plot(x, rng, 'k', label='RNG Player', color='r')
ax.plot(x, classifier, 'k--', label='Random Forest', color='b')
ax.set_ylim(0)

# Now add the legend with some customizations.
legend = ax.legend(loc='upper center', shadow=True)

# The frame is matplotlib.patches.Rectangle instance surrounding the legend.
frame = legend.get_frame()
frame.set_facecolor('0.90')

plot.show()
