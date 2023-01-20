import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from data_viz.data_analysis import DataAnalysis
import plotly.express as px
from pandas.io.formats.style import Styler
from statsmodels.tsa.seasonal import seasonal_decompose
from etl.catch_clean import data_aggregation


class StockPriceViz(DataAnalysis):
    '''
    Data visualization of Yahoo Finance historical data
    '''
    def __init__(self, data, start_date, end_date, axis_y, data_norm=pd.DataFrame()):
        '''
        :param data: Requested data
        :param start_date: Start date to analysis
        :param end_date: Last date to analysis
        :param axiy_y: Selected company tickers of downloaded data
        :param data_norm: Data in normalized format
        '''
        super().__init__(data, start_date, end_date, axis_y, data_norm)
        self._data_norm = data_norm
        self._data = self._data.loc[(self._data.index >= self._start_date) & 
                                    (self._data.index <= self._end_date)]

    
    def candlestick(self):
        '''
        Download information from Yahoo Finance and show candlestick of last 30 days

        Returns: Plotly Candlestick Charts
                    Candlestick for one or many tickers
        '''
        if len(self._axis_y) == 1:
            fig = go.Figure(data=[go.Candlestick(x=self._data.index,
                                                open=self._data['Open'],
                                                high=self._data['High'],
                                                low=self._data['Low'],
                                                close=self._data['Close'])])
            fig.update_layout(title=f'{self._axis_y[0]}',
                            yaxis_title='R$',
                            height=550)
            st.plotly_chart(fig, use_container_width=True)
        else:
            for ticker in self._axis_y:
                fig = go.Figure(data=[go.Candlestick(x=self._data.index,
                                                    open=self._data['Open'][ticker],
                                                    high=self._data['High'][ticker],
                                                    low=self._data['Low'][ticker],
                                                    close=self._data['Close'][ticker])])
                fig.update_layout(title=f'{ticker}',
                                yaxis_title='R$',
                                height=550)
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
                df_stats = self._data['Close'][[ticker]].describe().T.round()
                df_stats.columns = ['registros', 'média', 'desvio padrão', 'min', 'Q1', 'Q2', 'Q3', 'max']
                df_stats['range'] = df_stats['max'] - df_stats['min']
                df_stats = df_stats[['registros', 'min', 'max', 'range', 'média', 'desvio padrão', 'Q1', 'Q2', 'Q3']]
                st.dataframe(df_stats.style.format('{:.0f}'))    
        else:
            df_stats = self._data[['Close']].describe().T.round()
            df_stats.columns = ['registros', 'média', 'desvio padrão', 'min', 'Q1', 'Q2', 'Q3', 'max']
            df_stats['range'] = df_stats['max'] - df_stats['min']
            df_stats = df_stats[['registros', 'min', 'max', 'range', 'média', 'desvio padrão', 'Q1', 'Q2', 'Q3']]
            st.dataframe(df_stats.style.format('{:.0f}'))


    def time_series(self):
        '''
        Visualize the selected indicator

        Parameters: legend_x_position : Float 
                        The x position of legend in visualization
    
                    legend_y_position: Float
                        The y position of legend in visualization

        Returns: Plotly Line Chart
                    Line chart for one or many indicators
        '''
        if self._data_norm.empty:
            data = self._data.copy()
        else:
            data = self._data_norm.copy()
        if len(self._axis_y) > 1:
            fig = px.line(data['Close'], x=data.index, y=self._axis_y)
            fig.update_layout(
                xaxis_title='Data',
                yaxis_title='R$'
            )
            st.plotly_chart(fig, use_container_width=True)    
        else:
            fig = px.line(data, x=data.index, y='Close')
            fig.update_layout(
                xaxis_title='Data',
                yaxis_title='R$'
            )
            st.plotly_chart(fig, use_container_width=True)


    def histogram_view(self):
        '''
        Show financial market indicator statistical distribution

        Returns: Plotly Histogram Chart
                    Histogram chart for one or many indicators
        '''
        if len(self._axis_y) > 1:
            fig = px.histogram(self._data['Close'], x=self._axis_y)
            fig.update_layout(
                xaxis_title='R$',
                yaxis_title='')
            st.plotly_chart(fig, use_container_width=True)
        else:
            fig = px.histogram(self._data, x='Close')
            fig.update_layout(
                xaxis_title=self._axis_y[0],
                yaxis_title='')
            st.plotly_chart(fig, use_container_width=True)


    def boxplot_view(self):
        '''
        Show financial market indicator with Boxplot

        Returns: Plotly Boxplot Chart
                Boxplot chart for one or many indicators
        '''
        if len(self._axis_y) > 1:
            fig = px.box(self._data['Close'], y=self._axis_y)
            fig.update_layout(
                xaxis_title='',
                yaxis_title='R$')
            st.plotly_chart(fig)
        else:
            fig = px.box(self._data, y='Close')
            fig.update_layout(
                xaxis_title=self._axis_y[0],
                yaxis_title='R$')
            st.plotly_chart(fig, use_container_width=True)


    def barplot_view(self, aggregation: str, function: object):
        '''
        Financial market indicator with Barplot by year

        Returns: Plotly Barplot Chart
                    Barplot chart for one or many indicators with options to aggregate by year, quarter or
                    month, with sum or mean.
        '''
        data = self._data.copy()
        # Reset index to be used by data_aggregation function
        data.reset_index(inplace=True)
        data.rename(columns={'Date': 'date'}, inplace=True)
        data_agg = data_aggregation(data=data, aggregation=aggregation, function=function)

        if len(self._axis_y) > 1:
            fig = px.bar(data_agg['Close'], x=data_agg.index, y=self._axis_y, barmode='group')
            fig.update_layout(
                xaxis_title='',
                yaxis_title='R$',
                xaxis=dict(type='category'))
            st.plotly_chart(fig)
        else:
            fig = px.bar(data_agg, x=data_agg.index, y='Close')
            fig.update_layout(
                xaxis_title=self._axis_y[0],
                yaxis_title='R$',
                xaxis=dict(type='category'))
            st.plotly_chart(fig, use_container_width=True)


    def normalize_time_series(self):
        '''
        Transforms the time series into normalized form by dividing the series by the first record.
        '''
        self._data_norm = self._data.copy()
        if len(self._axis_y) > 1:
            for column in self._axis_y:
                self._data_norm.loc[:, ('Close', column)] = self._data_norm['Close'][column] / self._data_norm['Close'][column][0]
        else:
            self._data_norm['Close'] = self._data_norm['Close'] / self._data_norm['Close'].iloc[0]


    def normalized_metric(self):
        '''
        Show the metric referal to increase or decrease in the period of normalized time series

        Returns: Pandas DataFrame
                    DataFrame with calculated metric
        ''' 
        if len(self._axis_y) > 1:
            dic = dict()
            for column in self._axis_y:  
                dic[column] = [round((self._data_norm['Close'][column].iloc[-1] - self._data_norm['Close'][column].iloc[0]), 2)]
            df = pd.DataFrame(dic)
            df = Styler(df, 2)
            st.write('Valorização no período')
            st.dataframe(df)
        else:
            dic = dict()
            dic['Close'] = [round((self._data_norm['Close'].iloc[-1] - self._data_norm['Close'].iloc[0]), 2)]
            df = pd.DataFrame(dic)
            df = Styler(df, 2)
            st.write('Valorização no período')
            st.dataframe(df)


    def serie_decomposition(self):
        '''
        Seasonality and trend of time series
        '''  
        try:
            if len(self._axis_y) > 1:
                st.write('Selecione apenas um índice para essa visualização')
            else: 
                # Agregate data by mean/ month 
                data_month = self._data[['Close']].groupby(pd.Grouper(freq="M")).mean()
                # Decompose time serie with statsmodels
                dec = seasonal_decompose(data_month, period=12)
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
                st.write('Dados agregados por média mês!')
        except:
            st.write('Selecione ao menos 2 anos completos para essa visualização!')
