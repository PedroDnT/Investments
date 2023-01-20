import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pandas.io.formats.style import Styler


class DataAnalysis:
    '''
    --> Define the data and indicators to be analyzed
    '''
    def __init__(self, data: pd.DataFrame, start_date: str, end_date: str, axis_y: list, 
                 data_norm: pd.DataFrame):
        '''
        :param data: Data source to analyze
        :param start_date: Start date to analysis
        :param end_date: Last date to analysis
        :param y_axis: Selected columns in Pandas DataFrame
        :param data_norm: Pandas DataFrame with normalization format 
        '''
        self._data = data
        self._start_date = start_date
        self._end_date = end_date
        self._axis_y = axis_y
        self._data_norm = data_norm



    def correlation(self):
        '''
        --> Show the matrix correlation of selected indexes

        Returns: Plotly Imshow
                    Imshow to show correlation plot
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
            df_corr_viz = df_corr.mask(mask).dropna(how='all').dropna(axis='columns', how='all')
            fig = px.imshow(df_corr_viz, text_auto=True)
            st.plotly_chart(fig, use_container_width=True)
            

    def normalize_time_series(self):
        '''
        Transforms the time series into normalized form by dividing the series by the first record. 
        '''
        self._data_norm = self._data.copy()
        if len(self._axis_y) > 1:
            for column in self._axis_y:
                self._data_norm.loc[:, column] = self._data_norm.loc[:, column] / self._data_norm[column].values[0]
        else:
            self._data_norm.loc[:, self._axis_y] = self._data_norm.loc[:, self._axis_y] / self._data_norm[self._axis_y].values[0]


    def normalized_metric(self):
        '''
        Show the metric referal to increase or decrease in the period of normalized time series

        Returns: Pandas DataFrame
                    DataFrame with calculated metric
        ''' 
        dic = dict()
        for column in self._axis_y:  
            dic[column] = [round((self._data_norm[column].iloc[-1] - self._data_norm[column].iloc[0]), 2)]
        df = pd.DataFrame(dic).stack()
        df.rename(index='%', inplace=True)
        df = Styler(df, 2)
        st.write('Crescimento relativo %')
        st.dataframe(df)
