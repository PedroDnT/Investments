import streamlit as st
import pandas as pd
from data_viz.stock_price_viz import StockPriceViz 
from etl.catch_clean import request_data
from screens.view_options import visualizations, view_list, date_interval


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
    # Screen flow
    visualize_stocks = st.sidebar.multiselect('Stocks', carteira['código'].values, default='AMBEV S/A')
    selected_tickers = carteira[carteira['código'].isin(visualize_stocks)]['index'].tolist()
    # Date range definition
    if visualize_stocks:
        # Select the visualization type option
        view = st.sidebar.selectbox('Gráfico', option_view)
        # Define date interval
        start_date, end_date = date_interval(view=view)
        # Download data from Yahoo Finance
        stock_data = request_data(selected_tickers, start_date)
        stock_viz = StockPriceViz(stock_data, start_date, end_date, selected_tickers)
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
