import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from catch_clean import BrazilianIndicators

data = BrazilianIndicators()
data.clean_data_bcb()
data.clean_data_ibge()
data = data.data_frame_indicators()


year = str(st.selectbox('Year', data['date'].dt.year.unique()))
data_slice = data.query(f'date >= @year')
st.dataframe(data_slice['Savings'])
st.text(f'Savings {data_slice["Savings"].sum().round(2)}%')