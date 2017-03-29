""" Download USD RUR exchange rate from Bank of Russia web site."""

import pandas as pd
import datetime
import requests
import xml.etree.ElementTree as ET

CSV_FILENAME = "cbr_er.txt"
ER_VARNAME = "USDRUR"
  
def _dt(s):
    return datetime.datetime.strptime(s,"%d.%m.%Y")

def yield_date_and_usdrur(url):
    r = requests.get(url)
    root = ET.fromstring(r.text)
    for child in root:
        date_as_string = child.attrib['Date']
        # starting 02.06.1993 there are values like "2 153,0000"
        value_as_string = child[1].text.replace(",",".").replace(chr(160),"")
        try:
            yield _dt(date_as_string), float(value_as_string)
        except:
            raise ValueError(value_as_string.__repr__()+" at date "+date_as_string.__repr__())    
           
def _fmt(dt):
    return dt.strftime('%d/%m/%Y')   

def make_date_range(start, end):
    #start date
    if start:
        s = _fmt(start)
    else:
        s = "01/07/1992"    
    #end date
    if end:    
        e = _fmt(end)
    else:
        e = _fmt(datetime.datetime.today())
    
    return s, e

def make_url(start=None, end=None):   
    s, e = make_date_range(start, end)
    URL = 'http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={0}&date_req2={1}&VAL_NM_RQ=R01235'
    return URL.format(s, e)

# TODO 1 - move asserts to tests   

# def test_make_url():    
#    start = datetime.date(2001,3,2)
#    end = datetime.date(2001,3,14)   
#    target_url = 'http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=02/03/2001&date_req2=14/03/2001&VAL_NM_RQ=R01235'
#    assert target_url ==  make_url(start, end)
   
def download_er():
    url = make_url()
    gen = yield_date_and_usdrur(url)
    _dicts = dict((pd.to_datetime(date), price) for date, price in gen)
    ts = pd.Series(_dicts, name = ER_VARNAME)
    #divide values before 1997-12-30 by 1000
    ix = ts.index <= "1997-12-30"
    ts.loc[ix] = ts[ix] / 1000
    return ts.round(4)

def save_to_csv(ts):
    ts.to_csv(CSV_FILENAME, header = True)

def get_saved_er():
    df = pd.read_csv(CSV_FILENAME, index_col = 0) 
    df.index = pd.to_datetime(df.index)
    return df[df.columns[0]].round(4)
    
def get_er():
    return get_saved_er()    

# TODO 2 - move asserts to tests   
   
#def update():
#    er = download_er()
#    assert er['1997-12-27'] == 5.95800 
#    save_to_csv(er)    
#    df = get_saved_er()
#    ts = df[df.columns[0]]
#    # note: had problems with rounding, er and ts are at this point rounded to 4 digits   
#    assert er.equals(ts)
#    return ts   
    

class Ruble():    
    
    def __init__(self):                
        try:
            self.ts = get_saved_er()
        except FileNotFoundError:
            print("Cannot load from local file, updating...")
            self.update()
      
    def update(self):
        self.ts = download_er()
        save_to_csv(self.ts)    
        return self
        
    def get(self):
        return self.ts    
    
    
if __name__ == "__main__":
    er = Ruble().get()
    print(er.tail())
    # Ruble().update()


# caching ---------------------------------------------------------------------

def update_xml():

    def to_file(fn, string):
        with open(fn, "w") as text_file:
            text_file.write(string)

    url = make_url(start=None, end=None)
    to_file("er_xml.txt", requests.get(url).text)

# -----------------------------------------------------------------------------