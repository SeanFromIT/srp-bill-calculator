import pandas as pd
import datetime
from rates import *

def processInput(input):
    # Load File
    dataFrame = pd.read_csv(input)

    # Format Columns
    dataFrame['Datetime'] = pd.to_datetime(dataFrame['Usage date'] + ' ' + dataFrame['Interval'], format='mixed')
    dataFrame['Month'] = pd.DatetimeIndex(dataFrame['Datetime']).strftime('%B').str.lower()
    dataFrame['Hour'] = pd.DatetimeIndex(dataFrame['Datetime']).hour
    dataFrame['Date'] = pd.DatetimeIndex(dataFrame['Datetime']).strftime('%x')
    dataFrame.set_index('Datetime', inplace=True)

    onPeakFilter = dataFrame['On-peak kWh'] > 0

    # Find interval during on-peak hours when your home used the most electricity, daily
    dailyMaxes = dataFrame.where(onPeakFilter).groupby('Date', as_index=False).max('On-peak kWh')
    # Recombine to index
    dailyMaxes['Hour_int'] = dailyMaxes['Hour'].astype(int)
    dailyMaxes['Datetime'] = pd.to_datetime(dailyMaxes['Date'] + ' ' + dailyMaxes['Hour_int'].astype(str), format='mixed')
    dailyMaxes.set_index('Datetime', inplace=True)
    # Add it back to the dataset
    dataFrame['IsDailyMax'] = dataFrame.apply(findDailyMax, args=(dailyMaxes,), axis=1)
    averageDemand = dataFrame.where(dataFrame['IsDailyMax']).groupby('Month', as_index=False).mean('On-peak kWh')
    # Cleanup dataset
    averageDemand = averageDemand.drop(['Off-peak kWh', 'Hour'], axis=1)

    # Find interval during on-peak hours when your home used the most electricity, monthly
    monthlyMaxes = dataFrame.where(onPeakFilter).groupby('Month', as_index=False).max('On-peak kWh')
    # Cleanup dataset
    monthlyDemand = monthlyMaxes.drop(['Off-peak kWh', 'Hour'], axis=1)

    # Determine costs per plan
    ################
    # DEMAND PLANS #
    ################
    dataFrame['demandCost'] = dataFrame.apply(calcDemandCost, axis=1)

    #######
    # E13 #
    #######
    dataFrame['e13Cost'] = dataFrame.apply(calcE13Cost, axis=1)

    #######
    # E14 #
    #######
    dataFrame['e14Cost'] = dataFrame.apply(calcE14Cost, axis=1)

    return [dataFrame, monthlyDemand, averageDemand]

# Helper functions

def findDailyMax(row, maxes):
    if row.name in maxes.index:
        return True
    else:
        return False

def calcDemandCost(row):
    if row['Off-peak kWh'] > 0:
        #Off Peak
        return row['Off-peak kWh'] * demandPlans.month[row['Month']]['hour'][row['Hour']]
    else:
        #On Peak
        return row['On-peak kWh'] * demandPlans.month[row['Month']]['hour'][row['Hour']]
    
def calcE13Cost(row):
    if row['Off-peak kWh'] != 0:
        #Off Peak
        if row['Off-peak kWh'] > 0:
            #Consuming
            return row['Off-peak kWh'] * e13.month[row['Month']]['hour'][row['Hour']]
        else:
            #Selling Back
            return row['Off-peak kWh'] * e13.sellBackRate
    else:
        #On Peak
        if row['On-peak kWh'] > 0:
            #Consuming
            return row['On-peak kWh'] * e13.month[row['Month']]['hour'][row['Hour']]
        else:
            #Selling Back
            return row['On-peak kWh'] * e13.sellBackRate

def calcE14Cost(row):
    if row['Off-peak kWh'] != 0:
        #Off Peak
        if row['Off-peak kWh'] > 0:
            #Consuming
            return row['Off-peak kWh'] * e14.month[row['Month']]['hour'][row['Hour']]
        else:
            #Selling Back
            return row['Off-peak kWh'] * e14.sellBackRate
    else:
        #On Peak
        if row['On-peak kWh'] > 0:
            #Consuming
            return row['On-peak kWh'] * e14.month[row['Month']]['hour'][row['Hour']]
        else:
            #Selling Back
            return row['On-peak kWh'] * e14.sellBackRate