setwd('/home/marcos/Documents/Projetos/Investimentos/src')
library(rvest)
library(plyr)
library(dplyr)
library(BatchGetSymbols)

ibov = function(data_inicial='2015-01-01', data_final=Sys.Date(), benchmark='^BVSP'){
    
    # Capturando os índices IBOV na data atual
    indices=GetIbovStocks()
    # Gerando a coluna tickersSA
    indices$tickersSA = paste(indices$tickers, '.SA', sep = '')
    # Baixando a série temporal das ações do índice IBOV
    dados_ibov = BatchGetSymbols(tickers = indices$tickersSA, first.date = data_inicial,
                                last.date = data_final, bench.ticker = benchmark)
    # Selecionando os dados de interesse no DataFrame df.tickers
    dados_ibov = dados_ibov$df.tickers
    # Gerando uma lista para cada índice
    dados_ibov2 = dlply(dados_ibov, .(ticker), function(x) {rownames(x) = x$row; 
                        x$row = NULL;x})
    # Gerando um DataFrame com a primeira ação e as colunas de data e preço ajustado
    acao = dados_ibov2[[1]][,c(7,6)]
    # Renomeando as colunas
    colnames(acao) = c('data', paste('Preço', dados_ibov2[[1]][1,8]))
    # Adicionando as demais ações ao DataFrame
    for(i in 2:length(dados_ibov2)) {
        novaacao = dados_ibov2[[i]][,c(7,6)]
        colnames(novaacao) = c('data', paste('Preço', dados_ibov2[[i]][1,8]))
        acao = merge(acao, novaacao, by = 'data')
    }
    # Gerando um arquivo csv com o DataFrame final
    return(write.table(acao, '../dados/ibov.csv', sep=','))
}

ibov()
