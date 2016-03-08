""" Download USD RUR exchange rate from Bank of Russia web site."""

import json
import pandas as pd
import datetime
import requests
import xml.etree.ElementTree as ET

import os
import csv

CSV_FILENAME_SERIES = "er.txt"
ER_VARNAME = "CBR_USDRUR_DAILY"
CSV_FILENAME_DF = ER_VARNAME + ".txt"

  
def yield_date_and_usdrur(url):

    def dt(s):
       return datetime.datetime.strptime(s,"%d.%m.%Y")

    r = requests.get(url)
    root = ET.fromstring(r.text)
    for child in root:
        date_as_string = child.attrib['Date']
        # note: starting 02.06.1993 there are values like "2 153,0000"
        value_as_string = child[1].text.replace(",",".").replace(chr(160),"")
        try:
            yield dt(date_as_string), float(value_as_string)
        except:
            raise ValueError(value_as_string.__repr__()+" at date "+date_as_string.__repr__())    
           

def make_url(start=None, end=None):    
    URL = 'http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={0}&date_req2={1}&VAL_NM_RQ=R01235'

    def fmt(dt):
            return dt.strftime('%d/%m/%Y')
    
    if start:
        s = fmt(start)
    else:
        s = "01/07/1992"
    
    if end:    
        e = fmt(end)
    else:
        e = fmt(datetime.datetime.today())
        
    return URL.format(s, e)

    
def test_make_url():    
    start = datetime.date(2001,3,2)
    end = datetime.date(2001,3,14)   
    target_url = 'http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=02/03/2001&date_req2=14/03/2001&VAL_NM_RQ=R01235'
    assert target_url ==  make_url(start, end)

    
def as_series(flat_list, name_ = ER_VARNAME):
    data_dict = dict((pd.to_datetime(date), price) for date, price in iter(flat_list))
    return pd.Series(data_dict, name = name_)

    
def download_er():
    url = make_url(start=None, end=None)
    gen = yield_date_and_usdrur(url)
    ts = as_series(gen)
    try:
       #divide values before 1997-12-30 by 1000
       ix = ts.index < "1997-12-30"
       ts[ix] = round(ts[ix] / 1000, 4)
    except:
       pass  
    return ts.round(4)

    
def update_xml():

    def to_file(fn, string):
        with open(fn, "w") as text_file:
            text_file.write(string)

    url = make_url(start=None, end=None)
    to_file("er_xml.txt", requests.get(url).text)

    
def update_csv(ts):
    # two csv files will be identical
    ts.to_csv(CSV_FILENAME_SERIES, header = True)
    df = pd.DataFrame(ts)
    df.to_csv(CSV_FILENAME_DF)


def get_saved_er():
    df = pd.read_csv(CSV_FILENAME_DF, index_col = 0) 
    df.index = pd.to_datetime(df.index)
    return df.round(4)

    
def get_er():
    return get_saved_er()
    
    
def update():
    er = download_er()
    update_csv(er)    
    update_xml()
    df = get_saved_er()
    ts = df[df.columns[0]]
    # note: had problems with rounding, er and ts are at this point rounded to 4 digits   
    assert er.equals(ts)

    
# Need following wrapper class:
# er = CBR_USDRUR().series # df[df.columns[0]]
# df = CBR_USDRUR().df     # get_saved_er()
# CBR_USDRUR().update()
