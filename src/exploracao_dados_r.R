# Instalando pacotes
install.packages('corrplot')
# Pacotes adicionais
library(rvest)
library(plyr)
library(dplyr)
library(xts)
library(zoo)

# Importando pacotes
library(BatchGetSymbols)
library(quantmod)
library(GetDFPData2)
library(ggplot2)
library(ggthemes)
library(reshape2)
library(corrplot)

# Parâmtros para captura das ações nacionais
# Dia inicial
di = '2021-01-01' 
# Dia final
df = Sys.Date()
# Indicador, ticket
benchmark = '^BVSP'

# Baixando todas as ações do índice IBOV
# Será retornado um DataFrame com a cotação da ação no dia dos principais 
# índices relacionados na bolsa de valores de São Paulo
# O objetivo é capturar o ticket de cada ação para baixar os histórico (serie)
# das empresas listadas no índice IBOV
ibov = GetIbovStocks()

# Criando uma coluna concatenando a coluna tickers ao texto .SA
# Com essa nova coluna é possível capturar os preços de todas as ações no índice
# ibov
ibov$tickersSA = paste(ibov$tickers, '.SA', sep = '')

# Baixando todas as ações do índice IBOV
# tickers: Coluna tickersSA no DataFrame ibov, a função irá percorrer cada
# coluna do DataFrame e baixar o histórico do preço da ação
# bench.ticker: Valor cotado na bolsa de valores de São Paulo
dados_ibov = BatchGetSymbols(
  tickers = ibov$tickersSA,
  first.date = di,
  last.date = df,
  bench.ticker = benchmark
)

# Gerando uma nova variável apenas com o DataFrame tickers, o DataFrame 
# df.control não será utilizado
dados_ibov = dados_ibov$df.tickers

# SEÇÃO 2 - capturando várias ações

# Próximo passo 
# Capturar a coluna de preço ajustado de todas as ações, gerando um DataFrame 
# com uma coluna para cada ação e o respectivo preço ajustado
# Gerando um DataFrame para cada ação
dados_ibov2 = dlply(dados_ibov, .(ticker), function(x) {rownames(x) = x$row; 
                    x$row = NULL;x})

# Gerando um único DataFrame com a coluna de data e uma coluna para cada ação
# acao: É igual ao primeiro DataFrame em dados_ibov2, e a sétima e sexta coluna
# do DataFrame, que corresponde a data e ao preço ajustado da ação
acao = dados_ibov2[[1]][,c(7,6)]

# Renomeando a coluna
# O coluna da primeira coluna será Data e a segunda coluna será Preço 
# concatenado ao valor da primeira linha do DataFrame na coluna 8, 
# Lógica é Preço + ticket da ação, assim será possível criar uma coluna com a
# descriminação de cada ação na respectiva coluna
colnames(acao) = c('Data', paste('Preço', dados_ibov2[[1]][1,8]))

# Percorrendo a lista e capturando a sétima e sexta coluna de cada DataFrame
# para gerar um único DataFrame com essas informações
for(i in 2:75) {
  novaacao = dados_ibov2[[i]][,c(7,6)]
  colnames(novaacao) = c('Data', paste('Preço', dados_ibov2[[i]][1,8]))
  acao = merge(acao, novaacao, by = 'Data')
}

# Gerando um gráfico com várias ações
# Ações do setor financeiro

f_bancos = ggplot() +
  geom_line(data = acao, aes(x = Data, y = `Preço BBAS3.SA`, 
                             color = 'Banco do Brasil')) +
  geom_line(data = acao, aes(x = Data, y = `Preço BBDC4.SA`, 
                             color = 'Bradesco')) +
  geom_line(data = acao, aes(x = Data, y = `Preço ITUB4.SA`, 
                             color = 'Itaú')) +
  geom_line(data = acao, aes(x = Data, y = `Preço SANB11.SA`, 
                             color = 'Santander')) +
  
  xlab('Data') +
  ylab('Preço')

f_bancos$labels$colour = 'Bancos'
print(f_bancos)

# SEÇÃO 3 - Normalizando o preço das ações
# Utilizando índices de referência no mercado financeiro

# Índice da Bolsa de Valores de São Paulo
IBOV = BatchGetSymbols(
  tickers = '^BVSP',
  first.date = di,
  last.date = df,
  bench.ticker = benchmark
)

# Capturando o DataFrame tickers
IBOV = IBOV$df.tickers
# Renomeando as colunas
colnames(IBOV)[6] = 'IBOV'
colnames(IBOV)[7] = 'Data'
# Gerando um novo DataFrame com as colunas 7 e 6
IBOV = IBOV[,c(7,6)]

# Índice da Bolsa Norte Americana
SP500 = BatchGetSymbols(
  tickers = '^GSPC',
  first.date = di,
  last.date = df,
  bench.ticker = '^GSPC'
)

SP500 = SP500$df.tickers
colnames(SP500)[6] = 'SP500'
colnames(SP500)[7] = 'Data'
SP500 = SP500[,c(7,6)]

# Concatenando os dois índices 
ibov_sp500 = merge(IBOV, SP500, by = 'Data')

# Concatenando os índices as cotações da ações
acao_indices = merge(ibov_sp500, acao, by = 'Data')

# Normalizando os índices
# normalizado: ìndices desconsiderando a coluna de data
normalizado = acao_indices[,-c(1)]

# A primeira linha será igual a 1, as demais será igual a a divisão pelo 
# primeiro registro
novo_acao_indices = data.frame(lapply(normalizado, function(x) x/x[1]))

novo_acao_indices$Data = acao_indices$Data

f_construcao = ggplot() +
  geom_line(data = novo_acao_indices, aes(x = Data, y = `Preço.EZTC3.SA`, 
                             color = 'EZTEC')) +
  geom_line(data = novo_acao_indices, aes(x = Data, y = `Preço.MRVE3.SA`, 
                             color = 'MRV')) +
  geom_line(data = novo_acao_indices, aes(x = Data, y = `Preço.CYRE3.SA`, 
                             color = 'Cyrela')) +
  geom_line(data = novo_acao_indices, aes(x = Data, y = `IBOV`, 
                             color = 'IBOV')) +
  geom_line(data = novo_acao_indices, aes(x = Data, y = `SP500`, 
                                          color = 'SP500')) +
  
  xlab('Data') +
  ylab('Preço')

f_bancos$labels$colour = 'Construção'
print(f_construcao)

# Visualizando todas as colunas

# Gerando um data frame com apenas uma coluna com todos os índices
df = melt(novo_acao_indices, id.vars = 'Data', variable.name = 'series')

ggplot(df, aes(Data, value)) + geom_line(aes(colour = series))

# SEÇÃO 4 - Calculando correlação e construíndo portfólio
correlacoes = cor(normalizado, use = 'complete.obs', method = 'spearman')
corrplot(correlacoes, number.cex = 0.001, number.font = 5)

# tabela_1: amostra de dados para visualizar a correlação
tabela_1 = normalizado[,c(1,2,15:25)]
cor_tabela_1 = cor(tabela_1, use = 'complete.obs', method = 'spearman')
corrplot(cor_tabela_1, number.cex = 1, number.font = 1, method = 'number',
         type = 'lower')

tabela_2 = normalizado[, colnames(normalizado) %in% c('Preço VALE3.SA', 
                                                      'Preço TOTS3.SA',
                                                      'Preço MGLU3.SA',
                                                      'IBOV',
                                                      'Preço EMBR3.SA')]
cor_tabela_2 = cor(tabela_2, use = 'complete.obs', method = 'spearman')
corrplot(cor_tabela_2, number.cex = 1, number.font = 1, method = 'number',
         type = 'lower')

# Construção do portfólio

novo_acao_indices$carteira = 
  0.2 * novo_acao_indices$Preço.B3SA3.SA +
  0.15 * novo_acao_indices$Preço.ABEV3.SA +
  0.3 * novo_acao_indices$Preço.EZTC3.SA +
  0.2 * novo_acao_indices$Preço.MGLU3.SA +
  0.15 * novo_acao_indices$Preço.TOTS3.SA

portfolio = ggplot() +
  geom_line(data = novo_acao_indices, aes(x = Data, y = `carteira`, 
                                          color = 'Meu Portfólio')) +
  geom_line(data = novo_acao_indices, aes(x = Data, y = `Preço.MRVE3.SA`, 
                                          color = 'MRV')) +
  geom_line(data = novo_acao_indices, aes(x = Data, y = `Preço.CYRE3.SA`, 
                                          color = 'Cyrela')) +
  geom_line(data = novo_acao_indices, aes(x = Data, y = `IBOV`, 
                                          color = 'IBOV')) +
  geom_line(data = novo_acao_indices, aes(x = Data, y = `SP500`, 
                                          color = 'SP500')) +
  
  xlab('Data') +
  ylab('Preço')

f_bancos$labels$colour = 'Ativos vs. Portfólio'
print(portfolio)
