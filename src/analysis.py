import streamlit as st
import plotly.graph_objects as go
import numpy as np
import plotly.express as px


class AnalysisSeriesMontly:
    '''
    --> Analyzes the time series of the selected indicator(s)
    '''
    def __init__(self, data=None, start_date=None, axis_x='date', x_label='', y_label='%'):
        '''
        :param data: DataFrame Pandas of the time series with monthly indicators
        :param start_date: Selected period to analysis
        :param axis_x: Axis x of serie
        :param x_label: Label x of serie
        :param y_label: Label y of serie
        '''
        self._data = data
        self._start_date = start_date
        self._axis_x = axis_x
        self._x_label = x_label
        self._y_label = y_label


    def visualize_indicator(self, axis_y=None):
        '''
        --> Visualize the selected indicator

        :param indicator: Selected indicator
        '''
        # Selected data
        data_slice = self._data.query('date >= @self._start_date') 
        data_melt = data_slice.melt(id_vars='date', value_vars=axis_y, var_name='indexers', value_name='%')
        # Visualization
        fig = px.line(data_melt, 'date', '%', color='indexers')
        fig.update_layout(xaxis_title=self._x_label,
                        yaxis_title=self._y_label)
        st.plotly_chart(fig)        

    
class AnalysisSerieDaily:
    '''
    --> Analyzes the time series of the selected indicator(s)
    '''
    def __init__(self, data=None, start_date=None, axis_x='data', x_label='', y_label='R$'):
        '''
        :param data: DataFrame Pandas of time series with daily indicators
        :param start_data: Initial date of time series
        :param eixo_x: X axis of time series 
        :param x_label: Label x of serie
        :param y_label: Label y of serie
        '''
        self._data = data
        self._start_date = start_date
        self._axis_x = axis_x
        self._x_label = x_label
        self._y_label = y_label


    def visualize_indicator_daily(self, axis_y=None):
        '''
        --> Visualize selected indicator

        :param indicator: Selected indicator
        '''
        # Selected data
        data_slice = self._data.query('date >= @self._start_date')
        data_melt = data_slice.melt(id_vars='date', value_vars=axis_y, var_name='indexers', value_name='%')
        # Visualization
        fig = px.line(data_melt, 'date', '%', color='indexers')
        fig.update_layout(xaxis_title=self._x_label,
                        yaxis_title=self._y_label)
        st.plotly_chart(fig)
