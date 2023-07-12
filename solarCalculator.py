# Written against Python 3.9.0 on Windows, tested on Python 3.11.2 on Mac
# Requires pandas:
# pip install pandas
import argparse
import pandas as pd
from csvProcessor import *
from rates import *

parser = argparse.ArgumentParser()
parser.add_argument("-net", help="Path to your hourlyNetEnergy*.csv file")
args = parser.parse_args()
netEnergy = args.net

def calcDemandCharge(month, kWh):
    demandCharge = 0
    iter = 0
    while kWh > 0:
        if iter < 10:
            demandCharge = demandCharge + demandPlans.month[month]['demandCharge'][iter]
        else:
            demandCharge = demandCharge + demandPlans.month[month]['demandChargeRemainder']
        iter += 1
        kWh -= 1
    return demandCharge

# Calculate Net Energy?
netEnergyCalc = processInput(netEnergy)

####################
# DEMAND PLAN BASE #
####################
demandPlanBase = fixedFee + netEnergyCalc[0]['demandCost'].sum()

#######
# E27 #
#######
e27Result = demandPlanBase
# Add Demand Charge using Monthly Max
for index, row in netEnergyCalc[1].iterrows():
    e27Result = e27Result + calcDemandCharge(row['Month'], row['On-peak kWh'])
# Add taxes
taxes = e27Result * tax
e27Result = e27Result + taxes
# Round to cents
e27Result = round(e27Result, 2)

#######
# E15 #
#######
e15Result = demandPlanBase
# Add Demand Charge using Monthly Average of Daily Maxes
for index, row in netEnergyCalc[2].iterrows():
    monthlyAverageDemandCharge = demandPlans.month[row['Month']]['averageDemandCharge'] * row['On-peak kWh']
    e15Result = e15Result + monthlyAverageDemandCharge
# Add taxes
taxes = e15Result * tax
e15Result = e15Result + taxes
# Round to cents
e15Result = round(e15Result, 2)

#######
# E13 #
#######
e13Result = fixedFee + netEnergyCalc[0]['e13Cost'].sum()
# Add taxes
taxes = e13Result * tax
e13Result = e13Result + taxes
# Round to cents
e13Result = round(e13Result, 2)

#######
# E14 #
#######
e14Result = fixedFee + netEnergyCalc[0]['e14Cost'].sum()
# Add taxes
taxes = e14Result * tax
e14Result = e14Result + taxes
# Round to cents
e14Result = round(e14Result, 2)

# Print Results
results = {
    'E27': e27Result,
    'E15': e15Result,
    'E13': e13Result,
    'E14': e14Result
}
print("Under E27 [Customer Generation Price Plan] you would have paid... $" + str(e27Result))
print("Under E15 [Average Demand Price Plan] you would have paid... $" + str(e15Result))
print("Under E13 [Time-of-Use Export Price Plan] you would have paid... $" + str(e13Result))
print("Under E14 [Electric Vehicle (EV) Export Price Plan] you would have paid... $" + str(e14Result))
print("The most affordable plan based on your inputs was " + min(results, key=results.get))