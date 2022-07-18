# -----------------------------------------------pegasus_th----------------------------------------------

FUNCTIONING:

parse and process a csv with historical data downloaded from http://www.climagro.com.ar/Estaciones (the pegasus download is xlsx and must be saved in CSV).
can process temperature and humidity data

creates a directory in the same place where the script is located called "Analysis YYYY-MM-DD , HH-MM--SS ,
dataset" in which the following files are saved: days_values(csv data averaged per day), stats(csv monthly statistics), figures (pdf with 3 plots).

## required libraries:
sys
os
pandas
numpy
matplotlib.pyplot
seaborn
datetime
matplotlib.backends.backend_pdf


It is used by command line indicating the following arguments:

args[0] = pegasus.py (required)
args[1] = dataset (required)
args[2] = variable (required, can be 'temperature' or 'humidity')
args[3] = startline (optional, default=6)
args[4] = encoding (optional, default='cp1252')


dataset is a str, name of the csv file
startline is an int, previous line number where the row begins with the element "Date,Value"
encoding is a str

the csv to process has to be located in the same folder where the script is located

As an example, the 'temp' and 'humidity' files. set in cmd the directory where the script and the csv is located and write:
python pegasus.py temp.csv temperature
python pegasus.py humidity.csv humidity
