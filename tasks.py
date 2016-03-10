# import monthly eop and avg brent price into KEP dataset
# plot scatter brent vs er
# 'little segments': \ - normal or  / - abnormal

# not critical:
# - er as class
# - brent and er symmetrical structure
# - 

from eia import Brent
from cbr import get_er

brent = Brent().series
er = get_er()

def png(ts, filename):
    ax = ts.plot()
    fig = ax.get_figure()
    fig.savefig(filename)
    
png(brent, 'brent.png')
png(er, 'er.png')

# make dataframe
# make scatter df.plot(x = , y = , type='scatter')
# plot ruble value of oil 
# find explaination why commodity currency moves with oil


