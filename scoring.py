#!/usr/bin/python

def getHighScore(i):
	with open("highscore.txt","r") as f:
		for n in range(i+1):
#			print n
			high = int(f.readline())
#	print high
	return high

def setHighScore(score, i):
	with open("highscore.txt","r") as f:
		fa = f.readlines()
	fa[i] = str(score)+"\n"
	with open("highscore.txt","w+") as f:
		for n in range(len(fa)):
			f.write(fa[n])

