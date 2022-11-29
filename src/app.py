import streamlit as st
import pandas as pd
from datetime import datetime
from catch_clean import carteira_ibov
from catch_clean import BrazilianIndicators
from analysis import DataAnalysis, AnalysisSeriesMontly, StockPriceViz, request_data
import streamlit as st
import pandas as pd


carteira = carteira_ibov('./data/carteira_ibov.csv', cols=['Código']).copy()

data = BrazilianIndicators()
data.clean_data_bcb()
data.clean_data_ibge()
data = data.data_frame_indicators()
# Indexers description
description = pd.DataFrame({'Poupança': ['Poupança: Rentabilidade no 1º dia do mês (BCB-Demab)'],
                            'CDI': ['CDI: Taxa de Juros Acumulada Mensal (BCB-Demab)'],
                            'IPCA': ['IPCA: Abrange famílias com renda de 1 a 40 salários mínimos (IBGE)'],
                            'INPC': ['INPC: Abrange famílias com renda de 1 a 5 salários mínimos (IBGE)'],
                            'Selic': ['Selic: Taxa de Juros Acumulada Mensal (BCB-Demab)']})

def main():
    st.set_page_config(layout='wide')
    indexers = ['Poupança', 'CDI', 'IPCA', 'INPC', 'Selic']
    option_view = ['Série Temporal', 'Candlestick', 'Histograma', 'Estatística Descritiva', 'Correlação']
    option_view_indexes = ['Série Temporal', 'Histograma', 'Estatística Descritiva', 'Correlação']
    st.title('Análise do Mercado Financeiro')
    st.sidebar.selectbox('País', ['Brasil'])
    indicators = ['Índices Econômicos', 'Ações IBOVESPA']
    indicator = st.sidebar.selectbox('Indicadores', indicators)
    # ============================Economics indices visualizations============================
    if indicator == 'Índices Econômicos':
        start_year = str(st.sidebar.selectbox('Ano inicial', sorted(data['date'].dt.year.unique(), reverse=True)))
        all = st.sidebar.checkbox('Selecionar todos')
        if all:
            indexer = st.sidebar.multiselect('Índice', indexers, default=indexers)
        else:
            indexer = st.sidebar.multiselect('Índice', indexers, default=['Poupança'])
        # Data read
        #economic_data = DataAnalysis(data, indexer)
        # Time series of indexers
        if indexer:
            # View options
            view = st.sidebar.selectbox('Gráfico', option_view_indexes)
            # Data range
            if indexer == 'Selecionar todos':
                indexer = ['Poupança', 'CDI', 'IPCA', 'INPC', 'Selic']
            analyze = AnalysisSeriesMontly(data=data, axis_y=indexer, start_date=start_year)
            if view == 'Série Temporal':
                st.subheader('Série Temporal')
                analyze.visualize_indicator()
                analyze.acumulated()
            elif view == 'Histograma':
                st.subheader('Distribuição')
                analyze.histogram_view(indexer, 'indice', '%')
            elif view == 'Estatística Descritiva':
                st.subheader('Estatística Descritiva')
                analyze.descriptive_statistics()
            elif view == 'Correlação':
                st.subheader('Correlação Linear')
                analyze.correlation()
        else:
            st.write('Selecione um índice!')
    # ============================Stocks prices visualizations============================
    elif indicator == 'Ações IBOVESPA':
        start_date = str(st.sidebar.date_input('Data inicial', datetime(2022, 1, 1)))
        visualize_stocks = st.sidebar.multiselect('Stocks', carteira['código'].values, default='AMBEV S/A')
        selected_tickers = carteira[carteira['código'].isin(visualize_stocks)]['index'].tolist()
        if visualize_stocks:
            # Select the visualization type option
            view = st.sidebar.selectbox('Gráfico', option_view)
            # Download data from Yahoo Finance
            stock_data = request_data(selected_tickers, start_date)
            stock_viz = StockPriceViz(stock_data, selected_tickers)
            if view == 'Candlestick':  
                # Show selected visualization
                st.subheader('Cotação de preço')
                stock_viz.candlestick()
            if view == 'Série Temporal':
                st.subheader('Histórico do preço de fechamento')
                stock_viz.time_series()
            elif view == 'Histograma':
                # Show selected visualization
                st.subheader('Distribuição do preço de fechamento')
                stock_viz.histogram_view('Close', 'company', 'R$')
            elif view == 'Estatística Descritiva':
                st.subheader('Estatística Descritiva')
                stock_viz.descriptive_statistics()
            elif view == 'Correlação':
                st.subheader('Correlação Linear')
                stock_viz.correlation()
        else:
            st.write('Selecione uma opção!')
    if indicator == 'Índices':
        for index in indexer:
            st.text(description[index][0])
    st.markdown('[GitHub](https://github.com/MarcosRMG/Investimentos)')
    st.markdown('Version 1.6')
if __name__ == '__main__':
    main()
