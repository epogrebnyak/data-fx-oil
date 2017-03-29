# Load oil price data from quandl
#
# URL:
# https://www.quandl.com/data/CHRIS/ICE_B1-Brent-Crude-Futures-Continuous-Contract-1-B1-Front-Month


import pandas as pd

# please use your own token
TOKEN = "vaWNxpNxVaPe4DUn5oMz"

SPEC = {        
   'URL': "https://www.quandl.com/api/v3/datasets/CHRIS/ICE_B1.csv?api_key={}".format(TOKEN)
 , 'var_name': 'brent'
 , 'local_filename': 'quandl_ice_brent.txt'
 }


def get_local_data():
    df = pd.read_csv(SPEC['local_filename'], index_col=0, header=0)
    df.index = pd.to_datetime(df.index)
    df = df.round(2)    
    # return pd.Series object
    ts = df[df.columns[0]]   
    return ts  
    

def get_web_data():
    df = pd.read_csv(SPEC['URL'], index_col=0)
    brent = df["Settle"].sort_index().rename(SPEC['var_name'])
    brent.index = pd.to_datetime(brent.index)
    return brent 
    
def save_to_local(df):
    filename = SPEC['local_filename']
    df.to_csv(filename, header = True)
 

class Brent():    
    def __init__(self):                
        try:
            self.ts = get_local_data()
        except:
            print("Cannot load from local file, updating...")
            self.update()

    def update(self):
       self.ts = get_web_data()
       save_to_local(self.ts)
       return self
       
    def get(self):
        return self.ts
    
if __name__ == "__main__":
    oil = Brent().get()
    print(oil.tail())
    # Brent().update()