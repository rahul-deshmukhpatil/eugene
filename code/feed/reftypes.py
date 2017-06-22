#!/bin/python

product = [ 'OPTIDX', 'FUTIDX']

productSubTypes = {
	'OPT': ['OPTIDX','OPTSTOCK'], 
	'FUT': ['FUTIDX', 'FUTSTOCK'], 
	'STOCK' : ['STOCK']}

#Fields to decide strikes to look for
MAX_EXPIRIES=4

#Fields to decide strikes to look for
STRIKE_SPREAD=1000
STRIKE_SPREAD_PERC=10

#Call Fields
CF_BS=7
CF_BP=8
CF_AP=9
CF_AS=10

F_STRIKE=11

#Put Fields
PF_BS=12
PF_BP=13
PF_AP=14
PF_AS=15

 


