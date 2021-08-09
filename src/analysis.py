import streamlit as st
import pandas as pd
import plotly.express as px


class AnalysisSeriesMontly:
    '''
    --> Analyzes the time series of the selected indicator(s)
    '''
    def __init__(self, data=None, start_date=None, axis_x='date', x_label='', y_label='%', data_slice=pd.DataFrame):
        '''
        :param data: DataFrame Pandas of the time series with monthly indicators
        :param start_date: Selected period to analysis
        :param axis_x: Axis x of serie
        :param x_label: Label x of serie
        :param y_label: Label y of serie
        :param data_slice: Pandas DataFrame with selected data
        '''
        self._data = data
        self._start_date = start_date
        self._axis_x = axis_x
        self._x_label = x_label
        self._y_label = y_label
        self._data_slice = data_slice


    def visualize_indicator(self, axis_y=None):
        '''
        --> Visualize the selected indicator

        :param indicator: Selected indicator
        '''
        # Selected data
        self._data_slice = self._data.query('date >= @self._start_date') 
        data_melt = self._data_slice.melt(id_vars='date', value_vars=axis_y, var_name='indexers', value_name='%')
        # Visualization
        fig = px.line(data_melt, 'date', '%', color='indexers')
        annotations = list()
        annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                              xanchor='center', yanchor='top',
                              text='Source: Brazilian Government',
                              font=dict(family='Arial',
                                        size=12,
                                        color='rgb(150,150,150)'),
                              showarrow=False))
        fig.update_layout(xaxis_title=self._x_label,
                        yaxis_title=self._y_label,
                        annotations=annotations)
        st.plotly_chart(fig, use_container_width=True)


    def acumulated(self, axis_y=None):
        '''
        --> Print the metric referal to accumulated time series

        :param axis_y: Selected indicator
        ''' 
        dic = dict()
        for indexers in axis_y:  
            dic[f'{indexers} %'] = [round(sum(self._data_slice[indexers]), 2)]
        df = pd.DataFrame(dic)
        st.write('Accumulated in the period')
        st.dataframe(df)        

    
class AnalysisSerieDaily:
    '''
    --> Analyzes the time series of the selected indicator(s)
    '''
    def __init__(self, data=None, start_date=None, axis_x='data', x_label='', y_label='R$', data_normalized=pd.DataFrame, 
                data_melt=pd.DataFrame, data_slice=pd.DataFrame):
        '''
        :param data: DataFrame Pandas of time series with daily indicators
        :param data_normalized: Pandas DataFrame with all time series divided by first element 
        :param data_melt: Pandas DataFrame with time series with selected tickers in melt format
        :param start_data: Initial date of time series
        :param eixo_x: X axis of time series 
        :param x_label: Label x of serie
        :param y_label: Label y of serie
        :param data_slice: Selected data in filters
        '''
        self._data = data
        self._data_normalized = data_normalized
        self._data_melt = data_melt
        self._start_date = start_date
        self._axis_x = axis_x
        self._x_label = x_label
        self._y_label = y_label
        self._data_slice = data_slice


    def visualize_indicator_daily(self, axis_y=None):
        '''
        --> Visualize selected indicator

        :param indicator: Selected indicator
        '''
        # Selected data
        self._data_slice = self._data.query('date >= @self._start_date')
        self._data_melt = self._data_slice.melt(id_vars='date', value_vars=axis_y, var_name='indexers', value_name='%')
        # Visualization
        fig = px.line(self._data_melt, 'date', '%', color='indexers')
        # Data Souce
        annotations = list()
        annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                              xanchor='center', yanchor='top',
                              text='Source: Yahoo Finance',
                              font=dict(family='Arial',
                                        size=12,
                                        color='rgb(150,150,150)'),
                              showarrow=False))
        fig.update_layout(xaxis_title=self._x_label,
                        yaxis_title=self._y_label,
                        annotations=annotations)
        st.plotly_chart(fig, use_container_width=True)

    
    def normalize_time_series(self, axis_y=None):
        '''
        --> Transform time series in normalized form

        :param axis_y: Stocks series selected
        '''
        data_slice = self._data.query('date >= @self._start_date')
        for column in data_slice[axis_y]:
            normalized = list()
            for row in data_slice[column]:
                normalized.append(row / data_slice[column].iloc[0])
            if self._data_normalized.empty:
                self._data_normalized = pd.DataFrame(index=data_slice['date'], data=normalized, columns=[column])
            else:
                _ = pd.DataFrame(index=data_slice['date'], data=normalized, columns=[column])
                self._data_normalized = pd.merge(self._data_normalized, _, on='date')
        self._data_normalized.reset_index(inplace=True)


    def visualize_serie_normalized(self, axis_y=None, y_label='X'):
        '''
        --> Visualize time series normalized

        :param indicator: Selected indicator
        '''
        if len(axis_y) == 1:
            data_melt = self._data_normalized.melt(id_vars='date', var_name='indexers', value_name='%')
            # Visualization
            fig = px.line(data_melt, 'date', '%', color='indexers')
            annotations = list()
            annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                              xanchor='center', yanchor='top',
                              text='Source: Yahoo Finance',
                              font=dict(family='Arial',
                                        size=12,
                                        color='rgb(150,150,150)'),
                              showarrow=False))
            fig.update_layout(xaxis_title=self._x_label,
                            yaxis_title=y_label,
                            annotations=annotations)
            st.plotly_chart(fig, use_container_width=True)
        elif len(axis_y) > 1:
            data_melt = self._data_normalized.melt(id_vars='date', var_name='indexers', value_name='%')
            # Visualization
            fig = px.line(data_melt, 'date', '%', color='indexers')
            annotations = list()
            annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                              xanchor='center', yanchor='top',
                              text='Source: Yahoo Finance',
                              font=dict(family='Arial',
                                        size=12,
                                        color='rgb(150,150,150)'),
                              showarrow=False))
            fig.update_layout(xaxis_title=self._x_label,
                            yaxis_title=y_label,
                            annotations=annotations)
            st.plotly_chart(fig, use_container_width=True)


    def normalized_metric(self, axis_y=None):
        '''
        --> Print the metric referal to increase or decrease in the period of normalized time series

        :param axis_y: Selected indicator
        ''' 
        dic = dict()
        for stocks in axis_y:  
            dic[stocks] = [round(self._data_normalized[stocks].iloc[-1] - self._data_normalized[stocks].iloc[0], 2)]
        df = pd.DataFrame(dic)
        st.write('Over Time Valorization')
        st.dataframe(df)

    
    def valorization_metric(self, axis_y=None):
        '''
        --> Print the metric referal to increase or decrease in the period of normalized time series

        :param axis_y: Selected indicator
        ''' 
        dic = dict()
        for stocks in axis_y:  
            dic[stocks] = [round(self._data_slice[stocks].iloc[-1] - self._data_slice[stocks].iloc[0], 2)]
        df = pd.DataFrame(dic)
        st.write('Valorization R$')
        st.dataframe(df)

    
    
