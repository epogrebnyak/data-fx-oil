import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime
from quandl import Brent
from cbr import Ruble


# er is Moscow time 11:00-11:30 am MOEX average USDRUR_TOM contract
er = Ruble().get().rename('er')
brent = Brent().get()
assert type(er) == type(brent)

# make dataframe
df0 = pd.concat([brent, er], axis =1)

# add all dates
s = min(df0.index)
e = max(df0.index)
ix = pd.date_range(s, e)
days = [datetime.strftime(x.date(), "%a") for x in ix]
nf = pd.DataFrame(days, ix)
df = pd.concat([nf,df0], axis = 1)# [['brent', 'er']]


# shift dates 
df['er'] = df['er'].shift(-1)
ix2 = df['brent'].notnull() & df['er'].notnull()
df = df.loc[ix2,]
df['brent'] = df['brent'].shift(1)

# one more variable
r_oil = df['brent']*df['er']

# save resulting dataframe
df.to_csv("daily_rub_oil.txt", header=True)


#plot and axis names
plot_title = "Oil vs ruble, 2007-2016"
x_axis_name = "Oil price, USD/b"
y_axis_name = "Exchange rate, RUB/USD"

###############################################################################
#
#    Pandas/matplotlib with seaborn formatting
#
###############################################################################
plt.style.use('seaborn-darkgrid')

#plt.figure(1, figsize=(12, 8), dpi=80)
#df = df['2005-01-01':]
#
#
## draw time series 2
#plt.subplot(221)
#time2 = df['brent'].plot()
#time2.set_xlabel("Year")
#time2.set_ylabel(x_axis_name)
#
## draw time series
#plt.subplot(223)
#time1 = df['er'].plot()
#time1.set_xlabel("Year")
#time1.set_ylabel(y_axis_name)
#
#
## draw time series 3
#plt.subplot(222)
#time3 = r_oil.plot()
#time3.set_xlabel("Year")
#time3.set_ylabel("Oil price, rub/b")

plt.clf() #clears the entire current figure 
plt.figure(2, figsize=(30, 10), dpi=80)
scatter1 = df.plot.scatter(x='brent', y='er', marker = ".")
scatter1.set_xlabel(x_axis_name)
scatter1.set_ylabel(y_axis_name)
scatter1.set_title(plot_title)


###############################################################################


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




