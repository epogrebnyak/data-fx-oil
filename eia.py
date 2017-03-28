""" Download Brent FOB price time series from EIA API. """

import json
import pandas as pd
import datetime
import requests

ACCESS_KEY = "15C0821C54636C57209B84FEEE3CE654"
FILENAME_DICT = {'PET.RBRTE.D': 'brent_daily.txt'
               , 'PET.RBRTE.M': 'brent_monthly.txt'
               , 'PET.RBRTE.A': 'brent_annual.txt'}
VALID_IDS = list(FILENAME_DICT.keys())

def __string_to_date__(date_string, fmt):
    return pd.to_datetime(datetime.datetime.strptime(date_string, fmt).date()) 

def is_valid(_id):
    """Ensure variable **_id** is in supported list""" 
    if _id in VALID_IDS: 
        return True
    else: 
        raise ValueError(_id)    
               
def make_url(_id):
    """Return valid URL for data retrieval"""    
    if is_valid(_id):    
        return "http://api.eia.gov/series/?api_key={0}&series_id={1}".format(ACCESS_KEY, _id)    

def make_filename(_id):        
    if is_valid(_id):
        return FILENAME_DICT[_id]
        
def yield_json_data(self, url):
    """Stream data from url as pairs of date and values"""
    r = requests.get(url)
    json_data = json.loads(r.text)    
    parsed_json_data = json_data["series"][0]["data"]
    for row in parsed_json_data:
        date = __string_to_date__(row[0], "%Y%m%d") 
        price = float(row[1])
        yield date, price    

def get_data_by_id(_id):
    url = make_url(_id)
    gen = yield_json_data(url)
    data_dicts = dict((date, price) for date, price in gen)
    return pd.Series(data_dicts) 

def get_filename(_id):
    if is_valid(_id):
        return FILENAME_DICT[_id]    
    
def get_local_data(_id):
    filename = FILENAME_DICT[_id] 
    df = pd.read_csv(filename, index_col = 0) 
    df.index = pd.to_datetime(df.index)
    return df.round(2)

def save_local_data(_id, df):    
    
def        




#### Critical:

# Brent.annual() not correct, must be comparable to AnnualBrent()
# Brent.monthly() must be comparable to MonthlyBrent().series

#### Not critical: 

# QUESTION: can class instance itself be Series object allowing ```brent = DailyBrent()```


               
class EIA():
    
    ACCESS_KEY = "15C0821C54636C57209B84FEEE3CE654"

    FILENAME_DICT = {'PET.RBRTE.D': 'brent_daily.txt'
                   , 'PET.RBRTE.M': 'brent_monthly.txt'
                   , 'PET.RBRTE.A': 'brent_annual.txt'}
    
    def update(self):
       gen = self.yield_json_data(self.url)
       self.series = self.as_series(gen)
       self.save_csv()
       
    def __init__(self, id):
        self.id = id
        try:
            self.load_saved_series()
        except:
            print("Cannot load from file: " + self.filename)
       
    @property
    def url(self):
        """Valid API URL for *id* like 'PET.RBRTE.D' """
        return "http://api.eia.gov/series/?api_key={0}&series_id={1}".format(self.ACCESS_KEY, self.id)    

    @staticmethod
    def string_to_date(date_string):
        return __string_to_date__(date_string, "%Y%m%d") 
        
    def yield_json_data(self, url):
        """Stream data from url as pairs of date and values"""
        r = requests.get(url)
        json_data = json.loads(r.text)    
        parsed_json_data = json_data["series"][0]["data"]
        for row in parsed_json_data:
            date = self.string_to_date(row[0])
            price = float(row[1])
            yield pd.to_datetime(date), float(price)
        
    @staticmethod
    def as_series(gen):
        data_dicts = dict((date, price) for date, price in gen)
        return pd.Series(data_dicts)  
    
    @property
    def filename(self):        
        if self.id in self.FILENAME_DICT.keys():
           return self.FILENAME_DICT[self.id]
        else:
           return self.id + ".txt"
    
    def save_csv(self):
        self.series.to_csv(self.filename)

    def get_saved_df(self):
        df = pd.read_csv(self.filename, index_col = 0) 
        df.index = pd.to_datetime(df.index)
        return df.round(2)

    def load_saved_series(self):
        df = self.get_saved_df()
        self.series = df[df.columns[0]]
        return self.series  
        
# import daily, monthly and annual brent
class Brent(EIA):
    def __init__(self):
        super().__init__("PET.RBRTE.D")

    def daily(self):
        return self.series
        
    def __eop_or_avg__(self, eop:bool, ltr:str):
        if eop:
            return self.series.resample(ltr, how = 'last')
        else:
            return self.series.resample(ltr, how = 'mean')
    
    # 
    # COMMENT: from pandas documentation - 
    # 
    # http://pandas.pydata.org/pandas-docs/stable/timeseries.html#resampling
    # Any function available via dispatching can be given to the how parameter by name, including 
    # sum, mean, std, sem, max, min, median, first, last, ohlc.
    #
    # WARNING: labels with last day of month, irrespective of whether business day of nor, 
    #          information about last actual reported day in month is lost
    
    def monthly(self, eop = False):
        return self.__eop_or_avg__(eop, "M")
    
    def quarterly(self, eop = False):
        return self.__eop_or_avg__(eop, "Q")
    
    def annual(self, eop = False):
        return self.__eop_or_avg__(eop, "12M")
            
class MonthlyBrent(EIA):

    def __init__(self):
        super().__init__("PET.RBRTE.M")

    @staticmethod
    def string_to_date(date_string):
        return __string_to_date__(date_string, "%Y%m") 

class AnnualBrent(EIA):

    def __init__(self):
        super().__init__("PET.RBRTE.A")

    @staticmethod
    def string_to_date(date_string):
        return  __string_to_date__(date_string, "%Y") 

if __name__ == "__main__":
    
    assert Brent().filename == 'brent_daily.txt'
    assert isinstance(Brent().series, pd.Series)
    assert Brent().series['2016-02-16'] == 31.09
    
    # update local files using internet access:
    Brent().update()
    # MonthlyBrent().update()
    # AnnualBrent().update()
    
    brent = Brent().series
    
    brent_a_avg = Brent().annual()
    brent_q_avg = Brent().quarterly()
    brent_m_avg = Brent().monthly()

    brent_a_eop = Brent().annual(eop = True)
    brent_q_eop = Brent().quarterly(eop = True)
    brent_m_eop = Brent().monthly(eop = True)
    
    ab = AnnualBrent().series
    mb = MonthlyBrent().series
    
    
# ----------------------------------------------------------------------------------------------------------------
#   API calls
# ----------------------------------------------------------------------------------------------------------------

#http://api.eia.gov/series/categories/?series_id=PET.RBRTE.D&api_key=15C0821C54636C57209B84FEEE3CE654
#http://api.eia.gov/category/?api_key=15C0821C54636C57209B84FEEE3CE654&category_id=241335
#http://api.eia.gov/category/?api_key=15C0821C54636C57209B84FEEE3CE654&category_id=714757


# ----------------------------------------------------------------------------------------------------------------
#   JSON output reference
# ----------------------------------------------------------------------------------------------------------------


"""Sample output (whitespaces added below for readability). From http://www.eia.gov/opendata/commands.cfm#series_query

{
"request":{
    "command":"series",
    "series_id":"ELEC.GEN.ALL-AK-99.A"
    },

"series":[
        {
        "series_id":"ELEC.GEN.ALL-AK-99.A"
        "name":"Net Generation : All Fuels : Alaska : All Sectors",
        "units":"thousand megawatthours",
        "f":"A",
        "unitsshort":"",
        "description":"Summation of all fuels used for electricity generation; All sectors; ",
        "copyright":"None",
        "source":"EIA, U.S. Energy Information Administration",
        "iso3166":"USA-AK", DEPRECATED
        "lat":"", DEPRECATED
        "lon":"", DEPRECATED
        "latlon":"43.5589,-91.2325", 
        "latlon2":"43.5589,-91.2325", 
        "geography":"USA-AK", 
        "geography2":"USA-AK", 
        "lastHistoricalPeriod":"2013", 
        "start":"2001",
        "end":"2013",
        "updated":"2013-08-23T17:37:44-0400",
        "data":[
        ["2012",6979.39223],
        ["2011",6871.03279],
        ["2010",6759.5757],
        ["2009",6702.15939],
        ["2008",6774.83438],
        ...
        }
    ]
}
"""