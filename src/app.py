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
ibov.set_index('date', inplace=True)
# Indexers description
description = pd.DataFrame({'Savings': ['SAVINGS: Profitability on the 1st day of the month (BCB-Demab)'],
                            'CDI': ['CDI: Monthly Accumulated Interest Rate (BCB-Demab)'],
                            'IPCA': ['IPCA: Covers families with income from 1 to 40 minimum wages (IBGE)'],
                            'INPC': ['INPC: Covers families with income from 1 a 5 minimum wages (IBGE)'],
                            'Selic': ['Selic: Monthly Accumulated Interest Rate (BCB-Demab)']})

def main():
    stocks_ibov = ibov.columns
    indexers = ['Savings', 'CDI', 'IPCA', 'INPC', 'Selic']
    # Visualização gráfica
    st.markdown("<h1 style='text-align: right; font-size: 15px; font-weight: normal'>Version 1.1</h1>", 
                unsafe_allow_html=True)
    st.title('Brazilian Investments Analysis')
    indicators = ['Indexers', 'Stocks']
    indicator = st.sidebar.selectbox('Indicator', indicators)
    if indicator == 'Indexers':
        anos = data['date'].dt.year.unique().tolist()
        period = st.sidebar.slider('Select the period', min_value=min(anos), max_value=max(anos), value=(min(anos), max(anos)))
        indexer = st.sidebar.selectbox('Indexer', indexers)
        analyze = AnalysisSeriesMontly(data, period)
        analyze.visualize_indicator(axis_y=indexer, description_indicator=indexer)
    elif indicator == 'Stocks':
        initial_date = st.sidebar.date_input('Initial Date', ibov.index.min())
        final_date = st.sidebar.date_input('Final Date', ibov.index.max())
        analysis_daily = AnalysisSerieDaily(ibov, initial_date, final_date)
        visualize_stocks = st.sidebar.selectbox('Stocks', stocks_ibov)
        analysis_daily.visualize_indicator_daily(visualize_stocks, visualize_stocks)
    if indicator == 'Indexers':
        st.text(description[indexer][0])
    st.markdown('[GitHub repository](https://github.com/MarcosRMG/Investimentos)')
    
if __name__ == '__main__':
    main()
