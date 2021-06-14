import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import numpy as np


class AnalisaSerie:
    '''
    --> Analisa a série temporal do(s) indicador(s) selecioando(s)
    '''
    def __init__(self, dados=None, periodo=None, eixo_x='data', x_label='', y_label='%'):
        '''
        :param dados: DataFrame Pandas com as séries temporais
        :param periodo: Período selecionado para análise
        :param eixo_x: Eixo x da série
        :param x_label: Label x da série
        :param y_label: Label y da série
        '''
        self._dados = dados
        self._periodo = periodo
        self._eixo_x = eixo_x
        self._x_label = x_label
        self._y_label = y_label

    
    def compara_indicador(self, indicador_avaliado=None, indicador_comparado=None, descricao_indicador_avaliado=None, 
                        descricao_indicador_comparado=None, titulo_grafico=None):
        '''
        --> Plota a série temporal com o indicador selecionado e o indicador para comparação

        :param indicador_avaliado: Indicador selecionado para análise
        :param indicador_comparado: Indicador para comparação
        :param descricao_indicador_avaliado: Descrição do indicador avaliado
        :param descricao_indicador_comparado: Descrição do indicador em comparação
        :param titulo: Título do gráfico
        :param y_label: Descrição do eixo y do gráfico
        '''
        # Variáveis de definição do intervalo de tempo 
        periodo = self._dados['data'].dt.year.between(self._periodo[0], self._periodo[1]) == True
        # Dados das séries/ eixos
        eixo_x = self._dados[periodo][self._eixo_x]
        indicador_avaliado = self._dados[periodo][indicador_avaliado]
        indicador_comparado = self._dados[periodo][indicador_comparado]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=eixo_x, 
                                y=indicador_avaliado,
                    mode='lines',
                    name=descricao_indicador_avaliado))
        fig.add_trace(go.Scatter(x=eixo_x, 
                                y=indicador_comparado,
                    mode='lines',
                    name=descricao_indicador_comparado,
                    line_color='rgb(255,215,0)'))
        fig.add_trace(go.Indicator(
                    mode = "delta",
                    value = np.sum(indicador_avaliado).round(2),
                    delta = {"reference": np.sum(indicador_comparado).round(2)},
                    domain = {'y': [0, 1], 'x': [0.25, 0.75]}))
        fig.update_layout(title=titulo_grafico,
                        xaxis_title=self._x_label,
                        yaxis_title=self._y_label)
        st.plotly_chart(fig)


    def visualiza_indicador(self, dados=None, eixo_y=None, descricao_indicador=None):
        '''
        --> Visualiza o indicador selecionado

        :param indicador: Indicador selecionado
        :param descricao_indicador: Descrição do indicador selecionado
        '''
        # Variáveis de definição do intervalo de tempo 
        periodo = self._dados[self._eixo_x].dt.year.between(self._periodo[0], self._periodo[1]) == True
        # Dados das séries/ eixos
        eixo_x = self._dados[periodo][self._eixo_x]
        eixo_y = self._dados[periodo][eixo_y]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=eixo_x,
                    y=eixo_y,
                    mode='lines',
                    name=descricao_indicador))
        fig.update_layout(title=descricao_indicador,
                        xaxis_title=self._x_label,
                        yaxis_title=self._y_label)
        st.plotly_chart(fig)
