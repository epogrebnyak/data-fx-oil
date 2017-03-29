import pandas as pd

from quandl import brent
from cbr import get_er


# er is Moscow time 11:00-11:30 am MOEX average USDRUR_TOM contract
er = get_er()
er.columns = ['er']

z = pd.concat([er, brent], axis =1)

s = min(z.index)
e = max(z.index)
ix = pd.date_range(s, e)
nf = pd.DataFrame([0 for x in range(len(ix))], ix)
w = pd.concat([nf,z], axis = 1)

w['brent'] = w['brent'].shift(-1)
w['er'] = w['er'].shift(-1)
iz = w['brent'].notnull() & w['er'].notnull()
a = w[iz][['brent', 'er']]
a.plot()
a.plot(x='brent', y='er', kind='scatter')
a[-100:].plot(x='brent', y='er', kind='scatter')
(a['brent']*a['er'])[-1000:].plot()

# plot scatter brent vs er
def png(ts, filename):
    ax = ts.plot()
    fig = ax.get_figure()
    fig.savefig(filename)
    
png(brent, 'brent.png')
png(er, 'er.png')

ax = a.plot(x='brent', y='er', kind='scatter')
fig = ax.get_figure()
fig.savefig('scatter.png')

# Questions and concerns
# brent is end of day closing price - which exchange? which contract?
# too many dates are missing   
# plot ruble value of oil 
# find explaination why commodity currency moves with oil
# import monthly eop and avg brent price into KEP dataset
# segments

# not critical:
# er as class
# brent and er symmetrical structure
