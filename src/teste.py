from captura_tratamento import Indicadores

dados = Indicadores(arquivos_banco_central=['../dados/poupanca.csv', '../dados/cdi.csv', '../dados/selic.csv'],
                    arquivos_ibge=['../dados/inpc.csv', '../dados/ipca.csv'])
dados.tratamento_dados_bcb()
dados.tratamento_dados_ibge()
#dados = dados.data_frame_investimentos()
