""" Download Brent FOB price time series from EIA API. """

from urllib.request import urlopen
import json
import pandas
import datetime

BRENT_URL = "http://api.eia.gov/series/?api_key=15C0821C54636C57209B84FEEE3CE654&series_id=PET.RBRTE.D"

def get_restful_data(url):
    """Retrieves data from URL"""
    with urlopen(url) as f:
        url_data = f.read().decode()
    return url_data 

def parse(url_data):
    """Returns a list of time series values from API output"""
    json_data = json.loads(url_data)    
    return json_data["series"][0]["data"]
    
def raw_eia_brent_fob():
    """Yeilds data data from EIA on Brent FOB Price retrieved from BRENT_URL"""    
    url_data = get_restful_data(BRENT_URL)
    return parse(url_data)

def string_to_date(date_string):
    # string_to_date("20150115") == datetime.date(2015,1,15)    
    return datetime.datetime.strptime(date_string, "%Y%m%d").date()    

def yield_tuples(flat_list):
    for row in flat_list:
        date = string_to_date(row[0])
        price = row[1]
        yield date, price
    
def as_series(flat_list):
    # maybe there is shorter notation for unpacking below 
    data_dict = dict((date, price) for date, price in yield_tuples(flat_list))
    return pandas.Series(data_dict)  

def get_brent():
    return as_series(raw_eia_brent_fob())
    
if __name__ == "__main__":    
    assert string_to_date("20150115") == datetime.date(2015,1,15)    
    # todo: write some key asserts from eia_test.py here, they should address functions above (issue #5,6)
    
    brent = get_brent()
    
    
    # todo: write expressions for variables below (issue #7), do not make functions yet
    
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
        
        
    
    
    
# ----------------------------
#   JSON output reference
# ----------------------------

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
