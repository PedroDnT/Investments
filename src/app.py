from captura_tratamento import Investimentos
from analise import SerieTemporal
import streamlit as st


poupanca_df = Investimentos(dados_banco_central='./dados/poupanca.csv').tratamento_dados_bcb()
cdi_df = Investimentos(dados_banco_central='./dados/cdi.csv').tratamento_dados_bcb()
inpc_df = Investimentos(dados_ibge='./dados/inpc.xls').tratamento_dados_ibge()
ipca_df = Investimentos(dados_ibge='./dados/ipca.xls').tratamento_dados_ibge()
# Igualando o número de linhas pela menor série
menor_serie = min(poupanca_df.shape[0], cdi_df.shape[0], inpc_df.shape[0], ipca_df.shape[0])
poupanca_df = poupanca_df[:menor_serie]
cdi_df = cdi_df[:menor_serie]
inpc_df = inpc_df[:menor_serie]
ipca_df = ipca_df[:menor_serie]


def main():
    # Seleção do período em anos
    anos = poupanca_df['data'].dt.year.unique().tolist()
    periodo = st.sidebar.slider('Selecione o período', min_value=min(anos), max_value=max(anos), value=(min(anos), max(anos)))

    # Seleção da opção de investimento
    opcao_investimento = ['POUPANÇA', 'CDI']
    selecao_opcao_investimento = st.sidebar.selectbox('Opção de Investimento', opcao_investimento)
    if selecao_opcao_investimento == 'POUPANÇA':
        investimento_selecionado = poupanca_df
    elif selecao_opcao_investimento == 'CDI':
        investimento_selecionado = cdi_df

    # Seleção do índice de inflação
    indices_inflacao = ['IPCA', 'INPC']
    selecao_indice_inflacao = st.sidebar.selectbox('Índice de Inflação', indices_inflacao)
    if selecao_indice_inflacao == 'IPCA':
        inflacao_selecionada = ipca_df
    elif selecao_indice_inflacao == 'INPC':
        inflacao_selecionada = inpc_df

    # Visualização gráfica
    st.markdown("<h1 style='text-align: right; font-size: 15px; font-weight: normal'>V.1</h1>", 
                unsafe_allow_html=True)
    st.title('Investimentos')
    analise_investimento = SerieTemporal(investimento_selecionado, inflacao_selecionada, periodo=periodo)
    analise_investimento.serie_temporal(titulo=f'Rentabilidade {selecao_opcao_investimento}', 
                                    descricao_indice_inflacao=selecao_indice_inflacao,
                                    descricao_investimento=selecao_opcao_investimento)
    if selecao_indice_inflacao == 'IPCA':
        st.text('IPCA: Abrange as famílias com rendimentos de 1 a 40 salários mínimos (IBGE)')
    elif selecao_indice_inflacao == 'INPC':
        st.text('INPC: Abrange as famílias com rendimentos de 1 a 5 salários mínimos (IBGE)')
    if selecao_opcao_investimento == 'POUPANÇA':
        st.text('POUPANÇA: Depósitos a partir de 04.05.2012 - Rentabilidade no 1º dia do mês (BCB-Demab)')
    elif selecao_opcao_investimento == 'CDI':
        st.text('CDI: Taxa de juros acumulada no mês (BCB-Demab)')
    st.markdown('Repositório no [GitHub](https://github.com/MarcosRMG/Investimentos)')
    
if __name__ == '__main__':
    main()
