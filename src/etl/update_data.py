from etl.catch_clean import DownloadFilesBrGov

# Download data form Brazilian Government services
download = DownloadFilesBrGov()
download.series_central_bank()
download.series_ibge()
