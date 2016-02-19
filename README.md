Data import and transormation
-----------------------------

Existing data import: [eia.py](https://github.com/epogrebnyak/fx-oil/blob/master/eia.py)
Some data transformation code in R: [import_data.R](https://github.com/epogrebnyak/fx-oil/blob/master/manual-grab/import_data.R)

Todo:
0. separate eia.py into code and (py.test) test (= functions with assert)
0. demostrate import test is passing

0. store data in pandas Series object 
0. add simple test for pandas

0. transform data into period-average and end-of-period datapoint at annual, quarterly and monthly frequencies
0. add tests checking transformation 

0. store two time series (period average and end-of-period price) in csv files as in 
 [rosstat-kep-data](https://github.com/epogrebnyak/rosstat-kep-data/tree/master/output) (responsible code is 
 [here](https://github.com/epogrebnyak/rosstat-kep-data/blob/master/kep/getter/dataframes.py#L131) )

0. demonstrate ability to generalise procedure to other tickers/commodities
