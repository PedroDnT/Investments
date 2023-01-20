import streamlit as st
import pandas as pd
import plotly.express as px
from statsmodels.tsa.seasonal import seasonal_decompose
from data_viz.data_analysis import DataAnalysis
from etl.catch_clean import data_aggregation
from pandas.io.formats.style import Styler


class AnalysisSeries(DataAnalysis):
    '''
    Analyzes the time series of the selected indicator(s)
    '''
    def __init__(self, data, start_date, end_date, axis_y, axis_x='date', x_label='', y_label='%',
                 data_norm=pd.DataFrame()):
        '''
        :param data: DataFrame Pandas of the time series with monthly indicators
        :param start_date: Start date to analysis
        :param end_date: Last date to analysis
        :param axis_y: Selected columns in Pandas DataFrame
        :param axis_x: Axis x of serie
        :param x_label: Label x of serie
        :param y_label: Label y of serie
        :param data_norm: Pandas DataFrame with normalization format
        '''
        super().__init__(data, start_date, end_date, axis_y, data_norm)
        self._axis_x = axis_x
        self._x_label = x_label
        self._y_label = y_label
        self._data = data.loc[(data['date'] >= self._start_date) & (data['date'] <= self._end_date)]


    def time_series(self, legend_x_position=1.02, legend_y_position=1):
        '''
        Visualize the selected indicator

        Parameters: legend_x_position : Float 
                        The x position of legend in visualization
    
                    legend_y_position: Float
                        The y position of legend in visualization

        Returns: Plotly Line Chart
                    Line chart for one or many indicators
        ''' 
        # Visualization
        if self._data_norm.empty:
            data = self._data.copy()
        else:
            data = self._data_norm.copy()
        fig = px.line(data, x=self._axis_x, y=self._axis_y)
        annotations = list()
        annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                              xanchor='center', yanchor='top',
                              text='Fonte: Portal de Dados Abertos',
                              font=dict(family='Arial',
                                        size=12,
                                        color='rgb(150,150,150)'),
                              showarrow=False))
        fig.update_layout(xaxis_title=self._x_label,
                        yaxis_title=self._y_label,
                        annotations=annotations,
                        legend=dict(x=legend_x_position, y=legend_y_position))
        st.plotly_chart(fig, use_container_width=True)


    def descriptive_statistics(self):
        '''
        Central tendency and dispersion statistics information


        Returns: Pandas DataFrame
                    DataFrame with following columns: 
                        registros: number of records 
                        média: mean 
                        desvio padrão: standard deviation 
                        min: minimum 
                        Q1: first quartile 
                        Q2: median 
                        Q3: third quartile 
                        max: maximum                     
        '''
        if len(self._axis_y) > 1:
            for ticker in self._axis_y:
                df_stats = self._data[[ticker]].describe().T.round(2)
                df_stats.columns = ['registros', 'média', 'desvio padrão', 'min', 'Q1', 'Q2', 'Q3', 'max']
                df_stats['range'] = df_stats['max'] - df_stats['min']
                df_stats = df_stats[['registros', 'min', 'max', 'range', 'média', 'desvio padrão', 'Q1', 'Q2', 'Q3']]
                st.dataframe(df_stats.style.format('{:.2f}'))    
        else:
            df_stats = self._data[self._axis_y].describe().T.round(2)
            df_stats.columns = ['registros', 'média', 'desvio padrão', 'min', 'Q1', 'Q2', 'Q3', 'max']
            df_stats['range'] = df_stats['max'] - df_stats['min']
            df_stats = df_stats[['registros', 'min', 'max', 'range', 'média', 'desvio padrão', 'Q1', 'Q2', 'Q3']]
            st.dataframe(df_stats.style.format('{:.2f}'))


    def histogram_view(self):
        '''
        Show financial market indicator statistical distribution

        Returns: Plotly Histogram Chart
                    Histogram chart for one or many indicators
        '''
        fig = px.histogram(self._data, x=self._axis_y)
        fig.update_layout(
            xaxis_title='%',
            yaxis_title='Frequência')
        st.plotly_chart(fig, use_container_width=True)


    def boxplot_view(self):
        '''
        Show financial market indicator with Boxplot

        Returns: Plotly Boxplot Chart
                Boxplot chart for one or many indicators
        '''
        fig = px.box(self._data, y=self._axis_y)
        fig.update_layout(
            xaxis_title='',
            yaxis_title=self._y_label)
        st.plotly_chart(fig, use_container_width=True)


    def barplot_view(self, aggregation: str, function):
        '''
        Financial market indicator with Barplot by year

        Returns: Plotly Barplot Chart
                    Barplot chart for one or many indicators with options to aggregate by year, quarter or
                    month, with sum or mean.
        '''
        data = self._data.copy()
        data_agg = data_aggregation(data=data, aggregation=aggregation, function=function)
        
        fig = px.bar(data_agg, x=data_agg.index, y=self._axis_y, barmode='group')
        fig.update_layout(
            xaxis_title=aggregation,
            yaxis_title=self._y_label,
            xaxis=dict(type='category'))
        st.plotly_chart(fig, use_container_width=True)


    def acumulated(self):
        '''
        Print the metric referal to accumulated time series

        Returns: DataFrame
                    Pandas DataFrame with the sum of series records
        ''' 
        dic = dict()
        for indexers in self._axis_y:  
            dic[f'{indexers} %'] = [round(sum(self._data[indexers]), 2)]
        df = pd.DataFrame(dic)
        st.write('Acumulado no período')
        df = Styler(df, 2)
        st.dataframe(df)


    def serie_decomposition(self):
        '''
        Seasonality and trend of time series

        Returns: Plotly Line Chart
                    Line chart for seasonal and trend of series
        '''  
        try:
            if len(self._axis_y) > 1:
                st.write('Selecione apenas um índice para essa visualização')
            else:
                # Set date as index
                data = self._data.set_index('date')
                data.index = pd.to_datetime(data.index) 
                # Decompose time serie with statsmodels
                dec = seasonal_decompose(data[self._axis_y], period=12)

                # Create DataFrame of seasonality and trend
                df_dec = pd.DataFrame({'date': dec.seasonal.index, self._axis_y[0]: dec.seasonal.values})
                df_tred = pd.DataFrame({'date': dec.trend.index, self._axis_y[0]: dec.trend.values})
                
                # Show seasonal result
                seasonal_fig = px.line(df_dec, x='date', y=self._axis_y[0], title=f'Sazonalidade {self._axis_y[0]}')
                seasonal_fig.update_layout(xaxis_title='Data', yaxis_title='')
                st.plotly_chart(seasonal_fig, use_container_width=True)
                
                # Show trend result
                tred_fig = px.line(df_tred, x='date', y=self._axis_y[0], title=f'Tendênica {self._axis_y[0]}')
                tred_fig.update_layout(xaxis_title='Data', yaxis_title='')
                st.plotly_chart(tred_fig, use_container_width=True) 
        except:
            st.write('Selecione ao menos 2 anos completos para essa visualização!')
