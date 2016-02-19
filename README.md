Data import and transormation
-----------------------------

### Assets

Existing data import: [eia.py](https://github.com/epogrebnyak/fx-oil/blob/master/eia.py) 
Some data transformation code in R: [import_data.R](https://github.com/epogrebnyak/fx-oil/blob/master/manual-grab/import_data.R)

###Todo

1 separate eia.py into code and (py.test) test (= functions with assert)  
2 demostrate import test is passing

3 store data in pandas Series object  
4 add simple test for pandas

5 transform data into period-average and end-of-period datapoint at annual, quarterly and monthly frequencies  
6 add tests checking transformation 

7 store two time series (period average and end-of-period price) in csv files as in 
 [rosstat-kep-data](https://github.com/epogrebnyak/rosstat-kep-data/tree/master/output) (responsible code is 
 [here](https://github.com/epogrebnyak/rosstat-kep-data/blob/master/kep/getter/dataframes.py#L131) )

8 demonstrate ability to generalise procedure to other tickers/commodities
