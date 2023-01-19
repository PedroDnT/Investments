import pandas as pd
import streamlit as st
from data_viz.analysis import AnalysisSeries
from datetime import date, timedelta
from screens.view_options import visualizations, view_list, date_interval


def funds_screen(data: pd.DataFrame()):
    indicator_dict = {'Valor Cota': ['vl_quota', 'R$'], 'Patrimônio Líquido': ['vl_patrim_liq', 'R$'], 
                    'Captação Dia': ['captc_dia', 'R$'], 'Resgate Dia': ['resg_dia', 'R$'], 
                    'Cotistas': ['nr_cotst', 'Nº'], 'Valor total da carteira': ['vl_total', 'R$']}
    # Filters data definition
    fund_filter = st.sidebar.selectbox('Buscar por', ['Denominção Social', 'CNPJ'])
    if fund_filter == 'Denominção Social':
        fund_selected = st.sidebar.multiselect(label='Denominação Social', 
                                                options=data['denom_social'].unique(), 
                                                default=data['denom_social'].unique()[0])
    elif fund_filter == 'CNPJ':
        fund_selected = st.sidebar.multiselect(label='CNPJ', 
                                                options=data['cnpj_fundo'].unique(), 
                                                default=data['cnpj_fundo'].unique()[0])
    # Visualization options
    indicator = st.sidebar.selectbox(label='Indicador', options=indicator_dict.keys())
    # Data slice and pivot: fund and indicator
    if fund_filter == 'Denominção Social':
        # Slice found
        data_slice = data[data['denom_social'].isin(fund_selected)].copy()
        # Select indicator
        data_slice = data_slice[['date', 'denom_social', indicator_dict[indicator][0]]]
        # Data pivot
        data_pivot = data_slice.pivot(index='date', columns='denom_social', 
                                        values=indicator_dict[indicator][0]).reset_index()
    elif fund_filter == 'CNPJ':
        # Slice found
        data_slice = data[data['cnpj_fundo'].isin(fund_selected)].copy()
        data_slice = data_slice[['date', 'denom_social', indicator_dict[indicator][0]]]  
        # Data pivot 
        data_pivot = data_slice.pivot(index='date', columns='denom_social', 
                                        values=indicator_dict[indicator][0]).reset_index()
    if fund_selected:
        # Data Viz
        # Date definition (One Year before as default)
        view_options_list = view_list()
        view = st.sidebar.selectbox('Gráfico', view_options_list)
        # Date interval
        start_date, end_date = date_interval(view=view)
        # View options
        analyze = AnalysisSeries(data=data_pivot, start_date=start_date, end_date=end_date, 
                                axis_y=data_pivot.columns[1:], y_label=indicator_dict[indicator][1])
        # This variable avoid unecessary view check inside visualization function
        check_other_options = True
        if view == 'Série Temporal':
            check_other_options = False
            normalization = st.sidebar.checkbox('Normalizar')
            if normalization:
                st.subheader(indicator)
                analyze.normalize_time_series()
                analyze.time_series(legend_x_position=0, legend_y_position=1.2)
                analyze.normalized_metric()
            else:
                st.subheader(indicator)
                analyze.time_series(legend_x_position=0, legend_y_position=1.2)
        # Others options
        visualizations(analyzer=analyze, view=view, check=check_other_options)

    else:
        st.write('Selecione um fundo de investimento!')
