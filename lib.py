#!/usr/bin/python

import numpy as np
import math

def rotate(matrix, radians):
	rotator = np.matrix('%r %r ; %r %r' % (math.cos(radians), -math.sin(radians), math.sin(radians), math.cos(radians)))
	return rotator*matrix

def update(matrix):
	updator = np.matrix('1 0 0 ; 1 1 0 ; 0 1 1')
	return matrix*updator

def getCol(matrix, c):
	return matrix.transpose()[c]

def pos(state):
	print state.transpose()[0]

def vel(state):
	print state.transpose()[1]

def acc(state):
	print state.transpose()[2]

def leng(matrix, row):
	return len(matrix[row].tolist()[0])

def lengr(matrix, row):
	return len(matrix[row].tolist()[0])

def lengc(matrix, col):
	return leng(matrix.transpose(), col)
