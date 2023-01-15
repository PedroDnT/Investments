# Set local directory
setwd('/home/marcos/Documents/Investments/src')

# Install library
#install.packages("rvest")
#install.packages("plyr")
#install.packages("dplyr")
#install.packages("BatchGetSymbols")

# Import library
library(rvest)
library(plyr)
library(dplyr)
library(BatchGetSymbols)

ibov = function(initial_date='2021-01-01', final_date=Sys.Date(), benchmark='^BVSP'){
    
    # Capturing the IBOV indexes on the current date
    indices=GetIbovStocks()
    # Generating the column tickersSA
    indices$tickersSA = paste(indices$tickers, '.SA', sep = '')
    # Downloading the stock time series from the IBOV index
    data_ibov = BatchGetSymbols(tickers = indices$tickersSA, first.date = initial_date,
                                last.date = final_date, bench.ticker = benchmark)
    # Selecting the data of interest in DataFrame df.tickers
    data_ibov = data_ibov$df.tickers
    # Generating a list for each index
    data_ibov2 = dlply(data_ibov, .(ticker), function(x) {rownames(x) = x$row; 
                        x$row = NULL;x})
    # Creating a DataFrame with the First Action and Date and Price Adjusted Columns
    stocks = data_ibov2[[1]][,c(7,6)]
    # Renaming the columns
    colnames(stocks) = c('date', paste('', data_ibov2[[1]][1,8]))
    # Adding the others stocks to the DataFrame
    for(i in 2:length(data_ibov2)) {
        new_stocks = data_ibov2[[i]][,c(7,6)]
        colnames(new_stocks) = c('date', paste('', data_ibov2[[i]][1,8]))
        stocks = merge(stocks, new_stocks, by = 'date')
    }
    # Generating a csv file with the final DataFrame
    return(write.table(stocks, '../data/ibov.csv', sep=','))
}

tickers = function(){
    ibov = GetIbovStocks()
    ibov = data.frame(ibov$tickers)
    ibov$ibov.tickers = paste(ibov$ibov.tickers, '.SA', sep = '')
    colnames(ibov) = c('tickers')
    return(write.table(ibov, '../data/ibov_tickers.csv', row.names = FALSE))
  
}
   
ibov()
#tickers()
