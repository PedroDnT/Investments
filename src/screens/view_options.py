import streamlit as st
import numpy as np


def visualizations(analyzer: object, view: str, check: bool):
        # Define start year
        if check:
            if view == 'Sazonalidade e Tendência':
                st.subheader('Sazonalidade e Tendência')
                analyzer.serie_decomposition()
            elif view == 'Histograma':
                st.subheader('Distribuição')
                try:
                    analyzer.histogram_view()
                except:
                    analyzer.histogram_view('R$')
            elif view == 'Boxplot':
                st.subheader('Boxplot')
                try:
                    analyzer.boxplot_view()
                except:
                    analyzer.boxplot_view('R$')
            elif view == 'Barplot':
                function_dict = {'Soma': np.sum, 'Média': np.mean}
                agg = st.selectbox('Período', ['Ano', 'Trimestre', 'Mês'])
                function = st.selectbox('Função', function_dict.keys())
                st.subheader('Barplot')
                try:
                    analyzer.barplot_view(aggregation=agg, function=function_dict[function])
                except:
                    analyzer.barplot_view(y_label='R$', aggregation=agg, function=function_dict[function])
            elif view == 'Estatística Descritiva':
                st.subheader('Estatística Descritiva')
                analyzer.descriptive_statistics()
            elif view == 'Correlação Linear':
                st.subheader('Correlação Linear')
                analyzer.correlation()

def view_list():
    return ['Série Temporal', 'Sazonalidade e Tendência', 'Histograma', 'Boxplot', 'Barplot', 
            'Estatística Descritiva', 'Correlação Linear']