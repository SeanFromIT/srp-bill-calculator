# Written against Python 3.9.0 on Windows
# Requires pandas:
# pip install pandas
import argparse
from csvProcessor import *
from rates import *

parser = argparse.ArgumentParser()
parser.add_argument("net")
args = parser.parse_args()
netEnergy = args.net

# E27
e27Result = fixedFee
# Calculate Net Energy?
#...add to result...
processInput(netEnergy)

# IF Net Energy doesn't work...
# Process & Calculate Usage
#...add to result...

# IF Net Energy doesn't work...
# Process & Calculate Generation
#...add to result...

# Process & Calculate Demand
#...add to result...

# E15
e15Result = fixedFee
# Calculate Net Energy?
#...add to result...

# IF Net Energy doesn't work...
# Process & Calculate Usage
#...add to result...

# IF Net Energy doesn't work...
# Process & Calculate Generation
#...add to result...

# Process & Calculate Demand
#...add to result...

# E13
e13Result = fixedFee
# Calculate Net Energy?
#...add to result...

# IF Net Energy doesn't work...
# Process & Calculate Usage
#...add to result...

# IF Net Energy doesn't work...
# Process & Calculate Generation
#...add to result...

# Process & Calculate Demand
#...add to result...

# E14
e14Result = fixedFee
# Calculate Net Energy?
#...add to result...

# IF Net Energy doesn't work...
# Process & Calculate Usage
#...add to result...

# IF Net Energy doesn't work...
# Process & Calculate Generation
#...add to result...

# Process & Calculate Demand
#...add to result...

# Print Results
results = {
    'E27': e27Result,
    'E15': e15Result,
    'E13': e13Result,
    'E14': e14Result
}
print("Under E27 you would have paid... $" + e27Result)
print("Under E15 you would have paid... $" + e15Result)
print("Under E13 you would have paid... $" + e13Result)
print("Under E14 you would have paid... $" + e14Result)
print("The most affordable plan based on your inputs was " + min(results, key=results.get))
