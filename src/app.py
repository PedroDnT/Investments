from captura_tratamento import Investimentos
from analise import SerieTemporal
import streamlit as st

poupanca = Investimentos(historico_poupanca='./dados/poupanca.csv').rendimentos_poupanca()
inpc = Investimentos(historico_inpc='./dados/inpc.xls').indice_inpc()

def main():
    analise_poupanca = SerieTemporal(poupanca)
    analise_poupanca.serie_temporal(x='data', y='rentabilidade', titulo='Rentabilidade Poupança', x_label='', y_label='%', 
                                    x_inpc=inpc['data'], y_inpc=inpc['mes_%'])

if __name__ == '__main__':
    main()


