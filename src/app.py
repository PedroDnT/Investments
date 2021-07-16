from captura_tratamento import Indicadores
from analise import AnalisaSerieMensal, AnalisaSerieDiaria
import streamlit as st
import pandas as pd
import numpy as np


dados = Indicadores()
dados.tratamento_dados_bcb()
dados.tratamento_dados_ibge()
dados = dados.data_frame_investimentos_mensal()
ibov = pd.read_csv('./dados/ibov.csv')
ibov['data'] = pd.to_datetime(ibov['data'])
ibov.set_index('data', inplace=True)
# Descrição dos dados
descricao = pd.DataFrame({'Poupança': ['POUPANÇA: Rentabilidade no 1º dia do mês (BCB-Demab)'],
                            'CDI': ['CDI: Taxa de juros acumulada no mês (BCB-Demab)'],
                            'IPCA': ['IPCA: Abrange as famílias com rendimentos de 1 a 40 salários mínimos (IBGE)'],
                            'INPC': ['INPC: Abrange as famílias com rendimentos de 1 a 5 salários mínimos (IBGE)'],
                            'Selic': ['Selic: Taxa de juros acumulada no mês']})

def main():
    acoes_ibov = ibov.columns
    indexadores = ['Poupança', 'CDI', 'IPCA', 'INPC', 'Selic']
    # Visualização gráfica
    st.markdown("<h1 style='text-align: right; font-size: 15px; font-weight: normal'>Versão 1.1</h1>", 
                unsafe_allow_html=True)
    st.title('Análise de Investimentos')
    indicadores = ['Indexadores', 'Ações']
    indicador = st.sidebar.selectbox('Indicador', indicadores)
    if indicador == 'Indexadores':
        anos = dados['data'].dt.year.unique().tolist()
        periodo = st.sidebar.slider('Selecione o período', min_value=min(anos), max_value=max(anos), value=(min(anos), max(anos)))
        indexador = st.sidebar.selectbox('Indexador', indexadores)
        analisa = AnalisaSerieMensal(dados=dados, periodo=periodo)
        analisa.visualiza_indicador(eixo_y=indexador, descricao_indicador=indexador)
    elif indicador == 'Ações':
        data_inicial = st.sidebar.date_input('Data Inicial', ibov.index.min())
        data_final = st.sidebar.date_input('Data Final', ibov.index.max())
        analise_diaria = AnalisaSerieDiaria(ibov, data_inicial, data_final)
        visualizar_acao = st.sidebar.selectbox('Ação', acoes_ibov)
        analise_diaria.visualiza_indicador_diario(eixo_y=visualizar_acao, descricao_indicador=visualizar_acao)
    if indicador == 'Indexadores':
        st.text(descricao[indexador][0])
    st.markdown('Repositório no [GitHub](https://github.com/MarcosRMG/Investimentos)')
    
if __name__ == '__main__':
    main()
