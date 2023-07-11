import pandas as pd
import datetime
from rates import *

def processInput(input):
    dataFrame = pd.read_csv(input, parse_dates=[['Usage date', 'Interval']], date_format='%m/%d/%y %I:%M %p')
    #print(dataFrame['Usage date_Interval'])
#    for row in dataFrame.itertuples():
#        month = 
#    print(dataFrame['Usage date'])

    dataFrame['Month'] = pd.DatetimeIndex(dataFrame['Usage date_Interval']).strftime('%B').str.lower()
    dataFrame['Hour'] = pd.DatetimeIndex(dataFrame['Usage date_Interval']).hour

    dataFrame['e27Cost'] = dataFrame.apply(calcE27Cost, axis=1)

    #print(demandPlans.month['june']['hour'][0])

    #print (dataFrame)

    return dataFrame

def calcE27Cost(row):
    if row['Off-peak kWh'] > 0:
        #Off Peak
        return row['Off-peak kWh'] * demandPlans.month[row['Month']]['hour'][row['Hour']]
    else:
        #On Peak
        #TODO
        return 0