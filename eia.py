""" Download Brent FOB price time series from EIA API. """


# this is a truncated version of http://api.eia.gov/series/?api_key=15C0821C54636C57209B84FEEE3CE654&series_id=PET.RBRTE.D
xml_doc = """{"request":{"command":"series","series_id":"PET.RBRTE.D"},"series":[{"series_id":"PET.RBRTE.D","name":"Europe Brent Spot Price FOB, Daily","units":"Dollars per Barrel","f":"D","unitsshort":"$\/bbl","description":"Europe Brent Spot Price FOB","copyright":"Thomson-Reuters","source":"Thomson-Reuters","start":"19870520","end":"20151201","updated":"2015-12-02T13:20:30-0500",
"data":[["20151201",42.97],["20151130",43.73],["20151127",43.07],["20151126",43.55],["20151125",43.56],["20151124",44.38],["20151123",43.7],["20151120",42.49],["20151119",42.22],["20151118",41.45],["20151117",41.28],["20151116",40.28],["20151113",41.98],["19870521",18.45],["19870520",18.63]]}]}"""

# source: http://www.diveintopython3.net/xml.html
# import xml.etree.ElementTree as etree
# tree = etree.parse('examples/feed.xml')
# root = tree.getroot()
# root

SOURCE_URL = "http://api.eia.gov/series/?api_key=15C0821C54636C57209B84FEEE3CE654&series_id=PET.RBRTE.D"

def iter_raw_eia_brent_fob():
    # TODO: this function must return data from EIA on Brent FOB Price, retrieved from SOURCE_URL 
    #       result must pass test_iter()
    
    # Download data from SOURCE_URL to xml_doc
    # 
    
    # Parse xml_doc and emit values 
    # ...
    
    # stub
    yield ("20151201",42.97)
    yield ("20151130",43.73)    
    yield ("20151127",43.07)
    
def test_iter():
    gen = iter_raw_eia_brent_fob()
    test_dict = dict((x[0],x[1]) for x in gen)
    assert test_dict["20151201"] == 42.97
    assert test_dict["20151130"] == 43.73
    assert test_dict["20151127"] == 43.07
    
if __name__ == "__main__":
    test_iter()
