import pandas as pd

#https://www.quandl.com/data/CHRIS/ICE_B1-Brent-Crude-Futures-Continuous-Contract-1-B1-Front-Month

URL = "https://www.quandl.com/api/v3/datasets/CHRIS/ICE_B1.csv?api_key=vaWNxpNxVaPe4DUn5oMz"

df = pd.read_csv(URL, index_col=0)
brent2 = df["Settle"].sort_index()