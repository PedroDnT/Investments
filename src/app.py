from captura_tratamento import Investimentos
from analise import SerieTemporal
import streamlit as st


investimentos = Investimentos(historico_poupanca='./dados/poupanca.csv', historico_inpc='./dados/inpc.xls')
poupanca_df = investimentos.rendimentos_poupanca()
inpc_df = investimentos.indice_inpc()

def main():
    # Seleção do período em anos
    anos = poupanca_df['data'].dt.year.unique().tolist()
    periodo = st.sidebar.slider('Selecione o período', min_value=min(anos), max_value=max(anos), value=(min(anos), max(anos)))

    st.title('Investimentos')
    analise_poupanca = SerieTemporal(investimento=poupanca_df, inpc=inpc_df, x_investimento='data', y_investimento='rentabilidade',
                                    x_inpc='data', y_inpc='mes_%', periodo=periodo)
    analise_poupanca.serie_temporal(titulo='Rentabilidade Poupança', x_label='', y_label='%')
    
if __name__ == '__main__':
    main()


