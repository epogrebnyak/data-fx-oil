# ----------------------------
#   Data sample:
# ----------------------------

# this is a truncated version of http://api.eia.gov/series/?api_key=15C0821C54636C57209B84FEEE3CE654&series_id=PET.RBRTE.D
XML_DOC = """{"request":{"command":"series","series_id":"PET.RBRTE.D"},
"series":[{"series_id":"PET.RBRTE.D","name":"Europe Brent Spot Price FOB, Daily","units":"Dollars per Barrel","f":"D","unitsshort":"$\/bbl","description":"Europe Brent Spot Price FOB","copyright":"Thomson-Reuters","source":"Thomson-Reuters","start":"19870520","end":"20151201","updated":"2015-12-02T13:20:30-0500","data":[["20151201",42.97],["20151130",43.73],["20151127",43.07],["20151126",43.55],["20151125",43.56],["20151124",44.38],["20151123",43.7],["20151120",42.49],["20151119",42.22],["20151118",41.45],["20151117",41.28],["20151116",40.28],["20151113",41.98],["19870521",18.45],["19870520",18.63]]}]}"""

# ----------------------------
#   Code:
# ----------------------------

""" Download Brent FOB price time series from EIA API. """

from urllib.request import urlopen
import json

SOURCE_URL = "http://api.eia.gov/series/?api_key=15C0821C54636C57209B84FEEE3CE654&series_id=PET.RBRTE.D"

def get_restful_data(url = SOURCE_URL):
    # Download data from SOURCE_URL 
    with urlopen(url) as f:
        url_data = f.read().decode()
    return url_data 

def parse(url_data):
    """Returns a list of time series values from API output"""
    # NOTE: may also use lxml or xmltodict for parsing
    json_data = json.loads(url_data)    
    # NOTE: may also apply sorting here, because newest dates appear first in this list. 
    return json_data["series"][0]["data"]
    
def raw_eia_brent_fob():
    """Yeilds data data from EIA on Brent FOB Price retrieved from SOURCE_URL
       Passes test_iter()"""
    url_data = get_restful_data()
    return parse(url_data)
   
# ----------------------------
#   Testing:
# ----------------------------   

def raw_eia_brent_fob_local_copy(url_data = XML_DOC):
    return parse(url_data)
    
def check_values_from_eia_brent_fob(list_):
    """Checks few entries *list_* """
    test_values =[["20151201",42.97], ["20151130",43.73], ["20151127",43.07]]
    for t in test_values:
       assert t in list_    
    print("Test passed OK.")    
    
def test_iter():
    # urlopen() fails behind firewall, so I test only the XML/JSON parser
    # list_ = raw_eia_brent_fob()
    list_ = raw_eia_brent_fob_local_copy()
    check_values_from_eia_brent_fob(list_)
    
if __name__ == "__main__":
    test_iter()
    

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
