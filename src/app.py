import streamlit as st
import pandas as pd
from datetime import date, timedelta
from catch_clean import carteira_ibov
from catch_clean import BrazilianIndicators
from analysis import DataAnalysis, AnalysisSeriesMontly, StockPriceViz, request_data
import streamlit as st
import pandas as pd
from screens.economic_index import brazil_economic_index


#============================================IBOVESPA Indexers===========================================
carteira = carteira_ibov('./data/carteira_ibov.csv', cols=['Código']).copy()
year_before_date = date.today() - timedelta(days=365)

#============================================Economy indexers============================================
data = BrazilianIndicators()
data.clean_data_bcb()
data.clean_data_ibge()
data = data.data_frame_indicators()


def main():
    st.set_page_config(layout='wide')
    option_view = ['Série Temporal', 'Candlestick', 'Decomposição', 'Histograma', 'Boxplot', 'Estatística Descritiva', 
                    'Correlação']
    st.title('Mercado Financeiro')
    st.sidebar.selectbox('País', ['Brasil'])
    indicators = ['Índices Econômicos', 'Ações IBOVESPA']
    indicator = st.sidebar.selectbox('Indicadores', indicators)
    # ============================Economics indices visualizations============================
    if indicator == 'Índices Econômicos':
        brazil_economic_index(data)
    # ============================Stocks prices visualizations============================
    elif indicator == 'Ações IBOVESPA':
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
            elif view == 'Correlação':
                st.subheader('Correlação Linear')
                stock_viz.correlation()
        else:
            st.write('Selecione uma opção!')
    if indicator == 'Índices':
        for index in indexer:
            st.text(description[index][0])
    st.markdown('[GitHub](https://github.com/MarcosRMG/Investments)')
    st.markdown('Version 1.7.2')

    
if __name__ == '__main__':
    main()
