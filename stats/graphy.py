#!/usr/bin/python3

import operator

from datetime import datetime,timedelta
from math import fabs
from statistics import mean,median,stdev
import numpy as np

from Transaction import Transaction
from TransactEngine import TransactEngine
from prettyprint import p as p


def moneyLimit(date, totalMoney):
	return totalMoney > -500 and dateLimit(date, totalMoney)

def dateLimit(date, totalMoney):
	return date < datetime(2017, 5, 2)

totalOnHand = 1100-240
p.printhl("$%.2f\n" % totalOnHand, totalOnHand)

carT = Transaction.createByDayOfWeek(6, -36.0, "Car Payment")
insT = Transaction.createByDay(20, -80.0, "Car Insurance")
coffee = [Transaction.createByDayOfWeek(i, -1.35, "Coffee Food") for i in range(1,6)]
breakfast = [Transaction.createByDayOfWeek(i, -2, "Breakfast Food") for i in range(1,6)]
lunch = [Transaction.createByDayOfWeek(i, -3.5, "Lunch Food") for i in range(1,6)]
dinner = [Transaction.createByDayOfWeek(i, -3.5, "Dinner Food") for i in range(1,6)]
weekend = Transaction.createByDayOfWeek(6, -20, "Weekend Food")
weeklyAllowance = Transaction.createByDayOfWeek(6, -50, "Weekly Allowance")
japanSavings = Transaction.createByDayOfWeek(6, -85, "Japan Savings")
SmashTourneys = Transaction.createByDayOfWeek(6, -10, "Smash Tourneys")

pay = 23*35*.75
pxp_pay = Transaction.createByDayOfWeek(5, pay, "PXP Pay")

rent2 = [Transaction.createByMonth(2, i, -268, "Rent") for i in [1,2,3,4,5]]

tuition1 = Transaction.createByMonth(5,1,-2835.79/3-50, "Tuition")
tuition2 = Transaction.createByMonth(5,2,-2835.79/3, "Tuition")
tuition3 = Transaction.createByMonth(5,3,-2835.79/3, "Tuition")
tuition4 = Transaction.createByMonth(5,7,-3986.79/3-50, "Tuition")
tuition5 = Transaction.createByMonth(5,8,-3986.79/3, "Tuition")
tuition6 = Transaction.createByMonth(5,9,-3986.79/3, "Tuition")

trans = [carT, insT, weekend, tuition1, tuition2, tuition3, tuition4, tuition5, tuition6, weeklyAllowance, SmashTourneys, pxp_pay, japanSavings]
trans = trans + breakfast + lunch + dinner + rent2
engine = TransactEngine(totalOnHand, trans)

finalTotal, datecashlist,minimumDate,maximumDate = engine.simulate(moneyLimit, True)
for thing in datecashlist: print("Date: %s, $%.2f " %(thing[0], thing[1]))
print(finalTotal)

totalsByItem = engine.getTotalsByItem()

totalExpenses = sum([totalsByItem[key] for key in totalsByItem if totalsByItem[key] < 0])
totalEarnings = sum([totalsByItem[key] for key in totalsByItem if totalsByItem[key] > 0])
totalFood = sum([totalsByItem[key] for key in totalsByItem if totalsByItem[key] < 0 and "Food" in key])

for k,v in sorted(totalsByItem.items(), key=operator.itemgetter(1)):
	print("{:20s}  ${:7.2f} {:7.2f}%".format(k,v,v/totalExpenses*100))
print("{:20s}  ${:7.2f} {:7.2f}%".format("Total Food",totalFood,totalFood/totalExpenses*100))

print("Minimum Date: %s, $%.2f" % (minimumDate[0],minimumDate[1]))
print("Maximum Date: %s, $%.2f" % (maximumDate[0],maximumDate[1]))
print("Average Money: $%.2f" % mean([dc[1] for dc in datecashlist]))
print("Median Money: $%.2f" % median([dc[1] for dc in datecashlist]))
print("Std Dev Money: $%.2f" % stdev([dc[1] for dc in datecashlist]))
print("Total Expenses: ",totalExpenses)
print("Total Earnings: ",totalEarnings)

import matplotlib.pyplot as plot
fig = plot.figure()
ax = fig.add_subplot(111)
x = [d[0] for d in datecashlist]
y = [d[1] for d in datecashlist]
ax.plot(x, y)
ax.set_ylim(0)
plot.show()
