import pandas as pd
import shutil
import urllib.request as request
from contextlib import closing
from zipfile import ZipFile
import os


class BaixaArquivos:
    '''
    --> Baixa os arquivos para tratamento e análise
    '''
    def __init__(self, 
                link_inpc='https://ftp.ibge.gov.br/Precos_Indices_de_Precos_ao_Consumidor/INPC/Serie_Historica/inpc_SerieHist.zip',
                link_ipca='https://ftp.ibge.gov.br/Precos_Indices_de_Precos_ao_Consumidor/IPCA/Serie_Historica/ipca_SerieHist.zip'):
        '''
        :link_inpc: Link para baixar o arquivo com a série historica do INPC
        :link_ipca: Link para baixar o arquivo com a série historica do IPCA
        '''
        self._link_inpc = link_inpc
        self._link_ipca = link_ipca

    
    def baixa_inpc(self):
        '''
        --> Baixa o arquivo com a série histórica do INPC
        '''
        # Baixando arquivo da internet
        with closing(request.urlopen(self._link_inpc)) as r:
            with open('inpc_SerieHist.zip', 'wb') as f:
                shutil.copyfileobj(r, f)
        # Movendo e renomeando o arquivo zip
        shutil.move('inpc_SerieHist.zip', 
                    './dados/inpc.zip')
        # Extraindo o arquivo xls e renomeando o arquivo
        with ZipFile('./dados/inpc.zip', 'r') as zip_ref:
            zip_ref.extractall('./dados')
        if os.path.exists('.dados/inpc.xls'):
            os.remove('./dados/inpc.xls')
            os.rename('./dados/inpc_202104SerieHist.xls', './dados/inpc.xls')
        else:
            os.rename('./dados/inpc_202104SerieHist.xls', './dados/inpc.xls')
    

    def baixa_ipca(self):
        '''
        --> Baixa o arquivo com a série histórica do IPCA
        '''
        # Baixando arquivo da internet
        with closing(request.urlopen(self._link_ipca)) as r:
            with open('ipca_SerieHist.zip', 'wb') as f:
                shutil.copyfileobj(r, f)
        # Movendo e renomeando o arquivo zip
        shutil.move('ipca_SerieHist.zip', 
                    './dados/ipca.zip')
        # Extraindo o arquivo xls e renomeando o arquivo
        with ZipFile('./dados/ipca.zip', 'r') as zip_ref:
            zip_ref.extractall('./dados')
        if os.path.exists('.dados/ipca.xls'):
            os.remove('./dados/ipca.xls')
            os.rename('./dados/ipca_202104SerieHist.xls', './dados/ipca.xls')
        else:
            os.rename('./dados/ipca_202104SerieHist.xls', './dados/ipca.xls')


class Investimentos:
    '''
    --> Captura e trata as informações referente a investimentos e indicadores
    '''
    def __init__(self, historico_poupanca=None, historico_inpc=None, historico_ipca=None):
        '''
        :param histico_poupanca: Arquivo com o histórico dos pagamentos da poupança disponível em: 
        https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries
        :param historico_inpc: Arquivo com o histórico do índice INPC disponível em: 
        https://www.ibge.gov.br/estatisticas/economicas/precos-e-custos/9258-indice-nacional-de-precos-ao-consumidor.html?t=series-historicas
        :param historico_ipca: Arquivo com o histórico do índice IPCA disponível em: 
        https://www.ibge.gov.br/estatisticas/economicas/precos-e-custos/9258-indice-nacional-de-precos-ao-consumidor.html?t=series-historicas
        '''
        self._historico_poupanca = historico_poupanca
        self._historico_inpc = historico_inpc
        self._historico_ipca = historico_ipca
        

    def rendimentos_poupanca(self):
        '''
        --> Faz a leitura e tratamento dos histórico da poupança disponível no Sistema Gerenciador de Séries Temporais do Banco 
        Central
        '''
        poupanca = pd.read_csv(self._historico_poupanca, encoding='ISO-8859-1', sep=';', skipfooter=1, engine='python')
        poupanca.columns = ['data', 'rentabilidade']
        poupanca['rentabilidade'] = poupanca['rentabilidade'].str.replace(',', '.')
        poupanca['data'] = pd.to_datetime(poupanca['data'])
        poupanca['rentabilidade'] = poupanca['rentabilidade'].astype('float32')
        return poupanca
    

    def indice_inpc(self, renomeia_mes={'JAN': '1', 
                                        'FEV': '2', 
                                        'MAR': '3', 
                                        'ABR': '4', 
                                        'MAI': '5', 
                                        'JUN': '6', 
                                        'JUL': '7', 
                                        'AGO': '8', 
                                        'SET': '9',
                                        'OUT': '10', 
                                        'NOV': '11', 
                                        'DEZ': '12'}):
        '''
        --> Faz a leitura e tratamento dos histórico do índice INPC apurado pelo IBGE
        '''
        inpc = pd.read_excel(self._historico_inpc, header=6, skiprows=1)
        inpc = inpc.iloc[:, :4]
        inpc.columns = ['ano', 'mes', 'n_indice', 'mes_%']
        inpc['ano'] = inpc['ano'].fillna(method='ffill')
        inpc.dropna(inplace=True)
        inpc['mes'] = inpc['mes'].map(renomeia_mes)
        inpc['ano'] = inpc['ano'].astype('str')
        inpc['data'] = inpc['ano'] + '-' + inpc['mes']
        inpc['data'] = pd.to_datetime(inpc['data'])
        inpc = inpc[['data', 'mes_%']]
        inpc = inpc[inpc['data'] > '2012-05-01']
        inpc['mes_%'] = inpc['mes_%'].astype('float32')
        inpc.reset_index(drop=True, inplace=True)
        return inpc


    def indice_ipca(self, renomeia_mes={'JAN': '1', 
                                        'FEV': '2', 
                                        'MAR': '3', 
                                        'ABR': '4', 
                                        'MAI': '5', 
                                        'JUN': '6', 
                                        'JUL': '7', 
                                        'AGO': '8', 
                                        'SET': '9',
                                        'OUT': '10', 
                                        'NOV': '11', 
                                        'DEZ': '12'}):
        '''
        --> Faz a leitura e tratamento dos histórico do índice IPCA apurado pelo IBGE
        '''
        ipca = pd.read_excel(self._historico_ipca, header=6, skiprows=1)
        ipca = ipca.iloc[:, :4]
        ipca.columns = ['ano', 'mes', 'n_indice', 'mes_%']
        ipca['ano'] = ipca['ano'].fillna(method='ffill')
        ipca.dropna(inplace=True)
        ipca['mes'] = ipca['mes'].map(renomeia_mes)
        ipca['ano'] = ipca['ano'].astype('str')
        ipca['data'] = ipca['ano'] + '-' + ipca['mes']
        ipca['data'] = pd.to_datetime(ipca['data'])
        ipca = ipca[['data', 'mes_%']]
        ipca = ipca[ipca['data'] > '2012-05-01']
        ipca['mes_%'] = ipca['mes_%'].astype('float32')
        ipca.reset_index(drop=True, inplace=True)
        return ipca
