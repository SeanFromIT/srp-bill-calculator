import pandas as pd
import datetime

def processInput(input):
    dataFrame = pd.read_csv(input, parse_dates=[['Usage date', 'Interval']])
    #print(dataFrame['Usage date_Interval'])
    for row in dataFrame.itertuples():
        month = 
