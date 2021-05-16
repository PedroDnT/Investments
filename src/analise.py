import plotly.express as px
import streamlit as st


class SerieTemporal:
    '''
    --> Apresenta a série temporal dos investimentos analisados
    '''
    def __init__(self, investimento):
        '''
        :param investimento: Série temporal do investimento
        '''
        self._investimento = investimento
    
    
    def serie_temporal(self, x, y, titulo=None, x_label=None, y_label=None):
        '''
        --> Plota a série temporal
        :param x: Período analisado
        :param y: Pagamentos da série
        '''
        ax = px.line(data_frame=self._investimento, x=x, y=y, title=titulo)
        ax.update_layout(xaxis_title=x_label,
                        yaxis_title=y_label)
        st.plotly_chart(ax)
