import streamlit as st
import pandas as pd
from datetime import date, timedelta
from analysis import StockPriceViz, request_data


def stock_price_screen(carteira: pd.DataFrame):
    '''
    --> This function create the screen of Brazilian Stock Price. 

    Parameters: carteira : Pandas DataFrame 
                    DataFrame with ticket companies listed on IBOVESPA
    '''
    # Auxiliar variables
    option_view = ['Série Temporal', 'Candlestick', 'Decomposição', 'Histograma', 'Boxplot', 'Estatística Descritiva', 
                    'Correlação Linear']
    year_before_date = date.today() - timedelta(days=365)
    # Screen flow
    visualize_stocks = st.sidebar.multiselect('Stocks', carteira['código'].values, default='AMBEV S/A')
    selected_tickers = carteira[carteira['código'].isin(visualize_stocks)]['index'].tolist()
    if visualize_stocks:
        # Select the visualization type option
        view = st.sidebar.selectbox('Gráfico', option_view)
        # Define start date
        if view == 'Decomposição':
            # Ensure two years to calculate decomposition
            start_date = str(st.sidebar.date_input('Data inicial', year_before_date - timedelta(days=365)))
        else:
            start_date = str(st.sidebar.date_input('Data inicial', year_before_date))
        # Download data from Yahoo Finance
        stock_data = request_data(selected_tickers, start_date)
        stock_viz = StockPriceViz(stock_data, selected_tickers)
        if view == 'Candlestick':  
            # Show selected visualization
            st.subheader('Cotação de Preço')
            stock_viz.candlestick()
        elif view == 'Série Temporal':
            normalization = st.sidebar.checkbox('Normalizar')
            if normalization:
                st.subheader('Preço de Fechamento Normalizado')
                stock_viz.normalize_time_series()
                stock_viz.time_series()
                stock_viz.normalized_metric()
            else:
                st.subheader('Preço de Fechamento')
                stock_viz.time_series()
        elif view == 'Decomposição':
            st.subheader('Sazonalidade e Tendência')
            stock_viz.serie_decomposition()
        elif view == 'Histograma':
            # Show selected visualization
            st.subheader('Preço de Fechamento')
            stock_viz.histogram_view(x_label='R$')
        elif view == 'Boxplot':
            # Show selected visualization
            st.subheader('Preço de Fechamento')
            stock_viz.boxplot_view(y_label='R$')
        elif view == 'Estatística Descritiva':
            st.subheader('Estatística Descritiva')
            stock_viz.descriptive_statistics()
        elif view == 'Correlação Linear':
            st.subheader('Correlação Linear')
            stock_viz.correlation()
    else:
        st.write('Selecione uma opção!')