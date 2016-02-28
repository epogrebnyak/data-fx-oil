""" Download Brent FOB price time series from EIA API. """

from urllib.request import urlopen
import json
import pandas as pd
import datetime

class _Getter():
    def __init__(self, url):
        self.z = self.get_restful_data(url)
    
    @staticmethod
    def get_restful_data(url):
        """Retrieves data from URL"""    
        with urlopen(url) as f:
            url_data = f.read() #.decode()
        return url_data

s = _Getter('http://www.google.com')
print(s.z)        