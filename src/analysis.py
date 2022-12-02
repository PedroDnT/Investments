import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from pandas.io.formats.style import Styler
import yfinance as yf
from datetime import date
import plotly.graph_objects as go


class DataAnalysis:
    '''
    --> Define the data and indicators to be analyzed
    '''
    def __init__(self, data: pd.DataFrame, axis_y: list):
        '''
        :param data: Data source to analyze
        :param y_axis: Selected columns in Pandas DataFrame
        '''
        self._data = data
        self._axis_y = axis_y


    def correlation(self):
        '''
        --> Show the matrix correlation of selected indexes
        '''
        # Correlation calc
        try:
            df_corr = self._data[self._axis_y].corr().round(1)
        except:
            # Stock price with one ticker selected
            df_corr = self._data[['Close']].corr().round(1)    
            
        # Mask to matrix
        mask = np.zeros_like(df_corr)
        mask[np.triu_indices_from(mask)] = True
        # Viz seaborn
        fig, ax = plt.subplots()
        sns.set(rc={"figure.figsize":(4, 3)}, font_scale=0.5)
        ax = sns.heatmap(df_corr, annot=True, mask=mask, annot_kws={"size":5})
        plt.xticks(rotation=45, fontsize=5)
        plt.xlabel('')
        plt.ylabel('')
        plt.yticks(fontsize=5)
        st.pyplot(fig)


    def histogram_view(self, column: list, indicator: str, x_label: str):
        '''
        --> Show the stock price distribution
        '''
        if len(self._axis_y) > 1:
            fig = px.histogram(self._data[column].melt(var_name=indicator), x='value', color=indicator,
                                opacity=0.8)
            fig.update_layout(
                xaxis_title=x_label,
                yaxis_title='Frequência',
                barmode='overlay')
            st.plotly_chart(fig)
        else:
            fig = px.histogram(self._data, x=column)
            fig.update_layout(
                xaxis_title=x_label,
                yaxis_title='Frequência')
            st.plotly_chart(fig)


    def normalize_time_series(self):
        '''
        --> Transform time series in normalized form

        :param axis_y: Stocks series selected
        '''
        #data_slice = self._data.query('date >= @self._start_date')
        for column in self._axis_y:
            normalized = list()
            for row in self._data[column]:
                normalized.append(row / self._data[column].iloc[0])
            self._data[column] = normalized


    def normalized_metric(self):
        '''
        --> Print the metric referal to increase or decrease in the period of normalized time series

        :param axis_y: Selected indicator
        ''' 
        dic = dict()
        for column in self._axis_y:  
            dic[column] = [round((self._data[column].iloc[-1] - self._data[column].iloc[0]), 2)]
        df = pd.DataFrame(dic)
        df = Styler(df, 2)
        st.write('Crescimento relativo %')
        st.dataframe(df)


class AnalysisSeriesMontly(DataAnalysis):
    '''
    --> Analyzes the time series of the selected indicator(s)
    '''
    def __init__(self, data, axis_y, start_date, axis_x='date', x_label='', y_label='%'):
        '''
        :param data: DataFrame Pandas of the time series with monthly indicators
        :param axis_y: Selected columns in Pandas DataFrame
        :param start_date: Selected period to analysis
        :param axis_x: Axis x of serie
        :param x_label: Label x of serie
        :param y_label: Label y of serie
        :param data_slice: Pandas DataFrame with selected initial date
        '''
        super().__init__(data, axis_y)
        self._start_date = start_date
        self._axis_x = axis_x
        self._x_label = x_label
        self._y_label = y_label
        self._data = data.query('date >= @self._start_date')


    def visualize_indicator(self):
        '''
        --> Visualize the selected indicator
        '''
        # Selected data
        self._data = self._data.query('date >= @self._start_date') 
        data_melt = self._data.melt(id_vars='date', value_vars=self._axis_y, var_name='indexers', value_name='%')
        # Visualization
        fig = px.line(data_melt, 'date', '%', color='indexers')
        annotations = list()
        annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                              xanchor='center', yanchor='top',
                              text='Fonte: Governo Brasileiro',
                              font=dict(family='Arial',
                                        size=12,
                                        color='rgb(150,150,150)'),
                              showarrow=False))
        fig.update_layout(xaxis_title=self._x_label,
                        yaxis_title=self._y_label,
                        annotations=annotations)
        st.plotly_chart(fig, use_container_width=True)


    def descriptive_statistics(self):
        '''
        --> Central tendency and dispersion statistics information
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


    def acumulated(self):
        '''
        --> Print the metric referal to accumulated time series

        :param axis_y: Selected indicator
        ''' 
        dic = dict()
        for indexers in self._axis_y:  
            dic[f'{indexers} %'] = [round(sum(self._data[indexers]), 2)]
        df = pd.DataFrame(dic)
        st.write('Acumulado no período')
        df = Styler(df, 2)
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
        self._data_melt = self._data_slice.melt(id_vars='date', value_vars=axis_y, var_name='indexers', value_name='R$')
        # Visualization
        fig = px.line(self._data_melt, 'date', 'R$', color='indexers')
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


    def normalized_metric(self, axis_y=None):
        '''
        --> Print the metric referal to increase or decrease in the period of normalized time series

        :param axis_y: Selected indicator
        ''' 
        dic = dict()
        for column in axis_y:  
            dic[column] = [round((self._data[column].iloc[-1] - self._data[column].iloc[0]) * 100, 0)]
        df = pd.DataFrame(dic)
        df = Styler(df, 0)
        st.write('Valorization %')
        st.dataframe(df)


    def visualize_serie_normalized(self, axis_y=None, y_label='X'):
        '''
        --> Visualize time series normalized

        :param indicator: Selected indicator
        '''
        if len(axis_y) == 1:
            data_melt = self._data_normalized.melt(id_vars='date', var_name='indexers', value_name='x')
            # Visualization
            fig = px.line(data_melt, 'date', 'x', color='indexers')
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
            data_melt = self._data_normalized.melt(id_vars='date', var_name='indexers', value_name='x')
            # Visualization
            fig = px.line(data_melt, 'date', 'x', color='indexers')
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
            dic[stocks] = [round((self._data_normalized[stocks].iloc[-1] - self._data_normalized[stocks].iloc[0]) * 100, 0)]
        df = pd.DataFrame(dic)
        df = Styler(df, 0)
        st.write('Valorization %')
        st.dataframe(df)

    
    def valorization_metric(self, axis_y=None):
        '''
        --> Print the metric referal to increase or decrease in the period of normalized time series

        :param axis_y: Selected indicator
        ''' 
        dic = dict()
        for stocks in axis_y:  
            dic[stocks] = [round(self._data_slice[stocks].iloc[-1] - self._data_slice[stocks].iloc[0], 1)]
        df = pd.DataFrame(dic)
        df = Styler(df, 1)
        st.write('Valorization R$')
        st.dataframe(df)

    
class StockPriceViz(DataAnalysis):
    '''
    --> Catch data from Yahoo Finance to analysis
    '''
    def __init__(self, data, axis_y, data_norm=pd.DataFrame):
        '''
        :param data: Requested data
        :param tickers: Selected company tickers to download data
        '''
        super().__init__(data, axis_y)
        self._data_norm = data_norm

    
    def candlestick(self):
        '''
        --> Download information from Yahoo Finance and show candlestick of last 30 days

        :param ticker: Company ticker selected
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
        --> Central tendency and dispersion statistics information
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
        --> Show the historical series of selected tickers
        '''
        if self._data_norm.empty:
            data = self._data.copy()
        else:
            data = self._data_norm.copy()
        if len(self._axis_y) > 1:
            data = data[['Close']].melt(ignore_index=False, col_level=1)
            fig = px.line(data, x=data.index, y=data['value'], color='variable')
            fig.update_layout(
                xaxis_title='Data',
                yaxis_title='R$'
            )
            st.plotly_chart(fig)    
        else:
            fig = px.line(data, x=data.index, y='Close')
            fig.update_layout(
                xaxis_title='Data',
                yaxis_title='R$'
            )
            st.plotly_chart(fig)


    def normalize_time_series(self):
        '''
        --> Transform time series in normalized form

        :param axis_y: Stocks series selected
        '''
        self._data_norm = self._data.copy()
        if len(self._axis_y) > 1:
            for column in self._axis_y:
                normalized = list()
                for row in self._data_norm['Close'][column]:
                    normalized.append(row / self._data_norm['Close'][column].iloc[0])
                self._data_norm.loc[:, ('Close', column)] = normalized
        else:
            normalized = list()
            for row in self._data_norm['Close']:
                normalized.append(row / self._data_norm['Close'].iloc[0])
            self._data_norm['Close'] = normalized


    def normalized_metric(self):
        '''
        --> Print the metric referal to increase or decrease in the period of normalized time series

        :param axis_y: Selected indicator
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
    

@st.cache    
def request_data(selected_tickers, start_date):
        today = date.today()
        return yf.download(tickers=selected_tickers, start=start_date, end=today)