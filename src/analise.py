import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import numpy as np

class SerieTemporal:
    '''
    --> Apresenta a série temporal dos investimentos analisados
    '''
    def __init__(self, investimento=None, inpc=None, x_investimento=None, y_investimento=None, x_inpc=None, y_inpc=None):
        '''
        :param investimento: Série temporal do investimento
        '''
        self._investimento = investimento
        self._inpc = inpc
        self._x_investimento = x_investimento
        self._y_investimento = y_investimento
        self._x_inpc = x_inpc
        self._y_inpc = y_inpc
    
    
    def serie_temporal(self, titulo=None, x_label=None, y_label=None, inpc='INPC'):
        '''
        --> Plota a série temporal
        :param x: Período analisado
        :param y: Pagamentos da série
        '''
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self._investimento[self._x_investimento], y=self._investimento[self._y_investimento],
                      mode='lines',
                      name='Poupança'))
        fig.add_trace(go.Scatter(x=self._inpc[self._x_inpc], y=self._inpc[self._y_inpc],
                      mode='lines',
                      name=inpc,
                      line_color='rgb(255,215,0)'))
        fig.add_trace(go.Indicator(
                    mode = "number+delta",
                    value = np.sum(self._investimento[self._y_investimento]).round(2),
                    delta = {"reference": np.sum(self._inpc[self._y_inpc]).round(2)},
                    title = {"text": "Rendimento do Período"},
                    domain = {'y': [0, 1], 'x': [0.25, 0.75]}))
        fig.update_layout(title=titulo,
                        xaxis_title=x_label,
                        yaxis_title=y_label)
        st.plotly_chart(fig)
