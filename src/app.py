from captura_tratamento import Investimentos
from analise import SerieTemporal
import streamlit as st

poupanca = Investimentos(historico_poupanca='./dados/poupanca.csv').rendimentos_poupanca()


def main():
    analise_poupanca = SerieTemporal(poupanca)
    analise_poupanca.serie_temporal(x='data', y='rentabilidade', titulo='Rentabilidade Poupança', x_label='', y_label='%')

if __name__ == '__main__':
    main()


