# Importing RUR/USD and oil price data from Quandl.com
# 14:25 16.04.2015
#
# Problems:
# 1. ????????? ????? ???? ????? ????????????
# 2. ????????????? ???????? ???? ????? 
# 3. ??????????? ????? ??????????? ???????? - ???????????? ????????? ?????, ??????? ??? ? ?????-?? ?? ?????. (merged.data.frame)
#
#
# Prototype from:
# http://stackoverflow.com/questions/3507744/downloading-yahoo-stock-prices-in-r/3512562#3512562
# URL <- "http://ichart.finance.yahoo.com/table.csv?s=SPY"
# dat <- read.csv(URL)
# dat$Date <- as.Date(dat$Date, "%Y-%m-%d")
#
# See als? https://rpubs.com/irom/oil_vs_usrub
#
# Quandl.com API exmaple: https://www.quandl.com/api/v1/datasets/WIKI/AAPL.csv?sort_order=asc&exclude_headers=true&rows=3&trim_start=2012-11-01&trim_end=2013-11-30&column=4&collapse=quarterly&transformation=rdiff
# 



get_url = function(code, start_date, rows = -1, column = -1)
   # Create valid Quandl URL based on variable ticker (code) and time series start date.  
   {
   AUTH_TOKEN = "2_es4C5SXp2UHyCxxFix"
   BASE_URL = "http://www.quandl.com/api/v1/datasets/"

   if (rows == -1) {date_arg = paste0("trim_start=", start_date)}
   else            {date_arg = paste0("rows=", rows)}

   if (column == -1) {col_arg = ""}
   else              {col_arg = paste0("&column=", column)}

   url =  paste0(BASE_URL, code, ".csv?"
                 , date_arg 
                 , col_arg
                 , "&auth_token=", AUTH_TOKEN)
   return(url)
   };

get_csv = function(code, start_date, rows = -1, column = -1)
   # Retrieve variable from Quandl using its code 
    {
    url = get_url(code, start_date, rows, column) 
    dat = read.csv(url) 
    return(dat)
    };

start_date   = "1996-01-01"
er_code      = "CURRFX/USDRUB" #https://www.quandl.com/data/CURRFX/USDRUB-Currency-Exchange-Rates-USD-vs-RUB
brent_code_0 = "OFDP/FUTURE_B1"
brent_code_1 = "FRED/DCOILBRENTEU"
brent_code_2 = "SCF/ICE_B1_FW"
brent_code_3 = "ICE/BH2015"
brent_code_4 = "ICE/BG2015"
opec = "OPEC/ORB"

wtimonthly = "ODA/POILWTI_USD"
wtidaily = "DOE/RWTC"   #https://www.quandl.com/data/DOE/RWTC-WTI-Crude-Oil-Spot-Price-Cushing-OK-FOB
# https://www.quandl.com/c/futures/ice-brent-crude-oil-futures

er = get_csv(er_code, start_date, column = 1)
head(er)

brent = get_csv(brent_code_2, start_date, column = 4)
head(brent)

brent0 = get_csv(brent_code_0, start_date, column = 4)
brent1 = get_csv(brent_code_1, start_date)
brent2 = get_csv(brent_code_2, start_date, column = 4)
brent3 = get_csv(brent_code_3, start_date, column = 4)
brent4 = get_csv(brent_code_4, start_date, column = 4)
opec = get_csv(opec, start_date)
wtid = get_csv(wtidaily, start_date)
  
list.of.data.frames = list(brent0, brent1, brent2, brent3, brent4, opec)
merged.data.frame = Reduce(function(...) merge(..., by= "Date",  all=T), list.of.data.frames)
head(merged.data.frame)
tail(merged.data.frame)

#export to excel
q<-merge(er, wtid)
#library(xlsx)
#write.xlsx(q,  "/Users/Alex/Desktop/daily.xlsx")

# export to Stata 
#library(foreign)
#q<-merge(er, brent1)
#write.dta(q,  "/Users/Alex/Desktop/daily.dta")
