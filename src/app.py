from catch_clean import BrazilianIndicators
from analysis import AnalysisSeriesMontly, AnalysisSerieDaily
import streamlit as st
import pandas as pd


data = BrazilianIndicators()
data.clean_data_bcb()
data.clean_data_ibge()
data = data.data_frame_indicators()
ibov = pd.read_csv('./data/ibov.csv')
ibov['date'] = pd.to_datetime(ibov['date'])
# Indexers description
description = pd.DataFrame({'Savings': ['SAVINGS: Profitability on the 1st day of the month (BCB-Demab)'],
                            'CDI': ['CDI: Monthly Accumulated Interest Rate (BCB-Demab)'],
                            'IPCA': ['IPCA: Covers families with income from 1 to 40 minimum wages (IBGE)'],
                            'INPC': ['INPC: Covers families with income from 1 a 5 minimum wages (IBGE)'],
                            'Selic': ['Selic: Monthly Accumulated Interest Rate (BCB-Demab)']})

def main():
    st.set_page_config(layout='wide')
    stocks_ibov = ibov.columns[1:]
    indexers = ['Savings', 'CDI', 'IPCA', 'INPC', 'Selic']
    st.markdown("<h1 style='text-align: right; font-size: 15px; font-weight: normal'>Version 1.3</h1>", 
                unsafe_allow_html=True)
    st.title('Financial Data Analysis')
    st.sidebar.selectbox('Country', ['Brazil'])
    indicators = ['Indexers', 'Stocks']
    indicator = st.sidebar.selectbox('Indicator', indicators)
    if indicator == 'Indexers':
        start_year = str(st.sidebar.selectbox('Start Year', sorted(data['date'].dt.year.unique(), reverse=True)))
        indexer = st.sidebar.multiselect('Indexer', indexers, default=['Savings'])
        analyze = AnalysisSeriesMontly(data, start_year)
        analyze.visualize_indicator(indexer)
        analyze.acumulated(indexer)
    elif indicator == 'Stocks':
        start_date = str(st.sidebar.date_input('Initial Date', ibov['date'].min()))
        analysis_daily = AnalysisSerieDaily(ibov, start_date)
        visualize_stocks = st.sidebar.multiselect('Stocks', stocks_ibov, default='Price ABEV3.SA')
        normalize = st.sidebar.checkbox('Normalize')
        if normalize:
            analysis_daily.normalize_time_series(visualize_stocks)
            analysis_daily.visualize_serie_normalized(visualize_stocks)
            analysis_daily.normalized_metric(visualize_stocks)
        else:
            analysis_daily.visualize_indicator_daily(visualize_stocks)
            analysis_daily.valorization_metric(visualize_stocks)
    if indicator == 'Indexers':
        for index in indexer:
            st.text(description[index][0])
    st.markdown('[GitHub](https://github.com/MarcosRMG/Investimentos)')
    
if __name__ == '__main__':
    main()
