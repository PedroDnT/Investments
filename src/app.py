import streamlit as st
from etl.catch_clean import carteira_ibov
from etl.catch_clean import BrazilianIndicators
from screens.economic_index import economic_index_screen
from screens.stock_price import stock_price_screen
from screens.funds import funds_screen
from etl.catch_clean import read_fund_data


#============================================IBOVESPA Indexers===========================================
carteira = carteira_ibov('./data/carteira_ibov.csv', cols=['Código']).copy()

#============================================Economy indexers============================================
data = BrazilianIndicators()
data.clean_data_bcb()
data.clean_data_ibge()
data = data.data_frame_indicators() 


def main():
    # Header
    st.set_page_config(layout='wide')
    st.title('Mercado Financeiro')
    st.sidebar.selectbox('País', ['Brasil'])
    indicators = ['Índices Econômicos', 'Fundos', 'Ações IBOVESPA']
    indicator = st.sidebar.selectbox('Indicadores', indicators)
    # Screens options
    # ============================Economics indices visualizations============================
    if indicator == 'Índices Econômicos':
        economic_index_screen(data)
    # ============================Stocks prices visualizations============================
    elif indicator == 'Ações IBOVESPA':
        stock_price_screen(carteira)
    elif indicator == 'Fundos':
        df_funds = read_fund_data('https://bitbucket.org/marcos_rmg/largedata/raw/65a1af3d452651c9775ba8538e49d59ce0c1b38b/fundos.csv')
        funds_screen(df_funds)

    # Footer
    st.markdown('[GitHub](https://github.com/MarcosRMG/Investments)')
    st.markdown('Version 1.8.2')

    
if __name__ == '__main__':
    main()
