import pandas as pd
from datetime import date
import requests
import json
import pandas_datareader.data as web


class BaixaArquivos:
    '''
    --> Baixa os arquivos para tratamento e análise
    '''
    def __init__(self,
                data_inicial_yahoo='2015-01-01', data_final_yahoo=date.today(), data_inicial_bcb='01/01/2015', 
                data_final_bcb=date.today().strftime('%d/%m/%Y'), site_dados='yahoo', empresas_yahoo=['PETR4.SA', 'BBAS3.SA', 
                                                                                                    'MGLU3.SA'],
                indicadores_ibge=['https://servicodados.ibge.gov.br/api/v3/agregados/1736/periodos/-77/variaveis/44?localidades=N1[all]',
                                'https://servicodados.ibge.gov.br/api/v3/agregados/1737/periodos/-77/variaveis/63?localidades=N1[all]'], 
                descricao_indicadores_ibge=['inpc', 'ipca'], 
                codigos_series_bcb=['196', '4391', '4390'], 
                indicadores_bcb=['poupanca', 'cdi', 'selic'],
                api_alpha_vantage_1='https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&outputsize=full&symbol=',
                api_alpha_vantage_2='&apikey=M5QSLH6PMM9ZZXDD',
                api_alpha_vantage_co=['IBM']):
        '''
        :param indicadores_ibge: 
        1º: 1736-INPC-Série histórica com número-índice, variação mensal e variações acumuladas em 3 meses, em 6 meses, 
        no ano e em 12 meses (a partir de abril/1979),
        2º: 1737-IPCA-Série histórica com número-índice, variação mensal e variações acumuladas em 3 meses, em 6 meses, 
        no ano e em 12 meses (a partir de dezembro/1979)
        :param descricao_indicadores_ibge: Descrição dos indicadores que estão sendo baixados no site no IBGE
        :param data_inicial_bcb: Data inicial da série
        :param data_final_bcb: Data final da série
        :param codigos_series_bcb: Lista com os códigos das séries que será baixada via api do Sistema Gerenciador de Séries Temporais do Banco Central, 
        documentação disponível em: https://dadosabertos.bcb.gov.br/dataset/20542-saldo-da-carteira-de-credito-com-recursos-livres---total/resource/6e2b0c97-afab-4790-b8aa-b9542923cf88
        :param indicadore_bcb: Lista com a descrição dos indicadores que estão sendo baixados 
        :param api_alpha_vantage_1: Primeira parte da URL da API do site Alpha Vantage
        :param api_alpha_vantage_2: Segunda parte da URL da API do site Alpha Vantage
        :param api_alpha_vantage_co: Descrição da empresa para captura dos dados
        '''
        self._data_inicial_yahoo = data_inicial_yahoo
        self._data_final_yahoo = data_final_yahoo
        self._site_dados = site_dados
        self._indicadores_ibge = indicadores_ibge
        self._descricao_indicadores_ibge = descricao_indicadores_ibge
        self._indicadores_ibge = indicadores_ibge
        self._data_inicial_bcb = data_inicial_bcb
        self._data_final_bcb = data_final_bcb
        self._codigos_series_bcb = codigos_series_bcb
        self._indicadores_bcb = indicadores_bcb
        self._api_alpha_vantage_1 = api_alpha_vantage_1
        self._api_alpha_vantage_2 = api_alpha_vantage_2
        self._api_alpha_vantage_co = api_alpha_vantage_co


    def captura_json(self, url):
        '''
        --> Captura as infomações da URL em formato JSON

        :param url: URL do serviço da API de dados
        '''
        dados_json = requests.get(url)
        dados_dic = json.loads(dados_json.content)
        return dados_dic


    def series_banco_central(self):
        '''
        --> Baixa as séries temporais via api do Banco Central
        '''
        for indice in range(len(self._codigos_series_bcb)):
            api_bcb = 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.' + self._codigos_series_bcb[indice] + '/dados?formato=json&dataInicial=' + self._data_inicial_bcb + '&dataFinal=' + self._data_final_bcb
            dados_json = requests.get(api_bcb)
            dados_dic = json.loads(dados_json.content)
            data = list()
            valor = list()
            for i in dados_dic:
                data.append(i['data'])
                valor.append(i['valor'])
            dados_df = pd.DataFrame({'data': data, '%': valor})
            dados_df.to_csv(f'./dados/{self._indicadores_bcb[indice]}.csv', index=False)


    def series_ibge(self):
        '''
        --> Baixa as séreis temporais via api do IBGE
        '''
        for indice in range(len(self._indicadores_ibge)):
            dados = requests.get(self._indicadores_ibge[indice])
            dados = json.loads(dados.content)
            dados = dados[0]['resultados'][0]['series'][0]['serie']
            data = list()
            taxa = list()
            for chave, valor in dados.items():
                data.append(chave)
                taxa.append(valor)
            dados_df = pd.DataFrame({'data': data, '%': taxa})
            dados_df.to_csv(f'./dados/{self._descricao_indicadores_ibge[indice]}.csv', index=False)


    def series_alpha_vantage(self):
        '''
        Baixa as séries de fechamento de ações diárias por meio da API do site https://www.alphavantage.co/
        '''
        for empresa in self._api_alpha_vantage_co:
            dados = self.captura_json(self._api_alpha_vantage_1 + empresa + self._api_alpha_vantage_2)
            data = list()
            fechamento = list()
            for i in dados['Time Series (Daily)'].keys():
                data.append(i)
                fechamento.append(dados['Time Series (Daily)'][i]['4. close'])
            data_frame = pd.DataFrame({'data': data, empresa: fechamento})
            data_frame.to_csv(f'./dados/{empresa.lower()}.csv', index=False)


def yahoo_fiance(data_inicial='2015-01-01', data_final=date.today(), empresas=['PETR4.SA', 'BBAS3.SA', 'MGLU3.SA'],
                descricao_empresas=['Petrobras', 'Banco do Brasil', 'Magazine Luiza']):
    '''
    Captura os dados no site do Yahoo Finance
    '''
    for indice in range(len(empresas)):
        dados = web.DataReader(empresas[indice], 'yahoo', data_inicial, data_final)
        dados.columns = ['alta', 'baixa', 'abertura', 'fechamento', 'volume', 'fechamento_ajustado']
        dados.to_csv(f'./dados/{descricao_empresas[indice].lower()}.csv')


class Indicadores:
    '''
    --> Captura e trata as informações referente a investimentos e indicadores e agrupa as informações em um DataFrame Pandas
    '''
    def __init__(self, indicadores_bcb=['Poupança', 'CDI', 'Selic'], indicadores_ibge=['INPC', 'IPCA'],
                data_frame_banco_central=pd.DataFrame(), arquivos_banco_central=['./dados/poupanca.csv', './dados/cdi.csv',
                                                                                './dados/selic.csv'], 
                data_frame_ibge=pd.DataFrame(), 
                arquivos_ibge=['./dados/inpc.csv', './dados/ipca.csv']):
        '''
        :param indicadores_bcb: Indicadores baixados no site do Banco Central
        :param indicadores_ibge: Indicadores baixados no site do IBGE
        :param data_frame_banco_central: DataFrame Pandas dos arquivos baixados no Sistema Gerenciador de Séries Temporais do Banco 
        Central
        :param arquivos_banco_central: Arquivos baixados do Sistema Gerenciador de Séries Temporais do Banco Central
        :param data_frame_ibge: DataFrame Pandas dos arquivos baixados no  site do IBGE
        :param arquivos_ibge: Arquivos baixados no site do IBGE
        '''
        self._indicadores_bcb = indicadores_bcb
        self._indicadores_ibge = indicadores_ibge
        self._data_frame_banco_central = data_frame_banco_central
        self._arquivos_banco_central = arquivos_banco_central
        self._data_frame_ibge = data_frame_ibge
        self._arquivos_ibge = arquivos_ibge
        

    def tratamento_dados_bcb(self):
        '''
        --> Faz a leitura e tratamento dos dados baixados no Sistema Gerenciador de Séries Temporais do Banco 
        Central, os dados estão em periodicidade mensal.
        '''
        for indice in range(len(self._arquivos_banco_central)):
            dados = pd.read_csv(self._arquivos_banco_central[indice])
            dados.columns = ['data', self._indicadores_bcb[indice]]
            dados['data'] = pd.to_datetime(dados['data'], format='%d/%m/%Y', dayfirst=True)
            if self._data_frame_banco_central.empty:
                self._data_frame_banco_central = pd.concat([self._data_frame_banco_central, dados], axis=1)
            else:
                self._data_frame_banco_central = self._data_frame_banco_central.merge(dados, on='data')
    

    def tratamento_dados_ibge(self):
        '''
        --> Faz a leitura e tratamento dos dados disponibilizados pelo IBGE, os dados estão em periodicidade mensal
        '''
        for indice in range(len(self._arquivos_ibge)):
            dados = pd.read_csv(self._arquivos_ibge[indice])
            dados.columns = ['data', self._indicadores_ibge[indice]]
            dados['data'] = dados['data'].astype('str')
            dados['ano'] = dados['data'].str[:4]
            dados['mes'] = dados['data'].str[4:]
            dados['data'] = '01' + '/' + dados['mes'] + '/' + dados['ano']
            dados.drop(['mes', 'ano'], axis=1, inplace=True)
            dados['data'] = pd.to_datetime(dados['data'], format='%d/%m/%Y', dayfirst=True)
            if self._data_frame_ibge.empty:
                self._data_frame_ibge = pd.concat([self._data_frame_ibge, dados], axis=1)
            else:
                self._data_frame_ibge = self._data_frame_ibge.merge(dados, on='data')


    def data_frame_investimentos_mensal(self):
        '''
        --> Reune todos os arquivos em um DataFrame pandas
        '''
        data_frame = pd.merge(self._data_frame_banco_central, self._data_frame_ibge, on='data')
        return data_frame