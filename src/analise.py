import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import numpy as np

from captura_tratamento import Investimentos

class SerieTemporal:
    '''
    --> Apresenta a série temporal dos investimentos analisados
    '''
    def __init__(self, investimento=None, indice_inflacao=None, eixo_x='data', eixo_y='%', periodo=None):
        '''
        :param investimento: Série temporal do investimento
        :param indice_inflacao: Índice de inflação selecionada para comparação
        :param x_investimento: Eixo x da série, dados referente a data
        :param y_investimento: Eixo y da série, dados referente a taxa 
        :param periodo: Período selecionado
        '''
        self._investimento = investimento
        self._indice_inflacao = indice_inflacao
        self._eixo_x = eixo_x
        self._eixo_y = eixo_y
        self._periodo = periodo
        
    
    def serie_temporal(self, titulo=None, x_label='', y_label='%', descricao_indice_inflacao=None, descricao_investimento=None):
        '''
        --> Plota a série temporal
        :param titulo: Título do gráfico
        :param x_label: Descrição do eixo x do gráfico
        :param y_label: Descrição do eixo y do gráfico
        :param descricao_indice_inflacao: Descrição do índice de inflação selecionado
        :param descricao_investimento: Descrição do investimento selecionado
        '''
        # Variáveis de definição do intervalo de tempo 
        periodo_investimento = self._investimento['data'].dt.year.between(self._periodo[0], self._periodo[1]) == True
        periodo_inflacao = self._indice_inflacao['data'].dt.year.between(self._periodo[0], self._periodo[1]) == True
        menor_serie = min(self._investimento.shape[0], self._indice_inflacao.shape[0])
        # Dados das séries/ eixos
        investimentos_eixo_x = self._investimento[periodo_investimento][self._eixo_x][:menor_serie]
        investimentos_eixo_y = self._investimento[periodo_investimento][self._eixo_y][:menor_serie]
        inflacao_eixo_x = self._indice_inflacao[periodo_inflacao][self._eixo_x][:menor_serie]
        inflacao_eixo_y = self._indice_inflacao[periodo_inflacao][self._eixo_y][:menor_serie]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=investimentos_eixo_x, 
                                y=investimentos_eixo_y,
                    mode='lines',
                    name=descricao_investimento))
        fig.add_trace(go.Scatter(x=inflacao_eixo_x, 
                                y=inflacao_eixo_y,
                    mode='lines',
                    name=descricao_indice_inflacao,
                    line_color='rgb(255,215,0)'))
        fig.add_trace(go.Indicator(
                    mode = "number+delta",
                    value = np.sum(investimentos_eixo_y).round(2),
                    delta = {"reference": np.sum(inflacao_eixo_y).round(2)},
                    title = {"text": "Rendimento relativo a inflação"},
                    domain = {'y': [0, 1], 'x': [0.25, 0.75]}))
        fig.update_layout(title=titulo,
                        xaxis_title=x_label,
                        yaxis_title=y_label)
        st.plotly_chart(fig)
