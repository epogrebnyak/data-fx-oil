# import monthly eop and avg brent price into KEP dataset
# plot scatter brent vs er
# 'little segments': \ - normal or  / - abnormal

# not critical:
# - er as class
# - brent and er symmetrical structure
# - 

from eia import Brent
from cbr import get_er

# brent is end of day closing price - which exchange? which contract?
brent = Brent.series

# er is  Moscow time 11:30 am MOEX average USDRUR_TOM contract
er = get_er()

result = pd.concat([brent, er], axis=1)
# plot scatter brent vs er
#
