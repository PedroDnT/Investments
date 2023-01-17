import streamlit as st
import pandas as pd
from datetime import date, timedelta
from data_viz.analysis import StockPriceViz 
from etl.catch_clean import request_data
from screens.view_options import visualizations, view_list


def stock_price_screen(carteira: pd.DataFrame):
    '''
    --> This function create the screen of Brazilian Stock Price. 

    Parameters: carteira : Pandas DataFrame 
                    DataFrame with ticket companies listed on IBOVESPA
    '''
    # Auxiliar variables
    option_view = view_list()
    # Insert extra view
    option_view.insert(1, 'Candlestick')
    year_before_date = date.today() - timedelta(days=365)
    # Screen flow
    visualize_stocks = st.sidebar.multiselect('Stocks', carteira['código'].values, default='AMBEV S/A')
    selected_tickers = carteira[carteira['código'].isin(visualize_stocks)]['index'].tolist()
    if visualize_stocks:
        # Select the visualization type option
        view = st.sidebar.selectbox('Gráfico', option_view)
        # Define start date
        if view == 'Sazonalidade e Tendência' or 'Barplot':
            # Ensure two years to calculate decomposition
            start_date = str(st.sidebar.date_input('Data inicial', year_before_date - timedelta(days=365)))
        else:
            start_date = str(st.sidebar.date_input('Data inicial', year_before_date))
        # Download data from Yahoo Finance
        stock_data = request_data(selected_tickers, start_date)
        stock_viz = StockPriceViz(stock_data, selected_tickers)
        # This variable avoid unecessary view check inside visualization function
        check_other_options = True
        if view == 'Candlestick': 
            check_other_options = False 
            # Show selected visualization
            st.subheader('Cotação de Preço')
            stock_viz.candlestick()
        elif view == 'Série Temporal':
            check_other_options = False
            normalization = st.sidebar.checkbox('Normalizar')
            if normalization:
                st.subheader('Preço de Fechamento Normalizado')
                stock_viz.normalize_time_series()
                stock_viz.time_series()
                stock_viz.normalized_metric()
            else:
                st.subheader('Preço de Fechamento')
                stock_viz.time_series()
        # Other options
        visualizations(analyzer=stock_viz, view=view, check=check_other_options)
    else:
        st.write('Selecione uma opção!')