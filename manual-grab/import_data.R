# Import fx and oil data from screen-grab text files
#
# Requirements:
# (1) data files should be in var_name/var_name.txt
# 

# Use zoo library for time series
    library(zoo)
	
# Set root directory 
    # dir.root = "/Users/Alex/Dropbox/Exchange rates/Скачка данных/work-fx-oil/manual-screen-grab"
    dir.root = "D:\\work-fx-oil\\manual-screen-grab\\" 
    dir.data = dir.root 
               # paste0(dir.root,"data\\") 

# Access data transformation functions
    setwd(dir.root)
    source("f_mold.r")
    source("f_parse_functions.r")

get_var_from_file = function(var_name)
    # Retrieve time series using variable filename
    {
    parse_function = get(paste0("parse_", var_name))
    fn = paste0(var_name, ".txt")
    source_file = file.path(dir.data, var_name, fn)     
    assign(var_name, parse_function(source_file))
    return(get(var_name))
    # maybe 'return()' if var_name is assigned to global namespace
}

brent_ice   = get_var_from_file("brent_ice")
brent_finam = get_var_from_file("brent_finam")
er_cbr      = get_var_from_file("er_rur_usd_cbr")

# head(brent_ice)
head(brent_finam)
head(er_cbr)

# tail(brent_ice)
tail(brent_finam)
tail(er_cbr)

frame = merge(brent_finam, er_cbr, all = FALSE)

rn = as.Date(time(frame), format = '%Y-%m-%d')
write.csv(frame, "zoo.csv", row.names = rn)

write.table(data.frame(frame), file = "zoo.txt", row.names = T, sep = "\t", dec = ",", quote = F)