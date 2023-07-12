# srp-bill-calculator
A python rewrite of cheald/srp-bill-calculator for SRP's new export format.

This program calculates what your costs would have been under each of SRP's solar plans given an Hourly/Interval Net Energy Usage Export.

Requirements:
* python3
* pandas (install by running: `pip install pandas`)

Usage:
`python3 solarCalculator.py -net /path/to/hourlyNetEnergy*.csv`
where `/path/to/hourlyNetEnergy*.csv` is the file you downloaded from SRP's website from this screen:

![Screenshot of the SRP website Export to Excel feature.](ExportToExcel.png)