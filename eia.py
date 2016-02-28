""" Download Brent FOB price time series from EIA API. """

from urllib.request import urlopen
import json
import pandas as pd
import datetime

ACCESS_KEY = "15C0821C54636C57209B84FEEE3CE654"

def string_to_date(date_string):
    return datetime.datetime.strptime(date_string, "%Y%m%d").date() 
assert string_to_date("20150115") == datetime.date(2015,1,15)
    
class EIA():
    
    def __init__(self, id):
       self.url = self.series_url(id)
       raw_data = self.get_restful_data(self.url)
       flat_list = self.parse_json(raw_data)
       self.Series = self.as_series(flat_list)        
    
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
        
               
def get_daily_brent():
    return EIA("PET.RBRTE.D").Series
    
if __name__ == "__main__":
    
    s = EIA("PET.RBRTE.D").Series
    #print(s.Series)
    
    BRENT_URL = "http://api.eia.gov/series/?api_key=15C0821C54636C57209B84FEEE3CE654&series_id=PET.RBRTE.D"
    assert EIA("PET.RBRTE.D").url == BRENT_URL    

    assert string_to_date("20150115") == datetime.date(2015,1,15)    
    
    # todo: write some key asserts from eia_test.py here, they should address functions above (issue #5, #6)
    
    
    
    #daily_brent = get_daily_brent()
    assert s['2016-02-16'] == 31.09
    # todo: write expressions for variables below (issue #7), do not make functions yet
    # Note: PET.RBRTE.A and PET.RBRTE.M can be used for testing transformations of PET.RBRTE.D

    
    # brent_a_eop = 
    # brent_q_eop = 
    # brent_m_eop = 
    
    # brent_a_avg = 
    # brent_q_avg = 
    # brent_m_avg = 
    
    

    PERIOD_MONTH = 'month'
    PERIOD_YEAR = 'year'
    PERIOD_QUARTER = 'quarter'

        
    def eia_brent_fob_period_average(data, period):
        d_frame = pandas.DataFrame({'brent fob': data})
        d_frame.index = pandas.DatetimeIndex(d_frame.index)

        if period == PERIOD_MONTH:
            d_frame = d_frame.resample('M')
            d_frame = d_frame.set_index(d_frame.index.to_period('M'))
            d_frame.to_csv('monthly_average.csv', index_label='month')
        elif period == PERIOD_YEAR:
            d_frame = d_frame.resample('12M')
            d_frame = d_frame.set_index(d_frame.index.year)
            d_frame.to_csv('yearly_average.csv', index_label='year')
        elif period == PERIOD_QUARTER:
            d_frame = d_frame.resample('Q')
            d_frame = d_frame.set_index(d_frame.index.to_period('M'))
            d_frame.to_csv('quarter_average.csv', index_label='quarter')
        else:
            raise ValueError("The period parameter should be 'month', 'year' or 'quarter'")

        return d_frame
        
        
    
    
    
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
