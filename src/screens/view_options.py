import streamlit as st
import pandas as pd
import numpy as np
from datetime import timedelta, datetime


def visualizations(analyzer: object, view: str, check: bool):
        # Define start year
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
    return ['Série Temporal', 'Sazonalidade e Tendência', 'Histograma', 'Boxplot', 'Barplot', 
            'Estatística Descritiva', 'Correlação Linear']


def date_interval(view: str): 
    year_before_today = datetime.today() - timedelta(days=365)
    if view == 'Sazonalidade e Tendência': 
        # Ensure 24 months to calculate seasonality
        year_before_today -= timedelta(days=365)  
        # Ensure to get first day of month
        year_before_today -= timedelta(days=datetime.today().day - 1)


    initial_date = pd.to_datetime(st.sidebar.date_input('Data inicial', year_before_today))
    end_date = pd.to_datetime(st.sidebar.date_input('Data final', datetime.today()))
    
    return initial_date, end_date
    