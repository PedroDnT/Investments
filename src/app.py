import streamlit as st
from catch_clean import carteira_ibov
from catch_clean import BrazilianIndicators
from screens.economic_index import economic_index_screen
from screens.stock_price import stock_price_screen


#============================================IBOVESPA Indexers===========================================
carteira = carteira_ibov('./data/carteira_ibov.csv', cols=['Código']).copy()

#============================================Economy indexers============================================
data = BrazilianIndicators()
data.clean_data_bcb()
data.clean_data_ibge()
data = data.data_frame_indicators()


def main():
    # Global menu
    st.set_page_config(layout='wide')
    st.title('Mercado Financeiro')
    st.sidebar.selectbox('País', ['Brasil'])
    indicators = ['Índices Econômicos', 'Ações IBOVESPA']
    indicator = st.sidebar.selectbox('Indicadores', indicators)
    # ============================Economics indices visualizations============================
    if indicator == 'Índices Econômicos':
        economic_index_screen(data)
    # ============================Stocks prices visualizations============================
    elif indicator == 'Ações IBOVESPA':
        stock_price_screen(carteira)
    st.markdown('[GitHub](https://github.com/MarcosRMG/Investments)')
    st.markdown('Version 1.7.2')

    
if __name__ == '__main__':
    main()
