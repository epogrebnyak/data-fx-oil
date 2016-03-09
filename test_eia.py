#from urllib.request import urlopen
#import json
import pandas as pd
import datetime

import eia

def test_string_to_date():
    assert eia.__string_to_date__("20150115", "%Y%m%d") == datetime.date(2015,1,15)
    
def test_url():
    BRENT_URL = "http://api.eia.gov/series/?api_key=15C0821C54636C57209B84FEEE3CE654&series_id=PET.RBRTE.D"
    assert eia.EIA("PET.RBRTE.D").url == BRENT_URL   

def test_single_value():
    brent = eia.Brent().series
    assert brent['2016-02-16'] == 31.09
   
# this is a truncated version of http://api.eia.gov/series/?api_key=15C0821C54636C57209B84FEEE3CE654&series_id=PET.RBRTE.D
JSON_DOC = """{"request":{"command":"series","series_id":"PET.RBRTE.D"},
    "series":[{"series_id":"PET.RBRTE.D","name":"Europe Brent Spot Price FOB, Daily","units":"Dollars per Barrel","f":"D","unitsshort":"$\/bbl","description":"Europe Brent Spot Price FOB","copyright":"Thomson-Reuters","source":"Thomson-Reuters","start":"19870520","end":"20151201","updated":"2015-12-02T13:20:30-0500","data":[["20151201",42.97],["20151130",43.73],["20151127",43.07],["20151126",43.55],["20151125",43.56],["20151124",44.38],["20151123",43.7],["20151120",42.49],["20151119",42.22],["20151118",41.45],["20151117",41.28],["20151116",40.28],["20151113",41.98],["19870521",18.45],["19870520",18.63]]}]}"""

# Test values for the hardcoded JSON_DOC data
TEST_VALUES = [["20151201",42.97], ["20151130",43.73], ["20151127",43.07]]

# TODO: 
# must test TEST_VALUES are in JSON_DOC