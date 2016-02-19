# ‘ункции дл€ обработки ежедневных временных р€дов
# 15:20 16.04.2015

# ¬спомогательна€ функци€ дл€ получени€ года как числа из метки времени временного р€да
year = function(x){as.numeric(format(time(x), format = "%Y"))}


month.frame = function(x)
# ‘ункци€ дл€ получени€ сводной статистики в мес€чном разрезе 
# јргемент x - временной р€д

   {
	x1 = round(mold(x,period = "m", position =  "start"), 2)
	x2 = round(mold(x,period = "m", position =  "all",    using.function = "mean"), 2)
	x3 = round(mold(x,period = "m", position =  "end"),   2)

	year = as.numeric(time(x1) %/% 1) 			        # %/% - разделить нацело 
	month = round(12 * (as.numeric(time(x1) %% 1)),0)+1 # %% - остаток от делени€

	date = paste("1",month,year,sep="-")
	date = as.Date(date, "%d-%m-%Y")

	# запишем что получилось в фрейм (с датами)
		w = data.frame(date,year,month,x1,x2,x3)
		colnames(w)[4:6] = c("start", "mean", "end")
		
	# используем обратный пор€док дат, самое новое сверху
		w = w[dim(w)[1]:1,]

	return(w)
}

mold = function(ts, period = "m", position =  "all", using.function = "mean")
# Aggregate time series accoring to period (a, q, or m - annual, quarterly 
# and monthly), observation position (all, start , end) and function (mean, max, min, sd)

{
	# Use zoo library for time series
	library(zoo)
	freq = c(1,4,12)

	# здесь определ€етс€ временна€ шкала данных дл€ агрегировани€ 
	an.1 = c("y", "q", "m")
	period.choice = which(an.1 == period)
	aggregate.by = switch(period.choice,
		year(ts), 
		as.yearqtr(time(ts)),
		as.yearmon(time(ts))   )

	# здесь из временной шкалы выбираютс€ первые или последний метки по периодам, в зависимости от выбора
	# или оставл€ютс€ все метки
	an.2 = c("all", "start", "end")
	subset.index = switch (which (an.2 == position),
		aggregate.by == aggregate.by, # all TRUE
		!duplicated(aggregate.by),
		!duplicated(aggregate.by, fromLast = TRUE) )

	# по индексу subset.index урезаетс€ и ts и aggregate.by 
	aggregate.by = aggregate.by[subset.index]
	ts = ts[subset.index]

	# вызываетс€ функци€ агрегировани€
	s = aggregate(ts, aggregate.by, FUN = using.function)
	# aggregated = as.numeric(aggregate(ts, aggregate.by, FUN = using.function))

	# переводим числовой р€д обратно в тип ts
	# немного разный синтаксис дл€ года и дл€ других частот
	# start.val = switch (period.choice, start.year, c(start.year, start.qtr), c(start.year, start.month))
	# s = ts(aggregated, start = start.val, frequency = freq[period.choice])
		
	return(s)

}

