library('BatchGetSymbols')

index = BatchGetSymbols(
  tickers = '^BVSP', 
  first.date = '2021-07-20',
  last.date = '2021-07-31', 
  bench.ticker = '^BVSP'
)

index = index$df.tickers
index