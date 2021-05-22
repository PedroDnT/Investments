import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import numpy as np

class SerieTemporal:
    '''
    --> Apresenta a série temporal dos investimentos analisados
    '''
    def __init__(self, investimento=None, indice_inflacao=None, x_investimento=None, y_investimento=None, x_indice_inflacao=None, 
                y_indice_inflacao=None, periodo=None):
        '''
        :param investimento: Série temporal do investimento
        :param indice_inflacao: Índice de inflação selecionada para comparação
        :param x_investimento: Eixo x da série do investimento selecionado
        :param y_investimento: Eixo y da série de investimento selecionado
        :param x_inflacao: Eixo x do índice de inflação selecionado
        :param y_inflacao: Eixo y do indice de inflação selecionado
        :param periodo: Período selecionado
        '''
        self._investimento = investimento
        self._indice_inflacao = indice_inflacao
        self._x_investimento = x_investimento
        self._y_investimento = y_investimento
        self._x_indice_inflacao = x_indice_inflacao
        self._y_indice_inflacao = y_indice_inflacao
        self._periodo = periodo
        
    
    def serie_temporal(self, titulo=None, x_label=None, y_label=None, descricao_indice_inflacao=None):
        '''
        --> Plota a série temporal
        :param x: Período analisado
        :param y: Pagamentos da série
        '''
        # Variáveis de definição do intervalo de tempo 
        periodo_investimento = self._investimento['data'].dt.year.between(self._periodo[0], self._periodo[1]) == True
        periodo_inflacao = self._indice_inflacao['data'].dt.year.between(self._periodo[0], self._periodo[1]) == True
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self._investimento[periodo_investimento][self._x_investimento], 
                                y=self._investimento[periodo_investimento][self._y_investimento],
                    mode='lines',
                    name='Poupança'))
        fig.add_trace(go.Scatter(x=self._indice_inflacao[periodo_inflacao][self._x_indice_inflacao], 
                                y=self._indice_inflacao[periodo_inflacao][self._y_indice_inflacao],
                    mode='lines',
                    name=descricao_indice_inflacao,
                    line_color='rgb(255,215,0)'))
        fig.add_trace(go.Indicator(
                    mode = "number+delta",
                    value = np.sum(self._investimento[periodo_investimento][self._y_investimento]).round(2),
                    delta = {"reference": np.sum(self._indice_inflacao[periodo_inflacao][self._y_indice_inflacao]).round(2)},
                    title = {"text": "Rendimento relativo a inflação"},
                    domain = {'y': [0, 1], 'x': [0.25, 0.75]}))
        fig.update_layout(title=titulo,
                        xaxis_title=x_label,
                        yaxis_title=y_label)
        st.plotly_chart(fig)
