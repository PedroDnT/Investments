import pandas as pd


class Investimentos:
    '''
    --> Captura e trata as informações referente a investimentos
    '''
    def __init__(self, historico_poupanca):
        self._historico_poupanca = historico_poupanca
        '''
        :param histico_poupanca: Arquivo com o histórico dos pagamentos da poupança
        '''

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
