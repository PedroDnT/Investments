import streamlit as st
import pandas as pd
from data_viz.analysis import AnalysisSeries


def economic_index_screen(data: pd.DataFrame):
    '''
    --> This function create the screen of Brazilian Economic Index. 

    Parameters: data : Pandas DataFrame 
                    DataFrame with historical index data downloaded from IBGE and Banco Central do Brasil
    '''
    # variables definition
    indexers = ['Poupança', 'CDI', 'IPCA', 'INPC', 'Selic']
    option_view_indexes = ['Série Temporal', 'Decomposição', 'Histograma', 'Boxplot', 'Barplot', 'Estatística Descritiva', 
                            'Correlação Linear']
    # Available data years
    years_list = sorted(data['date'].dt.year.unique(), reverse=True)
    # Auxiliar variables to apply data filter on app inicialization
    # One year before of available data
    # 12 months before data available
    year_before = data.sort_values('date', ascending=False)[:12]['date'].reset_index(drop=True)[11]
    ref_year = year_before.year
    # The month of one year before of available data
    ref_month = year_before.month
    # Years list
    years_list = sorted(data['date'].dt.year.unique(), reverse=True)
    # Year ref index
    year_index = years_list.index(ref_year)
    # Months label to filter data
    months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    months_dict = {'Jan': '01', 'Fev': '02', 'Mar': '03', 'Abr': '04', 'Mai': '05', 'Jun': '06', 'Jul': '07', 'Ago': '08', 
                'Set': '09', 'Out': '10', 'Nov': '11', 'Dez': '12'}

    # Indexers description
    description = pd.DataFrame({'Indicador': ['Rentabilidade no 1º dia do mês (BCB-Demab)', 
                                        'Taxa de Juros Acumulada Mensal (BCB-Demab)', 
                                        'Abrange famílias com renda de 1 a 40 salários mínimos (IBGE)',
                                        'Abrange famílias com renda de 1 a 5 salários mínimos (IBGE)',
                                        'Taxa de Juros Acumulada Mensal (BCB-Demab)']}, 
                                        index=['Poupança', 'CDI', 'IPCA', 'INPC', 'Selic'])
    # All indexers options screen
    all_ = st.sidebar.checkbox('Selecionar todos')
    if all_:
        indexer = st.sidebar.multiselect('Índice', indexers, default=indexers)
    else:
        indexer = st.sidebar.multiselect('Índice', indexers, default=['Poupança'])
    # Time series of indexers
    if indexer:
        # View options
        view = st.sidebar.selectbox('Gráfico', option_view_indexes)
        # Define start year
        if view == 'Decomposição':
            # Ensures two years before
            start_year = str(st.sidebar.selectbox('Ano inicial', years_list, index=year_index + 1))
        else:
            start_year = str(st.sidebar.selectbox('Ano inicial', years_list, index=year_index))
        # Difine start month
        start_month = st.sidebar.selectbox('Mês inicial', months, index=ref_month - 1)
        # Start Year/ month definition 
        start_year_month = start_year + '-' + months_dict[start_month] + '-01' 
        # Data range
        if indexer == 'Selecionar todos':
            indexer = ['Poupança', 'CDI', 'IPCA', 'INPC', 'Selic']
        analyze = AnalysisSeries(data=data, axis_y=indexer, start_date=start_year_month)
        if view == 'Série Temporal':
            st.subheader('Série Temporal')
            analyze.time_series()
            analyze.acumulated()
        elif view == 'Decomposição':
            st.subheader('Sazonalidade e Tendência')
            analyze.serie_decomposition()
        elif view == 'Histograma':
            st.subheader('Distribuição')
            analyze.histogram_view()
        elif view == 'Boxplot':
            st.subheader('Boxplot')
            analyze.boxplot_view()
        elif view == 'Barplot':
            st.subheader('Barplot')
            analyze.barplot_view()
        elif view == 'Estatística Descritiva':
            st.subheader('Estatística Descritiva')
            analyze.descriptive_statistics()
        elif view == 'Correlação Linear':
            st.subheader('Correlação Linear')
            analyze.correlation()
        # Indicator source description
        if view != 'Correlação Linear':
            st.table(description[description.index.isin(indexer)])
        elif view == 'Correlação Linear' and len(indexer) > 1:
            st.table(description[description.index.isin(indexer)])
    else:
        st.write('Selecione um índice!')