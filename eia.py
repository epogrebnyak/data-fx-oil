""" Download Brent FOB price time series from EIA API. """

from urllib.request import urlopen
import json
import pandas
import datetime

SOURCE_URL = "http://api.eia.gov/series/?api_key=15C0821C54636C57209B84FEEE3CE654&series_id=PET.RBRTE.D"

PERIOD_MONTH = 'month'
PERIOD_YEAR = 'year'
PERIOD_QUARTER = 'quarter'

def get_restful_data(url = SOURCE_URL):
    with urlopen(url) as f:
        url_data = f.read().decode()
    return url_data 

def parse(url_data):
    """Returns a list of time series values from API output"""
    json_data = json.loads(url_data)    
    # NOTE: may also apply sorting here, because newest dates appear first in this list. 
    return json_data["series"][0]["data"]
    
def raw_eia_brent_fob():
    """Yeilds data data from EIA on Brent FOB Price retrieved from SOURCE_URL
       Passes test_iter()"""
    url_data = get_restful_data()
    return parse(url_data)

def convert_to_date(date_string):
    year = int(date_string[0:4])
    month = int(date_string[4:6])
    day = int(date_string[6:])
    return datetime.date(year, month, day)

def convert_to_pandas_series(raw_data):
    if not raw_data:
        raise ValueError("Invalid data parameter!")

    data_dict = {}
    for raw_data_item in raw_data:
        date_str = raw_data_item[0]
        date = convert_to_date(date_str)
        price = raw_data_item[1]

        data_dict[date] = price

    data_series = pandas.Series(data_dict)
    return data_series

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
#   For reference:
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
