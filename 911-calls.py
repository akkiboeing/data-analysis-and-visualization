'''
---------------------------------------911-Calls Data Capstone Project---------------------------------------
[-] A practice project to understand Data Analysis and Data Visualization
[-] Dataset taken from kaggle.com
[-] REQUIREMENTS: Python3 with libraries numpy, pandas, seaborn, matplotlib, plotly, cufflinks
--* Install the requirements using the following pip command without the quotes and execute this command in linux terminal or cmd or powershell from the location where 'req.txt' file is present *--
Linux: "sudo pip install -r req.txt"
CMD & Windows PowerShell: "pip install -r req.txt"
-------------------------------------------------------------------------------------------------------------
'''

# import data pre-processing libraries
import numpy as np
import pandas as pd

# import data visualization libraries 
import matplotlib.pyplot as plt
import seaborn as sns
import cufflinks as cf
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
# set %matplotlib inline if you're using Jupyter Notebook

init_notebook_mode(connected = True)
cf.go_offline()

# read the csv file using pandas
df = pd.read_csv("911.csv")

# dataset's info
print(df.info())

# head of the dataframe
print(df.head())

# top 5 zipcodes for 911 calls
print(df['zip'].value_counts().head(5))

# top 5 townships for 911 calls
print(df['twp'].value_counts().head(5))

# number of unique title codes
print(df['title'].nunique())

# pre-process data by creating new features
df['Reason'] = df['title'].apply(lambda x: x.split(':')[0])
print(df['Reason'].value_counts().head())

# countplot of 911 Calls by 'Reason' column
sns.countplot(x = 'Reason', data = df)
plt.show()

# some data pre-processing done again
type(df['timeStamp'].iloc[0])
df['timeStamp'] = pd.to_datetime(df['timeStamp'])
df['Hour'] = df['timeStamp'].apply(lambda x: x.hour)
df['Month'] = df['timeStamp'].apply(lambda x: x.month)
df['Date'] = df['timeStamp'].apply(lambda x: x.date())
df['Day of Week'] = df['timeStamp'].apply(lambda x: x.dayofweek)
dmap = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}
df['Day of Week'] = df['Day of Week'].map(dmap)

# countplot 'Day of Week' column with respect to/hue based off the 'Reason' column
sns.countplot(x = df['Day of Week'], data = df, hue = df['Reason'], palette = 'viridis')
plt.show()

# countplot 'Month' column with respect to/hue based off the 'Reason' column
sns.countplot(x = df['Month'], data = df, hue = df['Reason'], palette = 'viridis')
plt.show()

# data pre-processing done again to fill the missing months as seen from the visualisation done by previous statement
bm = df.groupby('Month').count()
print(bm.head())
bm['twp'].plot()

# create a linear fit on the number of calls per month and visualize it
sns.lmplot(y = 'twp', x = 'Month', data = bm.reset_index())
plt.show()

# visualize the count of 911 calls based on the dates 
df['Date'] = df['timeStamp'].apply(lambda x: x.date())
df.groupby('Date').count()['twp'].plot()
plt.tight_layout()
plt.show()

# visualize the count of calls for the three reasons of 911 calls 
# Reason = EMS
df[df['Reason']=='EMS'].groupby('Date').count()['twp'].plot()
plt.title('EMS')
plt.tight_layout()
plt.show()

# Reason = Traffic
df[df['Reason']=='Traffic'].groupby('Date').count()['twp'].plot()
plt.title('Traffic')
plt.tight_layout()
plt.show()

# Reason = Fire
df[df['Reason']=='Fire'].groupby('Date').count()['twp'].plot()
plt.title('Fire')
plt.tight_layout()
plt.show()

# some data pre-processing done to make 'Hour' become the columns and 'Day of the Week' become the Rows and store it in a new data frame
rd = df.groupby(by=['Day of Week','Hour']).count()['Reason'].unstack()
print(rd.head())

# heatmap & clustermap for the dataframe rd
sns.heatmap(rd, cmap = 'viridis')
sns.clustermap(rd, cmap = 'viridis')
plt.show()

# some data pre-processing done to make 'Month' become the columns and 'Day of the Week' become the Rows and store it in a new data frame
mod = df.groupby(by = ['Day of Week','Month']).count()['Reason'].unstack() 
print(mod.head())

# heatmap & clustermap for the dataframe mod
sns.heatmap(mod, cmap='viridis')
sns.clustermap(mod, cmap='viridis')
plt.show()