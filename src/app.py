import streamlit as st
import pandas as pd
from datetime import datetime
from catch_clean import carteira_ibov
from catch_clean import BrazilianIndicators
from analysis import AnalysisSeriesMontly, StockPriceViz, request_data
import streamlit as st
import pandas as pd


carteira = carteira_ibov('./data/carteira_ibov.csv', cols=['Código']).copy()

data = BrazilianIndicators()
data.clean_data_bcb()
data.clean_data_ibge()
data = data.data_frame_indicators()
# Indexers description
description = pd.DataFrame({'Savings': ['SAVINGS: Profitability on the 1st day of the month (BCB-Demab)'],
                            'CDI': ['CDI: Monthly Accumulated Interest Rate (BCB-Demab)'],
                            'IPCA': ['IPCA: Covers families with income from 1 to 40 minimum wages (IBGE)'],
                            'INPC': ['INPC: Covers families with income from 1 a 5 minimum wages (IBGE)'],
                            'Selic': ['Selic: Monthly Accumulated Interest Rate (BCB-Demab)']})

def main():
    st.set_page_config(layout='wide')
    indexers = ['Savings', 'CDI', 'IPCA', 'INPC', 'Selic']
    option_view = ['Time Series', 'Candle', 'Histogram', 'Descriptive Statistics']
    option_view_indexes = ['Time Series', 'Correlation']
    st.markdown("<h1 style='text-align: right; font-size: 15px; font-weight: normal'>Version 1.5</h1>", 
                unsafe_allow_html=True)
    st.title('Financial Data Analysis')
    st.sidebar.selectbox('Country', ['Brazil'])
    indicators = ['Indexers', 'Stocks']
    indicator = st.sidebar.selectbox('Indicator', indicators)
    # ============================Economics indices visualizations============================
    if indicator == 'Indexers':
        st.subheader('Brazilian Economic Indices')
        start_year = str(st.sidebar.selectbox('Start Year', sorted(data['date'].dt.year.unique(), reverse=True)))
        all = st.sidebar.checkbox('Select all')
        if all:
            indexer = st.sidebar.multiselect('Indexer', indexers, default=indexers)
        else:
            indexer = st.sidebar.multiselect('Indexer', indexers, default=['Savings'])
        # Time series of indexers
        if indexer:
            # View options
            view = st.sidebar.selectbox('View', option_view_indexes)
            # Data range
            if indexer == 'All':
                indexer = ['Savings', 'CDI', 'IPCA', 'INPC', 'Selic']
            analyze = AnalysisSeriesMontly(data, start_year, indexer)
            if view == 'Time Series':
                analyze.visualize_indicator()
                analyze.acumulated()
            elif view == 'Correlation':
                analyze.correlation()
        else:
            st.write('Please select a indexer!')
    # ============================Stocks prices visualizations============================
    elif indicator == 'Stocks':
        start_date = str(st.sidebar.date_input('Initial Date', datetime(2022, 1, 1)))
        visualize_stocks = st.sidebar.multiselect('Stocks', carteira['código'].values, default='AMBEV S/A')
        selected_tickers = carteira[carteira['código'].isin(visualize_stocks)]['index'].tolist()
        if visualize_stocks:
            # Select the visualization type option
            view = st.sidebar.selectbox('View', option_view)
            # Download data from Yahoo Finance
            stock_data = request_data(selected_tickers, start_date)
            stock_viz = StockPriceViz(data=stock_data, tickers=selected_tickers)
            if view == 'Candle':  
                # Show selected visualization
                st.subheader('Brazilian Stock Price')
                stock_viz.candlestick()
            if view == 'Time Series':
                st.subheader('Time Series Stock Price')
                stock_viz.time_series()
            elif view == 'Histogram':
                # Show selected visualization
                st.subheader('Histogram Stock Price')
                stock_viz.histogram_view()
            elif view == 'Descriptive Statistics':
                st.subheader('Descriptive Statistics')
                stock_viz.descriptive_statistics()
        else:
            st.write('Please select a stock option!')
    if indicator == 'Indexers':
        for index in indexer:
            st.text(description[index][0])
    st.markdown('[GitHub](https://github.com/MarcosRMG/Investimentos)')

if __name__ == '__main__':
    main()
