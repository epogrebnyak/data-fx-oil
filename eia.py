""" Download Brent FOB price time series from EIA API. """

from urllib.request import urlopen
import json
import pandas as pd
import datetime

ACCESS_KEY = "15C0821C54636C57209B84FEEE3CE654"

def string_to_date(date_string):
    return datetime.datetime.strptime(date_string, "%Y%m%d").date() 

class EIA():
    
    def __init__(self, id):
       self.url = self.series_url(id)
       raw_data = self.get_restful_data(self.url)
       datapoints = self.parse_json(raw_data)
       self.series = self.as_series(datapoints)        
    
    @staticmethod
    def series_url(id, key = ACCESS_KEY):
        return "http://api.eia.gov/series/?api_key={0}&series_id={1}".format(key, id)    

    @staticmethod
    def get_restful_data(url):
        """Retrieves data from URL"""    
        with urlopen(url) as f:
            url_data = f.read().decode()
        return url_data
        
    @staticmethod
    def parse_json(url_data):
        """Returns a list of time series values from API output"""
        json_data = json.loads(url_data)    
        return json_data["series"][0]["data"]

    @staticmethod
    def yield_tuples(flat_list):
        for row in flat_list:
            date = string_to_date(row[0])
            price = row[1]
            yield date, price

    def as_series(self, flat_list):
        data_dict = dict((pd.to_datetime(date), price) for date, price in self.yield_tuples(flat_list))
        return pd.Series(data_dict)  
        
# import daily, monthly and annual brent
class DailyBrent(EIA):
    def __init__(self):
        super().__init__("PET.RBRTE.D")
        
class MonthlyBrent(EIA):
    def __init__(self):
        super().__init__("PET.RBRTE.M")

class AnnualBrent(EIA):
    def __init__(self):
        super().__init__("PET.RBRTE.A")

# QUESTION: can class instance itself be Series object allowing: 
#    brent = DailyBrent()

# Need following wrapper class:
# brent = DailyBrent().series # df[df.columns[0]]
# df = DailyBrent().df     # get_saved_er()
# DailyBrent().update()
        
if __name__ == "__main__":
    
    brent = DailyBrent().series
    assert brent['2016-02-16'] == 31.09
    brent.to_csv('brent_daily.csv')
    
    
    # http://pandas.pydata.org/pandas-docs/stable/timeseries.html#resampling
    # Any function available via dispatching can be given to the how parameter by name, including 
    # sum, mean, std, sem, max, min, median, first, last, ohlc.
    # brent.resample('M', how = 'mean')
    # brent.resample('M', how = 'last')
    
    brent_a_avg = brent.resample('12M', how = 'mean')
    brent_q_avg = brent.resample('Q', how = 'mean')
    brent_m_avg = brent.resample('M', how = 'mean')

    # WARNING: labels with last day of month, irrespective of whether business day of nor, 
    #          information about last actual reported day in month is lost
    
    brent_a_eop = brent.resample('12M', how = 'last')
    brent_q_eop = brent.resample('Q', how = 'last')
    brent_m_eop = brent.resample('M', how = 'last')




    
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