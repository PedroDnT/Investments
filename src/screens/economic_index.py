import streamlit as st
import pandas as pd
from data_viz.analysis_series import AnalysisSeries
from screens.view_options import visualizations, view_list, date_interval


def economic_index_screen(data: pd.DataFrame):
    '''
    This function create the screen of Brazilian Economic Index. 

    Parameters: data : Pandas DataFrame 
                    DataFrame with historical index data downloaded from IBGE and Banco Central do Brasil
    '''
    # variables definition
    indexers = ['Poupança', 'CDI', 'IPCA', 'INPC', 'Selic']
    option_view_indexes = view_list()
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
        # Define date interval
        start_date, end_date = date_interval(view=view)
        if indexer == 'Selecionar todos':
            indexer = ['Poupança', 'CDI', 'IPCA', 'INPC', 'Selic']
        analyze = AnalysisSeries(data=data, start_date=start_date, end_date=end_date, axis_y=indexer)
        # This variable avoid unecessary view check inside visualization function
        check_other_options = True
        if view == 'Série Temporal':
            check_other_options = False
            st.subheader('Série Temporal')
            analyze.time_series()
            analyze.acumulated()
        # Other options
        visualizations(analyzer=analyze, view=view, check=check_other_options)
        if view != 'Correlação Linear':
            st.table(description[description.index.isin(indexer)])
        elif view == 'Correlação Linear' and len(indexer) > 1:
            st.table(description[description.index.isin(indexer)])
    else:
        st.write('Selecione um índice!')
