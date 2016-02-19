library(zoo)

parse_brent_ice = function(filename1)
	{
	data = read.table(filename1, skip = 0 , sep = "\t", header = TRUE, dec = ",", 
    	                             colClasses = "character")
	Sys.setlocale("LC_TIME", "US")

	dates = as.Date(data[,1], format="%B %d, %Y")
	val = as.numeric(data[,2])

	Sys.setlocale("LC_TIME", "Russian")

	exclude = duplicated(dates)

	ts1 <- zoo(val[!exclude], dates[!exclude])

	return(ts1)
	}

parse_brent_finam = function(filename1)
	{
	data = read.table(filename1, skip = 0 , sep = ",", header = TRUE, dec = ".", 
       colClasses = "character")

	dates = as.Date(data[,3], format="%Y%m%d")
	val = as.numeric(data[,5])

	brent <- zoo(val, dates)

	return(brent)
	}



parse_er_rur_usd_cbr = function(filename1)
	{
	data = read.table(filename1, sep = "\t", header = TRUE, dec = ",")

	dates = as.Date(data[,1], format="%d.%m.%Y")
	val = data[,3] 	
	er <- zoo(val, dates)

	# Divide by 1000 before denomination 
		denom_date = as.Date("30.12.1997", format="%d.%m.%Y")
		index_subset = which(time(er)<=denom_date)
		er[index_subset] = er[index_subset] / 1000
	
	return(er)
}



################################## Functions below not used



parse.er_rur_eur = function(filename1)
	{
	data = read.table(filename1, sep = " ", header = TRUE, dec = ",")

	dates = as.Date(data[,1], format="%d.%m.%Y")
	val = data[,3] 	
	er <- zoo(val, dates)

	# Divide by 1000 before denomination 
		denom_date = as.Date("30.12.1997", format="%d.%m.%Y")
		index_subset = which(time(er)<=denom_date)
		er[index_subset] = er[index_subset] / 1000
	
	return(er)
}

parse.ir_cb_deposit = function(filename1)
	{

	data = read.table(filename1, sep = " ", header = FALSE, dec = ",", colClasses="character")

	dates = as.Date(data[,1], format="%d.%m.%Y")
	val = as.numeric(gsub(",", ".", data[,3])) 

	cb.deposit <- zoo(val, dates)

	start_date = as.Date("2005-01-11")
	end_date = time(cb.deposit)[length(cb.deposit)]

	plotline = window(cb.deposit, start = start_date, end = end_date)
	
	return(plotline)
}

parse.m_cb_deposit = function(filename1)
	{
	data = read.table(filename1, sep = " ", header = TRUE, dec = ",")

	dates = as.Date(data[,1], format="%d.%m.%Y")
	val = data[,2] 	
	m <- zoo(val, dates)

	return(m)
}

parse.ir_libor_on_usd = function(filename1)
	{
	data = read.table(filename1, sep = "\t", header = TRUE, dec = ",", colClasses = "character")

	dates = as.Date(data[,1], format="%Y-%m-%d")
	val = as.numeric(gsub(",", ".", data[,2]))

	libor <- zoo(val, dates)

	libor = libor[which(!is.na(libor))]

	return(libor)
}


parse.ir_mosprime_on = function(filename1)
	{
	data = read.table(filename1, sep = " ", header = FALSE, dec = ".")

	dates = as.Date(data[,2], format="%d-%m-%Y")
	val = as.numeric(data[,3]) 

	mosprime <- zoo(val, dates)

	mosprime = mosprime[which(!time(mosprime)==as.Date("30-12-2011", format="%d-%m-%Y"))]

	return(mosprime)
}

parse.m_bank_liq = function(filename1)
	{

	data = read.table(filename1, sep = "\t", skip = 1, header = FALSE, dec = ",")

	dates = as.Date(data[,1], format="%d.%m.%Y")
	val = data[,2] 

	liq <- zoo(val, dates)

	return(liq)

	}




