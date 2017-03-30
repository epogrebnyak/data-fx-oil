# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 16:28:26 2017

@author: PogrebnyakEV
"""

import pandas as pd
import matplotlib.pyplot as plt
import bokeh.charts as bh

# dataframe
df= pd.read_csv("daily_rub_oil.txt", header=0, index_col=0)



#plot and axis names
plot_title = "Oil vs ruble, 2005-2016"
x_axis_name = "Oil price, USD/b"
y_axis_name = "Exchange rate, RUB/USD"

###############################################################################
#
#    Pandas/matplotlib with seaborn formatting
#
###############################################################################
plt.style.use('seaborn-darkgrid')

dict(figsize=(12, 8), dpi=80)

df = df['2005-01-01':]
r_oil = df['er'] * df['brent']


plt.figure(1)

## draw time series 2
time2 = df['brent'].plot()
time2.set_xlabel("Year")
time2.set_ylabel(x_axis_name)

plt.figure(2)
## draw time series
time1 = df['er'].plot()
time1.set_xlabel("Year")
time1.set_ylabel(y_axis_name)

plt.figure(3)
## draw time series 3
time3 = r_oil.plot()
time3.set_xlabel("Year")
time3.set_ylabel("Oil price, rub/b")

plt.figure(4)

df1 = df[:-15]
df2 = df[-15:]

scatter1 = df1.plot.scatter(x='brent', y='er', marker = ".", color = 'blue')
scatter1.scatter(x=df2['brent'], y=df2['er'], marker = ".", color = 'red')

scatter1.set_xlabel(x_axis_name)
scatter1.set_ylabel(y_axis_name)
scatter1.set_title(plot_title)


# -----------------------------------------------------------------------------
#
#    Bokeh charts*3
#
# -----------------------------------------------------------------------------

p = bh.Scatter(df, x='brent', y='er', title="Oil vs ruble, 2007-2016",
               xlabel=x_axis_name , ylabel=y_axis_name, color ='blue')
bh.output_file("scatter.html")
bh.show(p)

# -----------------------------------------------------------------------------
#
#    Save as csv and xlsx
#
# -----------------------------------------------------------------------------


if len(df.columns) == 3:
   df=df.drop(df.columns[0], axis=1)
df = df.round(4)
df.to_csv("fx.csv")
df.to_excel("fx.xlsx")



# -----------------------------------------------------------------------------
#
#    Questions
#
# -----------------------------------------------------------------------------


# Q4: how do I control labels order - which label is for which line
# time1.legend([x_axis_name, y_axis_name], loc=2)


## plotting
#
## plot scatter brent vs er
#def png(ts, filename):
#    ax = ts.plot()
#    fig = ax.get_figure()
#    fig.savefig(filename)
#    
#Figure(0)
#r_oil['2016-01-01' : '2017-03-28'].plot()
#
#Figure(1)
#png(brent, 'brent.png')
#png(er, 'er.png')
#
#Figure(2)
#ax = df.plot(x='brent', y='er', kind='scatter')
#fig = ax.get_figure()
#fig.savefig('scatter.png')