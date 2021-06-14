from captura_tratamento import Indicadores
from analise import AnalisaSerie
import streamlit as st
import pandas as pd
import numpy as np


dados = Indicadores()
dados.tratamento_dados_bcb()
dados.tratamento_dados_ibge()
dados = dados.data_frame_investimentos()
# Descrição dos dados
descricao = pd.DataFrame({'Poupança': ['POUPANÇA: Rentabilidade no 1º dia do mês (BCB-Demab)'],
                            'CDI': ['CDI: Taxa de juros acumulada no mês (BCB-Demab)'],
                            'IPCA': ['IPCA: Abrange as famílias com rendimentos de 1 a 40 salários mínimos (IBGE)'],
                            'INPC': ['INPC: Abrange as famílias com rendimentos de 1 a 5 salários mínimos (IBGE)'],
                            'Selic': ['Selic: Taxa de juros acumulada no mês']})

def main():
    # Seleção do período em anos
    anos = dados['data'].dt.year.unique().tolist()
    periodo = st.sidebar.slider('Selecione o período', min_value=min(anos), max_value=max(anos), value=(min(anos), max(anos)))
    # Classe para análise
    analisa = AnalisaSerie(dados, periodo)
    # Indicadores
    investimentos = ['Poupança', 'CDI']
    indexadores = ['IPCA', 'INPC', 'Selic']
    #indicadores = ['Poupança', 'CDI', 'IPCA', 'INPC', 'Selic']
    indicadores = dados.columns[1:]
    # Visualização gráfica
    st.markdown("<h1 style='text-align: right; font-size: 15px; font-weight: normal'>V.1</h1>", 
                unsafe_allow_html=True)
    st.title('Análise de Investimentos')
    acao = st.sidebar.selectbox('Visualizar', ['Indicador', 'Comparação'])
    if acao == 'Indicador':
        indicador = st.sidebar.selectbox('Indicador', indicadores)
        analisa.visualiza_indicador(dados, eixo_y=indicador, descricao_indicador=indicador)
        st.text(descricao[indicador][0])
    elif acao == 'Comparação':
        opcao_comparacao = st.sidebar.selectbox('Comparar com', ['Investimento', 'Indexador'])
        if opcao_comparacao == 'Investimento':    
            # Seleção da opção de investimento
            investimento = st.sidebar.selectbox('Avaliar', investimentos)
            comparacao = st.sidebar.selectbox('Comparar', np.sort(investimentos))
            analisa.compara_indicador(investimento, comparacao, investimento, comparacao, f'{investimento} x {comparacao}') 
            st.text(descricao[investimento][0])
            st.text(descricao[comparacao][0])       
        elif opcao_comparacao == 'Indexador':
            investimento = st.sidebar.selectbox('Investimento', investimentos)
            indexador = st.sidebar.selectbox('Indexador', indexadores)
            analisa.compara_indicador(investimento, indexador, investimento, indexador, 
                                    f'{investimento} x {indexador}')
            st.text(descricao[investimento][0])
            st.text(descricao[indexador][0])
    st.markdown('Repositório no [GitHub](https://github.com/MarcosRMG/Investimentos)')
    
if __name__ == '__main__':
    main()
