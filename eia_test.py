from eia import convert_to_date, parse, convert_to_pandas_series
import datetime

# this is a truncated version of http://api.eia.gov/series/?api_key=15C0821C54636C57209B84FEEE3CE654&series_id=PET.RBRTE.D
JSON_DOC = """{"request":{"command":"series","series_id":"PET.RBRTE.D"},
    "series":[{"series_id":"PET.RBRTE.D","name":"Europe Brent Spot Price FOB, Daily","units":"Dollars per Barrel","f":"D","unitsshort":"$\/bbl","description":"Europe Brent Spot Price FOB","copyright":"Thomson-Reuters","source":"Thomson-Reuters","start":"19870520","end":"20151201","updated":"2015-12-02T13:20:30-0500","data":[["20151201",42.97],["20151130",43.73],["20151127",43.07],["20151126",43.55],["20151125",43.56],["20151124",44.38],["20151123",43.7],["20151120",42.49],["20151119",42.22],["20151118",41.45],["20151117",41.28],["20151116",40.28],["20151113",41.98],["19870521",18.45],["19870520",18.63]]}]}"""

def raw_eia_brent_fob_local_copy(url_data = JSON_DOC):
    return parse(url_data)

def test_check_values_from_eia_brent_fob(list_):
    """Checks few entries *list_* """
    test_values =[["20151201",42.97], ["20151130",43.73], ["20151127",43.07]]
    for t in test_values:
       assert t in list_    
    print("Test passed OK.")

def test_iter():
    # urlopen() fails behind firewall, so I test only the XML/JSON parser
    # list_ = raw_eia_brent_fob()
    list_ = raw_eia_brent_fob_local_copy()
    test_check_values_from_eia_brent_fob(list_)

def convert_to_date_object_test():
    test_string = "20150115"
    date_object = datetime.date(2015,1,15)
    function_res = convert_to_date(test_string)

    assert date_object == function_res
    print("Test passed OK.")


if __name__ == "__main__":
    test_iter()
