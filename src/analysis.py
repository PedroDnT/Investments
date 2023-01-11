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
from statsmodels.tsa.seasonal import seasonal_decompose


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
        if len(self._axis_y) <= 1:
            st.write('Selecione ao menos dois índices!')
        else: 
            try:
                df_corr = self._data[self._axis_y].corr().round(1)
            except:
                # Stock price with one ticker selected
                df_corr = self._data['Close'].corr().round(1)  
            # Mask to matrix
            mask = np.zeros_like(df_corr, dtype=bool)
            mask[np.triu_indices_from(mask)] = True
            # Viz
            df_corr_viz = df_corr.mask(mask).dropna(how='all').dropna('columns', how='all')
            fig = px.imshow(df_corr_viz, text_auto=True)
            st.plotly_chart(fig)
            

    def normalize_time_series(self):
        '''
        --> Transform time series in normalized form

        :param axis_y: Stocks series selected
        '''
        for column in self._axis_y:
            normalized = list()
            for row in self._data[column]:
                normalized.append(row / self._data[column].iloc[0])
            self._data[column] = normalized


    def normalized_metric(self):
        '''
        --> Print the metric referal to increase or decrease in the period of normalized time series
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
    Analyzes the time series of the selected indicator(s)
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
        # Visualization
        fig = px.line(self._data, x='date', y=self._axis_y)
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


    def histogram_view(self):
        '''
        --> Show financial market indicator statistical distribution
        '''
        fig = px.histogram(self._data, x=self._axis_y)
        fig.update_layout(
            xaxis_title='%',
            yaxis_title='Frequência')
        st.plotly_chart(fig)


    def boxplot_view(self):
        '''
        --> Show financial market indicator with Boxplot
        '''
        fig = px.box(self._data, y=self._axis_y)
        fig.update_layout(
            xaxis_title='',
            yaxis_title=self._y_label)
        st.plotly_chart(fig)


    def barplot_view(self):
        '''
        --> Show financial market indicator with Barplot by year
        '''
        data = self._data.copy()
        data['year'] = data['date'].dt.year
        fig = px.bar(data.groupby('year', as_index=False).sum(numeric_only=True), x='year', y=self._axis_y, 
                    barmode='group')
        fig.update_layout(
            xaxis_title='Ano',
            yaxis_title=self._y_label,
            xaxis=dict(type='category'))
        st.plotly_chart(fig)


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


    def serie_decomposition(self):
        '''
        Seasonality and trend of time series
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
                st.plotly_chart(seasonal_fig)
                # Show trend result
                tred_fig = px.line(df_tred, x='date', y=self._axis_y[0], title=f'Tendênica {self._axis_y[0]}')
                tred_fig.update_layout(xaxis_title='Data', yaxis_title='')
                st.plotly_chart(tred_fig) 
        except:
            st.write('Selecione ao menos 2 anos completos para essa visualização!')
    
 
class StockPriceViz(DataAnalysis):
    '''
    Data visualization of Yahoo Finance historical data
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
            fig = px.line(data['Close'], x=data.index, y=self._axis_y)
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
            st.plotly_chart(fig, use_container_width=True)


    def histogram_view(self, x_label: str):
        '''
        --> Show financial market indicator statistical distribution
        '''
        if len(self._axis_y) > 1:
            fig = px.histogram(self._data['Close'], x=self._axis_y)
            fig.update_layout(
                xaxis_title=x_label,
                yaxis_title='')
            st.plotly_chart(fig)
        else:
            fig = px.histogram(self._data, x='Close')
            fig.update_layout(
                xaxis_title=self._axis_y[0],
                yaxis_title='')
            st.plotly_chart(fig)


    def boxplot_view(self, y_label: str):
        '''
        --> Show financial market indicator with Boxplot
        '''
        if len(self._axis_y) > 1:
            fig = px.box(self._data['Close'], y=self._axis_y)
            fig.update_layout(
                xaxis_title='',
                yaxis_title=y_label)
            st.plotly_chart(fig)
        else:
            fig = px.box(self._data, y='Close')
            fig.update_layout(
                xaxis_title=self._axis_y[0],
                yaxis_title=y_label)
            st.plotly_chart(fig)


    def normalize_time_series(self):
        '''
        --> Transform time series in normalized form

        :param axis_y: Stocks series selected
        '''
        self._data_norm = self._data.copy()
        if len(self._axis_y) > 1:
            for column in self._axis_y:
                self._data_norm.loc[:, ('Close', column)] = self._data_norm['Close'][column] / self._data_norm['Close'][column][0]
        else:
            self._data_norm['Close'] = self._data_norm['Close'] / self._data_norm['Close'].iloc[0]


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
                st.plotly_chart(seasonal_fig)
                # Show trend result
                tred_fig = px.line(df_tred, x='date', y=self._axis_y[0], title=f'Tendênica {self._axis_y[0]}')
                tred_fig.update_layout(xaxis_title='Data', yaxis_title='')
                st.plotly_chart(tred_fig) 
                st.write('Dados agregados por média mês!')
        except:
            st.write('Selecione ao menos 2 anos completos para essa visualização!')
    

@st.cache    
def request_data(selected_tickers: list, start_date: str):
    '''
    Download historical financial data from Yahoo Finance about ticker negatiation 

    Parameters: selected_tickers : List of string 
                    Company tickers selected to download
    
                start_date: String
                    Initial date to download historical data

    Returns: DataFrame
                Pandas DataFrame with Open, High, Low, Close, Adj Close and Volume columns about selected tickers 
                market negatiation
    '''
    today = date.today()
    return yf.download(tickers=selected_tickers, start=start_date, end=today)
