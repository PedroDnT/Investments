import streamlit as st
import pandas as pd
import numpy as np
from datetime import timedelta, datetime


def visualizations(analyzer: object, view: str, check: bool):
    '''
    Show the visualizations options common to all indicators 

    Parameters: analyzer : Object 
                    Class with visualizations to be showed
    
                view: String
                    Selected view option

                check: Boolean
                    To avoid unnecessary checking if the selected view is not available here

    Returns: Plotly Chart
                Plotly chart of selected view
    '''
    if check:
        if view == 'Sazonalidade e Tendência':
            st.subheader('Sazonalidade e Tendência')
            analyzer.serie_decomposition()
        elif view == 'Histograma':
            st.subheader('Distribuição')
            analyzer.histogram_view()
        elif view == 'Boxplot':
            st.subheader('Boxplot')
            analyzer.boxplot_view()
        elif view == 'Barplot':
        # Aggregation options
            function_dict = {'Soma': np.sum, 'Média': np.mean}
            agg = st.selectbox('Período', ['Ano', 'Trimestre', 'Mês'])
            function = st.selectbox('Função', function_dict.keys())
            st.subheader('Barplot')
            analyzer.barplot_view(aggregation=agg, function=function_dict[function])
        elif view == 'Estatística Descritiva':
            st.subheader('Estatística Descritiva')
            analyzer.descriptive_statistics()
        elif view == 'Correlação Linear':
            st.subheader('Correlação Linear')
            analyzer.correlation()

def view_list():
    '''
    List of generalized view 

    Returns: List
                List with view options common to all analyzer
    '''
    return ['Série Temporal', 'Sazonalidade e Tendência', 'Histograma', 'Boxplot', 'Barplot', 
            'Estatística Descritiva', 'Correlação Linear']


def date_interval(view: str): 
    '''
    Define the initial and final date selected to analyze data

    Parameters: view : String
                    Selected view to increase the initial date plus 365 days if "Seanalidade e Tendência" 
                    was selected otherwise 365 before is predefined as default period

    Returns: initial_date : Pandas datetime
                Initial date
             end_date : Pandas datetime
                Final date
    '''
    year_before_today = datetime.today() - timedelta(days=365)
    if view == 'Sazonalidade e Tendência': 
        # Ensure 24 months to calculate seasonality
        year_before_today -= timedelta(days=365)  
        # Ensure to get first day of month
        year_before_today -= timedelta(days=datetime.today().day - 1)


    initial_date = pd.to_datetime(st.sidebar.date_input('Data inicial', year_before_today))
    end_date = pd.to_datetime(st.sidebar.date_input('Data final', datetime.today()))
    
    return initial_date, end_date
    