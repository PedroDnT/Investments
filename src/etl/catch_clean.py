import streamlit as st
# Data manipulation
import pandas as pd
from datetime import date

# Yahoo finance
import yfinance as yf

# API Requests 
import urllib3
import ssl
import requests
import json


#----------------------------Solving problem: unsafe legacy renegotiation disabled (_ssl.c:997)
class CustomHttpAdapter (requests.adapters.HTTPAdapter):
    '''
    --> "Transport adapter" that allows us to use custom ssl_context.

    Source: https://py4u.org/questions/71603314/
    '''
    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_context=self.ssl_context)

#----------------------------Solving problem: unsafe legacy renegotiation disabled (_ssl.c:997)
def get_legacy_session():
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
    session = requests.session()
    session.mount('https://', CustomHttpAdapter(ctx))
    return session


class DownloadFilesBrGov:
    '''
    --> Download files from the Brazilian Government Services
    '''
    def __init__(self,
                initial_date='01/01/2015', final_date=date.today().strftime('%d/%m/%Y'),
                indicators_ibge=['https://servicodados.ibge.gov.br/api/v3/agregados/1736/periodos/-77/variaveis/44?localidades=N1[all]',
                                'https://servicodados.ibge.gov.br/api/v3/agregados/1737/periodos/-77/variaveis/63?localidades=N1[all]'], 
                description_indicators_ibge=['inpc', 'ipca'], code_series_bcb=['196', '4391', '4390'], 
                description_indicators_bcb=['savings', 'cdi', 'selic']):
        '''
        :param initial_date: Initial date to downloads files
        :param final_date: The last day of file downloads
        :param indicators_ibge: List with URLs to download the files of the Brazilian Institute of Geography and Statistics - IBGE 
        :param description_indicators_ibge: Description of the files that will be downloaded from the IBGE API
        :param code_series_bcb: Code of series to download files from Central Bank of Brazil Time Series Managment System 
        :param description_indicators_bcb: Descriptions of series that will be downloaded from Central Bank of Brazil Time Sereies 
        Managment System 
        '''
        self._initial_date = initial_date
        self._final_date = final_date
        self._indicators_ibge = indicators_ibge
        self._description_indicators_ibge = description_indicators_ibge
        self._code_series_bcb = code_series_bcb
        self._description_indicators_bcb = description_indicators_bcb


    def catch_json(self, url):
        '''
        --> Catch the information from URL in JSON format

        :param url: URL of API service
        '''
        data_json = get_legacy_session().get(url)
        data_dic = json.loads(data_json.content)
        return data_dic


    def series_central_bank(self):
        '''
        --> Download the series via the Central Bank of Brazil API
        '''
        for index in range(len(self._code_series_bcb)):
            api_bcb = 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.' + self._code_series_bcb[index] + '/dados?formato=json&dataInicial=' + self._initial_date + '&dataFinal=' + self._final_date
            data_dic = self.catch_json(api_bcb)
            date = list()
            value = list()
            for i in data_dic:
                date.append(i['data'])
                value.append(i['valor'])
            date_df = pd.DataFrame({'date': date, '%': value})
            date_df.to_csv(f'./data/{self._description_indicators_bcb[index]}.csv', index=False)


    def series_ibge(self):
        '''
        --> Download the series through the API of the Brazilian Institute of Geography and Statistics
        '''
        for index in range(len(self._indicators_ibge)):
            data = self.catch_json(self._indicators_ibge[index])
            data = data[0]['resultados'][0]['series'][0]['serie']
            date = list()
            rate = list()
            for key, value in data.items():
                date.append(key)
                rate.append(value)
            data_df = pd.DataFrame({'date': date, '%': rate})
            data_df.to_csv(f'./data/{self._description_indicators_ibge[index]}.csv', index=False)


class BrazilianIndicators:
    '''
    --> Takes and cleans information about investments and indexes and group it into a DataFrame Pandas
    '''
    def __init__(self, indicators_bcb=['Poupança', 'CDI', 'Selic'], indicators_ibge=['INPC', 'IPCA'],
                data_frame_central_bank=pd.DataFrame(), 
                files_central_bank=['./data/savings.csv', './data/cdi.csv', './data/selic.csv'], 
                data_frame_ibge=pd.DataFrame(), 
                files_ibge=['./data/inpc.csv', './data/ipca.csv']):
        '''
        :param indicators_bcb: Indicators that was downloaded on Central Bank of Brazil API (BCB)
        :param indicators_ibge: Indicators that was downloaded from Brazilian Institute of Geography and Statistics API (IBGE)
        :param data_frame_central_bank: DataFrame Pandas of downloaded files from BCB API
        :param files_central_bank: Files that was downloaded from BCB API
        :param data_frame_ibge: DataFrame Pandas from the files that were downloaded from IBGE API 
        :param files_ibge: Files that were downloaded from IBGE API
        '''
        self._indicators_bcb = indicators_bcb
        self._indicators_ibge = indicators_ibge
        self._data_frame_central_bank = data_frame_central_bank
        self._files_central_bank = files_central_bank
        self._data_frame_ibge = data_frame_ibge
        self._files_ibge = files_ibge
        

    def clean_data_bcb(self):
        '''
        --> Read and process the data downloaded in the Bank's Time Series Management System Central, the data is monthly.
        '''
        for index in range(len(self._files_central_bank)):
            data = pd.read_csv(self._files_central_bank[index])
            data.columns = ['date', self._indicators_bcb[index]]
            data['date'] = pd.to_datetime(data['date'], format='%d/%m/%Y', dayfirst=True)
            if self._data_frame_central_bank.empty:
                self._data_frame_central_bank = pd.concat([self._data_frame_central_bank, data], axis=1)
            else:
                self._data_frame_central_bank = self._data_frame_central_bank.merge(data, on='date')
    

    def clean_data_ibge(self):
        '''
        --> Read and process the data made available by the IBGE, the data are monthly
        '''
        for index in range(len(self._files_ibge)):
            data = pd.read_csv(self._files_ibge[index])
            data.columns = ['date', self._indicators_ibge[index]]
            data['date'] = data['date'].astype('str')
            data['year'] = data['date'].str[:4]
            data['month'] = data['date'].str[4:]
            data['date'] = '01' + '/' + data['month'] + '/' + data['year']
            data.drop(['month', 'year'], axis=1, inplace=True)
            data['date'] = pd.to_datetime(data['date'], format='%d/%m/%Y', dayfirst=True)
            if self._data_frame_ibge.empty:
                self._data_frame_ibge = pd.concat([self._data_frame_ibge, data], axis=1)
            else:
                self._data_frame_ibge = self._data_frame_ibge.merge(data, on='date')


    def data_frame_indicators(self):
        '''
        --> Gather all files into a DataFrame Pandas
        '''
        data_frame = pd.merge(self._data_frame_central_bank, self._data_frame_ibge, on='date')
        return data_frame

def carteira_ibov(tickers_file_path: str, cols: list):
    carteira = pd.read_csv(tickers_file_path, encoding='ISO-8859-1', sep=';', skiprows=1, skipfooter=2,
                            usecols=cols, engine='python')
    carteira.reset_index(inplace=True)
    carteira.columns = carteira.columns.str.lower()
    carteira['index'] = carteira['index'] + '.SA'
    return carteira


@st.cache
def read_fund_data(path: str):
    '''
    Read historical investment fund data 

    Parameters: path : String 
                    The file path

    Returns: DataFrame
                Pandas DataFrame with fund historical data containing with the following columns: 
                    dt_comptc: Date 
                    cnpj_fundo: CNPJ 
                    denom_social: Social denomination 
                    vl_quota: Value of quota 
                    vl_patrim_liq: Value of net worth 
                    captc_dia: Fundraising carried out on the day
                    resg_dia: Redemptions paid on the day 
                    nr_cotst: Number of shareholders
    '''
    df = pd.read_csv(path)
    df['date'] = pd.to_datetime(df['date'])
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


@st.cache    
def request_data(selected_tickers: list, start_date: str):
    '''
    Download historical financial data from Yahoo Finance about ticker negatiation 

    Parameters: selected_tickers : List of string 
                    Company tickers selected to download
    
                start_date: String
                    Initial date to download historical data

    Returns: DataFrame
                Pandas DataFrame with Open, High, Low, Close, Adj Close and Volume columns about selected tickers 
                market negatiation
    '''
    today = date.today()
    df = yf.download(tickers=selected_tickers, start=start_date, end=today)
    df.reset_index(inplace=True)
    return df
