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
        os.remove('./dados/inpc.zip')
    

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
        os.remove('./dados/ipca.zip')


class Investimentos:
    '''
    --> Captura e trata as informações referente a investimentos e indicadores
    '''
    def __init__(self, dados_banco_central=None, dados_ibge=None):
        '''
        :dados_banco_central: Arquivos baixados no Sistema Gerenciador de Séries Temporais do Banco Central
        :param dados ibge: Arquivos baixados no site do IBGE 
        '''
        self._dados_banco_central = dados_banco_central
        self._dados_ibge = dados_ibge
        

    def tratamento_dados_bcb(self):
        '''
        --> Faz a leitura e tratamento dos dados baixados no Sistema Gerenciador de Séries Temporais do Banco 
        Central, os dados estão em periodicidade mensal.
        '''
        dados_bcb = pd.read_csv(self._dados_banco_central, encoding='ISO-8859-1', sep=';', skipfooter=1, engine='python')
        dados_bcb.columns = ['data', '%']
        dados_bcb['%'] = dados_bcb['%'].str.replace(',', '.')
        dados_bcb['data'] = pd.to_datetime(dados_bcb['data'])
        dados_bcb['%'] = dados_bcb['%'].astype('float32')
        return dados_bcb
    

    def tratamento_dados_ibge(self, renomeia_mes={'JAN': '1', 
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
        --> Faz a leitura e tratamento dos dados disponibilizados pelo IBGE, os dados estão em periodicidade mensal
        '''
        dados_ibge = pd.read_excel(self._dados_ibge, header=6, skiprows=1)
        dados_ibge = dados_ibge.iloc[:, :4]
        dados_ibge.columns = ['ano', 'mes', 'n_indice', '%']
        dados_ibge['ano'] = dados_ibge['ano'].fillna(method='ffill')
        dados_ibge.dropna(inplace=True)
        dados_ibge['mes'] = dados_ibge['mes'].map(renomeia_mes)
        dados_ibge['ano'] = dados_ibge['ano'].astype('str')
        dados_ibge['data'] = dados_ibge['ano'] + '-' + dados_ibge['mes']
        dados_ibge['data'] = pd.to_datetime(dados_ibge['data'])
        dados_ibge = dados_ibge[['data', '%']]
        dados_ibge = dados_ibge[dados_ibge['data'] > '2012-05-01']
        dados_ibge['%'] = dados_ibge['%'].astype('float32')
        dados_ibge.reset_index(drop=True, inplace=True)
        return dados_ibge
