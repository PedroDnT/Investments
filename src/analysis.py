import streamlit as st
import plotly.graph_objects as go
import numpy as np


class AnalysisSeriesMontly:
    '''
    --> Analyzes the time series of the selected indicator(s)
    '''
    def __init__(self, data=None, period=None, axis_x='date', x_label='', y_label='%'):
        '''
        :param data: DataFrame Pandas of the time series with monthly indicators
        :param periodo: Selected period to analysis
        :param axis_x: Axis x of serie
        :param x_label: Label x of serie
        :param y_label: Label y of serie
        '''
        self._data = data
        self._period = period
        self._axis_x = axis_x
        self._x_label = x_label
        self._y_label = y_label

    
    def compare_indicator(self, indicador_avaliado=None, indicador_comparado=None, descricao_indicador_avaliado=None, 
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


    def visualize_indicator(self, axis_y=None, description_indicator=None):
        '''
        --> Visualize the selected indicator

        :param indicator: Selected indicator
        :param description_indicator: Description of selected indicator
        '''
        period = self._data[self._axis_x].dt.year.between(self._period[0], self._period[1]) == True
        axis_x = self._data[period][self._axis_x]
        axis_y = self._data[period][axis_y]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=axis_x,
                    y=axis_y,
                    mode='lines',
                    name=description_indicator))
        fig.update_layout(title=description_indicator,
                        xaxis_title=self._x_label,
                        yaxis_title=self._y_label)
        st.plotly_chart(fig)

    
class AnalysisSerieDaily:
    '''
    --> Analyzes the time series of the selected indicator(s)
    '''
    def __init__(self, data=None, initial_date=None, final_date=None, axis_x='data', x_label='', y_label='R$'):
        '''
        :param data: DataFrame Pandas of time series with daily indicators
        :param data_inicial: Initial date of time series
        :param data_final: Final date of time series
        :param eixo_x: X axis of time series 
        :param x_label: Label x of serie
        :param y_label: Label y of serie
        '''
        self._data = data
        self._initial_date = initial_date        
        self._final_date = final_date
        self._axis_x = axis_x
        self._x_label = x_label
        self._y_label = y_label


    def visualize_indicator_daily(self, axis_y=None, description_indicator=None):
        '''
        --> Visualize selected indicator

        :param indicator: Selected indicator
        :param description_indicator: Description of selected indicator
        '''
        data = self._data.loc[self._initial_date:self._final_date]
        # Dados das séries/ eixos
        axis_x = data.index
        axis_y = data[axis_y]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=axis_x,
                    y=axis_y,
                    mode='lines'))
        fig.update_layout(title=description_indicator,
                        xaxis_title=self._x_label,
                        yaxis_title=self._y_label)
        st.plotly_chart(fig)
