""" Download Brent FOB price time series from EIA API. """

from urllib.request import urlopen
import json
import pandas as pd
import datetime

import requests
r = requests.get('http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=02/03/2001&date_req2=14/03/2001&VAL_NM_RQ=R01235')

import xml.etree.ElementTree as ET
root = ET.fromstring(r.text)

def num(s):
   return float(s.replace(",","."))
   
def dt(s):
   return datetime.datetime.strptime(s,"%d.%m.%Y")

def yield_date_usd():   
    for child in root:
        yield (child.attrib['Date'], num(child[1].text))

print(list(yield_date_usd()))