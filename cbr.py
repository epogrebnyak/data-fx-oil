""" Download Brent FOB price time series from EIA API. """

from urllib.request import urlopen
import json
import pandas as pd
import datetime
import requests
import xml.etree.ElementTree as ET

def num(s):
   return float(s.replace(",","."))

   
def dt(s):
   return datetime.datetime.strptime(s,"%d.%m.%Y")


def yield_from_xml(root):   
    for child in root:
        yield (dt(child.attrib['Date']), num(child[1].text))


def yield_usdrur():
   r = requests.get('http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=02/03/2001&date_req2=14/03/2001&VAL_NM_RQ=R01235')
   root = ET.fromstring(r.text)
   return yield_from_xml(root)


def make_url(dt1, dt2):
    URL = 'http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={0}&date_req2={1}&VAL_NM_RQ=R01235'
    s = dt1.strftime('%d/%m/%Y')
    e = dt2.strftime('%d/%m/%Y')
    return URL.format(s, e)

    
start = datetime.date(2001,3,2)
end = datetime.date(2001,3,14)   
target_url = 'http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=02/03/2001&date_req2=14/03/2001&VAL_NM_RQ=R01235'
assert target_url ==  make_url(start, end)


def as_series(flat_list):
    data_dict = dict((pd.to_datetime(date), price) for date, price in iter(flat_list))
    return pd.Series(data_dict)
    
er = as_series(yield_usdrur())        
print(er)