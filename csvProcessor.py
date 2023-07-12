import pandas as pd
import datetime
from rates import *

def processInput(input):
    #dataFrame = pd.read_csv(input, parse_dates=[['Usage date','Interval']], date_format='%m/%d/%y %I:%M %p')
    dataFrame = pd.read_csv(input)

    dataFrame['Datetime'] = pd.to_datetime(dataFrame['Usage date'] + ' ' + dataFrame['Interval'], format='mixed')
    dataFrame['Month'] = pd.DatetimeIndex(dataFrame['Datetime']).strftime('%B').str.lower()
    dataFrame['Hour'] = pd.DatetimeIndex(dataFrame['Datetime']).hour
    dataFrame['Date'] = pd.DatetimeIndex(dataFrame['Datetime']).strftime('%x')
    
    dataFrame.set_index('Datetime', inplace=True)

    print(dataFrame)

    # Find interval during on-peak hours when your home used the most electricity
    
    filter = dataFrame['On-peak kWh'] > 0
    maxes = dataFrame.where(filter).groupby('Date', as_index=False).max('On-peak kWh')
    #recombine to index
    maxes['Hour_int'] = maxes['Hour'].astype(int)
    maxes['Datetime'] = pd.to_datetime(maxes['Date'] + ' ' + maxes['Hour_int'].astype(str), format='mixed')
    maxes.set_index('Datetime', inplace=True)

    # Add it back to the dataset
    dataFrame['IsDailyMax'] = dataFrame.apply(findDailyMax, args=(maxes,), axis=1)

    print(dataFrame)

    # Fill in costs per plan
    dataFrame['e27Cost'] = dataFrame.apply(calcE27Cost, axis=1)

    #print(demandPlans.month['june']['hour'][0])

    return dataFrame

def calcE27Cost(row):
    if row['Off-peak kWh'] > 0:
        #Off Peak
        return row['Off-peak kWh'] * demandPlans.month[row['Month']]['hour'][row['Hour']]
    else:
        #On Peak
        peakCalc = row['On-peak kWh'] * demandPlans.month[row['Month']]['hour'][row['Hour']]
        # TODO: figure out the day's max On-peak kWh, run thru cost calcs on it
        return peakCalc
    
def findDailyMax(row, maxes):
    if row.name in maxes.index:
        return True
    else:
        return False

