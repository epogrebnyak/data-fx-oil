import pandas as pd
from eia import Brent
from cbr import get_er

# brent is end of day closing price - which exchange? which contract?
brent = Brent().series

# er is  Moscow time 11:30 am MOEX average USDRUR_TOM contract
er = get_er()

def png(ts, filename):
    ax = ts.plot()
    fig = ax.get_figure()
    fig.savefig(filename)
    
png(brent, 'brent.png')
png(er, 'er.png')

# plot scatter brent vs er
r = pd.concat([brent, er], join = 'inner', axis=1) 
r.columns = ['brent', 'er']
ax = r.plot(x='brent', y='er', kind='scatter')
fig = ax.get_figure()
fig.savefig('scatter.png')

# too many dates are missing   
# plot ruble value of oil 
# find explaination why commodity currency moves with oil
# import monthly eop and avg brent price into KEP dataset
# segments

# not critical:
# er as class
# brent and er symmetrical structure
