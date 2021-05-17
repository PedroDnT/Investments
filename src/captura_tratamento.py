import pandas as pd


class Investimentos:
    '''
    --> Captura e trata as informações referente a investimentos e indicadores
    '''
    def __init__(self, historico_poupanca=None, historico_inpc=None):
        '''
        :param histico_poupanca: Arquivo com o histórico dos pagamentos da poupança disponível em: 
        https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries
        :param historico_inpc: Arquivo com o histórico do índice INPC disponível em: 
        https://www.ibge.gov.br/estatisticas/economicas/precos-e-custos/9258-indice-nacional-de-precos-ao-consumidor.html?t=series-historicas
        '''
        self._historico_poupanca = historico_poupanca
        self._historico_ipca = historico_inpc
        

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
        inpc = pd.read_excel(self._historico_ipca, header=6, skiprows=1)
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
        return inpc
