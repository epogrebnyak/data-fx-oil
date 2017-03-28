""" Download Brent FOB price time series from EIA API. """

import json
import pandas as pd
import datetime
import requests

ACCESS_KEY = "15C0821C54636C57209B84FEEE3CE654"
FILENAME_DICT = {'PET.RBRTE.D': ['brent_daily.txt', 'brent']
               , 'PET.RBRTE.M': ['brent_monthly.txt', 'brent']
               , 'PET.RBRTE.A': ['brent_annual.txt', 'brent']}
VALID_IDS = list(FILENAME_DICT.keys())

# -----------------------------------------------------------------------------
# Simple checks

def string_to_date(date_string):
    fmt = {4:'%Y', 6:"%Y%m", 8:"%Y%m%d"}[len(date_string)]    
    return pd.to_datetime(datetime.datetime.strptime(date_string, fmt).date()) 

def is_valid(_id):
    """Ensure variable **_id** is in supported list""" 
    if _id in VALID_IDS: 
        return True
    else: 
        raise ValueError(_id)    

# -----------------------------------------------------------------------------
# Get EIA data
               
def make_url(_id):
    """Return valid URL for data retrieval"""    
    if is_valid(_id):    
        return "http://api.eia.gov/series/?api_key={0}&series_id={1}".format(ACCESS_KEY, _id)    

def yield_json_data(url):
    """Stream data from url as pairs of date and values"""
    r = requests.get(url)
    json_data = json.loads(r.text)    
    parsed_json_data = json_data["series"][0]["data"]
    for row in parsed_json_data:
        date = string_to_date(row[0]) 
        price = float(row[1])
        yield date, price    

def get_data_as_series(_id):
    url = make_url(_id)
    gen = yield_json_data(url)
    data_dicts = dict((date, price) for date, price in gen)
    return pd.Series(data_dicts)   

# -----------------------------------------------------------------------------
# Local file operations

def get_filename(_id):
    if is_valid(_id):
        return FILENAME_DICT[_id][0]  
    
def get_local_data_as_series(_id):
    filename = get_filename(_id)
    df = pd.read_csv(filename, index_col=0, header=None, names=['date', 'brent'])
    df.index = pd.to_datetime(df.index)
    df = df.round(2)    
    ts = df[df.columns[0]]   
    return ts  

def save_local_data(_id, df):
    filename = get_filename(_id)
    df.to_csv(filename, header = False)
    
# -----------------------------------------------------------------------------
    
class LocalDataset():
    
    def __init__(self, _id):        
        self._id = _id
        try:
            self.ts = get_local_data_as_series(_id)
        except:
            print("Cannot load from file: " + self.filename)
            self.update()


    def update(self):
       self.ts = get_data_as_series(self._id)
       save_local_data(self._id, self.ts)
       return self
   
       
    def get(self):
        return self.ts.rename(FILENAME_DICT[self._id][1]) 

    
class DailyBrent(LocalDataset):
    def __init__(self):
        super().__init__("PET.RBRTE.D")


class MonthlyBrent(LocalDataset):
    def __init__(self):
        super().__init__("PET.RBRTE.M")

   
class AnnualBrent(LocalDataset):
    def __init__(self):
        super().__init__("PET.RBRTE.A")    
    
# -----------------------------------------------------------------------------

# def __str__(self):
#    print ("1")
#    AnnualBrent().update()
#    Out[62]: <__main__.AnnualBrent at 0xc141530>

#### Critical:

# Brent.annual() not correct, must be comparable to AnnualBrent()
# Brent.monthly() must be comparable to MonthlyBrent().series

#    # COMMENT: from pandas documentation - 
#    # 
#    # http://pandas.pydata.org/pandas-docs/stable/timeseries.html#resampling
#    # Any function available via dispatching can be given to the how parameter by name, including 
#    # sum, mean, std, sem, max, min, median, first, last, ohlc.

#    # WARNING: labels with last day of month, irrespective of whether business day of nor, 
#    #          information about last actual reported day in month is lost
    
  
#    def quarterly(self, eop = False):
#        return self.__eop_or_avg__(eop, "Q")

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    
    assert string_to_date("2015") ==  pd.Timestamp('2015-01-01 00:00:00')    
    assert get_filename('PET.RBRTE.D') == 'brent_daily.txt'
    assert isinstance(DailyBrent().get(), pd.Series)
    assert DailyBrent().get()['2016-02-16'] == 31.09
    
    # update local files using internet access:
    # DailBrent().update()
    # MonthlyBrent().update()
    # AnnualBrent().update()
    
    d = DailyBrent().get()    
    m_eop = d.resample('M').last()
    
    m2 = MonthlyBrent().get()
    m_avg = d.resample('M').mean().round(2)
    
    a2 = AnnualBrent().get().round(2)
    a_avg = d.resample('A').mean().round(2)
    
    #join together - avg + monthly
    
   
    
# ----------------------------------------------------------------------------------------------------------------
#   API calls
# ----------------------------------------------------------------------------------------------------------------

"""
http://api.eia.gov/series/categories/?series_id=PET.RBRTE.D&api_key=15C0821C54636C57209B84FEEE3CE654
http://api.eia.gov/category/?api_key=15C0821C54636C57209B84FEEE3CE654&category_id=241335
http://api.eia.gov/category/?api_key=15C0821C54636C57209B84FEEE3CE654&category_id=714757
"""

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