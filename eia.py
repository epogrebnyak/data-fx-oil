""" Download Brent FOB price time series from EIA API. """

from urllib.request import urlopen
import json
import pandas
import datetime

SOURCE_URL = "http://api.eia.gov/series/?api_key=15C0821C54636C57209B84FEEE3CE654&series_id=PET.RBRTE.D"

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

def convert_to_date(pair):
    """Convert date in "20150304" format to date python object"""
    date_string = pair[0]
    year = int(date_string[0:4])
    mounth = int(date_string[4:6])
    day = int(date_string[6:])
    return [datetime.date(year, mounth, day), pair[1]]


data_list = raw_eia_brent_fob()
data_list = list(map(convert_to_date, data_list))

data = pandas.Series(data_list)
print (data)
    

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
