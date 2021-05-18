from captura_tratamento import Investimentos
from analise import SerieTemporal
import streamlit as st


investimentos = Investimentos(historico_poupanca='./dados/poupanca.csv', historico_inpc='./dados/inpc.xls')
poupanca_df = investimentos.rendimentos_poupanca()
inpc_df = investimentos.indice_inpc()

def main():
    st.title('Investimentos')
    analise_poupanca = SerieTemporal(investimento=poupanca_df, inpc=inpc_df, x_investimento='data', y_investimento='rentabilidade',
                                    x_inpc='data', y_inpc='mes_%')
    analise_poupanca.serie_temporal(titulo='Rentabilidade Poupança', x_label='', y_label='%')

if __name__ == '__main__':
    main()


