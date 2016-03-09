# import monthly eop and avg brent price into KEP dataset
# plot scatter brent vs er
# 'little segments': \ - normal or  / - abnormal

# not critical:
# - er as class
# - brent and er symmetrical structure
# - 

from eia import Brent
from cbr import get_er

brent = Brent.series
er = get_er()