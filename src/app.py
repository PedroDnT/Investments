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
    stocks_ibov = ibov.columns
    indexers = ['Savings', 'CDI', 'IPCA', 'INPC', 'Selic']
    st.markdown("<h1 style='text-align: right; font-size: 15px; font-weight: normal'>Version 1.2</h1>", 
                unsafe_allow_html=True)
    st.title('Brazilian Investments Analysis')
    indicators = ['Indexers', 'Stocks']
    indicator = st.sidebar.selectbox('Indicator', indicators)
    if indicator == 'Indexers':
        start_year = str(st.sidebar.selectbox('Start Year', data['date'].dt.year.unique()))
        indexer = st.sidebar.multiselect('Indexer', indexers, default=['Savings'])
        analyze = AnalysisSeriesMontly(data, start_year)
        analyze.visualize_indicator(indexer)
    elif indicator == 'Stocks':
        start_date = str(st.sidebar.date_input('Initial Date', ibov['date'].min()))
        analysis_daily = AnalysisSerieDaily(ibov, start_date)
        visualize_stocks = st.sidebar.multiselect('Stocks', stocks_ibov, default='Price ABEV3.SA')
        analysis_daily.visualize_indicator_daily(visualize_stocks)
    if indicator == 'Indexers':
        for index in indexer:
            st.text(description[index][0])
    st.markdown('[GitHub repository](https://github.com/MarcosRMG/Investimentos)')
    
if __name__ == '__main__':
    main()
