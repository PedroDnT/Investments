from captura_tratamento import Investimentos
from analise import SerieTemporal
import streamlit as st


investimentos = Investimentos(historico_poupanca='./dados/poupanca.csv', historico_inpc='./dados/inpc.xls', 
                            historico_ipca='./dados/ipca.xls')
poupanca_df = investimentos.rendimentos_poupanca()
inpc_df = investimentos.indice_inpc()
ipca_df = investimentos.indice_ipca()

def main():
    # Seleção do período em anos
    anos = poupanca_df['data'].dt.year.unique().tolist()
    periodo = st.sidebar.slider('Selecione o período', min_value=min(anos), max_value=max(anos), value=(min(anos), max(anos)))
    # Seleção do índice de inflação
    indices_inflacao = ['IPCA', 'INPC']
    selecao_indice_inflacao = st.sidebar.selectbox('Índice de Inflação', indices_inflacao)
    if selecao_indice_inflacao == 'IPCA':
        inflacao_selecionada = ipca_df
    elif selecao_indice_inflacao == 'INPC':
        inflacao_selecionada = inpc_df

    st.title('Investimentos')
    analise_poupanca = SerieTemporal(investimento=poupanca_df, indice_inflacao=inflacao_selecionada, x_investimento='data', 
                                    y_investimento='rentabilidade', x_indice_inflacao='data', y_indice_inflacao='mes_%', 
                                    periodo=periodo)
    analise_poupanca.serie_temporal(titulo='Rentabilidade Poupança', x_label='', y_label='%', 
                                    descricao_indice_inflacao=selecao_indice_inflacao)
    if selecao_indice_inflacao == 'IPCA':
        st.text('IPCA: Abrange as famílias com rendimentos de 1 a 40 salários mínimos (IBGE)')
    elif selecao_indice_inflacao == 'INPC':
        st.text('INPC: Abrange as famílias com rendimentos de 1 a 5 salários mínimos (IBGE)')
    
if __name__ == '__main__':
    main()


