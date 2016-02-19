from eia import *
import datetime
import pytest

# this is a truncated version of http://api.eia.gov/series/?api_key=15C0821C54636C57209B84FEEE3CE654&series_id=PET.RBRTE.D
JSON_DOC = """{"request":{"command":"series","series_id":"PET.RBRTE.D"},
    "series":[{"series_id":"PET.RBRTE.D","name":"Europe Brent Spot Price FOB, Daily","units":"Dollars per Barrel","f":"D","unitsshort":"$\/bbl","description":"Europe Brent Spot Price FOB","copyright":"Thomson-Reuters","source":"Thomson-Reuters","start":"19870520","end":"20151201","updated":"2015-12-02T13:20:30-0500","data":[["20151201",42.97],["20151130",43.73],["20151127",43.07],["20151126",43.55],["20151125",43.56],["20151124",44.38],["20151123",43.7],["20151120",42.49],["20151119",42.22],["20151118",41.45],["20151117",41.28],["20151116",40.28],["20151113",41.98],["19870521",18.45],["19870520",18.63]]}]}"""

# Test values for the hardcoded JSON_DOC data
TEST_VALUES = [["20151201",42.97], ["20151130",43.73], ["20151127",43.07]]

# Test values known to exist in the Brent FOB data 
REST_VALUES = [["19890907",17.8], ["20080312",107.99], ["20120330",123.41]] 

@pytest.fixture
def hardcoded_data():
    return raw_eia_brent_fob_local_copy()

@pytest.fixture
def eia_brent_fob_data():
    return raw_eia_brent_fob()

def raw_eia_brent_fob_local_copy(url_data = JSON_DOC):
    return parse(url_data)

def check_values_from_eia_brent_fob(list_):
    """Checks few entries *list_* """
    for t in TEST_VALUES:
       assert t in list_   
    print("Test passed OK.")

def test_iter(hardcoded_data):
    # urlopen() fails behind firewall, so I test only the XML/JSON parser
    # list_ = raw_eia_brent_fob()
    check_values_from_eia_brent_fob(hardcoded_data)

def test_convert_to_date_object():
    test_string = "20150115"
    date_object = datetime.date(2015,1,15)
    function_res = convert_to_date(test_string)

    assert date_object == function_res
    print("Test passed OK.")

def test_convert_to_pandas_series_hardcoded(hardcoded_data):
    """Tests the conversion of the hardcoded json data to pandas series."""
    series_data = convert_to_pandas_series(hardcoded_data)
    # check if the date strings from TEST_VALUES are in the index list of the series.
    for test_val in TEST_VALUES:
        assert convert_to_date(test_val[0]) in series_data.index

def test_convert_to_pandas_series_restful(eia_brent_fob_data):
    """Tests the conversion of the restful data retreived from the internet."""
    series_data = convert_to_pandas_series(eia_brent_fob_data)
    for test_val in REST_VALUES:
        assert convert_to_date(test_val[0]) in series_data.index

def test_convert_to_pandas_series_param_none():
    with pytest.raises(ValueError):
        convert_to_pandas_series(None)

def test_eia_brent_fob_period_average(hardcoded_data):
    eia_brent_fob_series = convert_to_pandas_series(hardcoded_data)
    assert eia_brent_fob_period_average(eia_brent_fob_series, PERIOD_YEAR).iloc[0,0] == 18.54
    assert eia_brent_fob_period_average(eia_brent_fob_series, PERIOD_MONTH)[-1:].iloc[0,0] == 42.97
    assert eia_brent_fob_period_average(eia_brent_fob_series, PERIOD_QUARTER).iloc[0,0] == 18.54

def test_eia_brent_fob_period_average_invalid_period():
    with pytest.raises(ValueError):
        eia_brent_fob_period_average(None, 'invalid period label')

if __name__ == "__main__":
    convert_to_date_object_test()
    test_iter()
