import pandas as pd
import numpy as np
import streamlit as st
import geopandas as gpd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.cluster import KMeans
import statsmodels.api as sm

# --- Load Data ---
activity_data = pd.read_csv('Casa_Timis_Monthly_Activity_3Y.csv')
reviews_data = pd.read_csv('Casa_Timis_Customers_Reviews_3Y.csv')

# --- Streamlit App Start ---
st.title('Casa Timis - Activity Dashboard') # ex 1

st.header('Monthly Activity Data')
st.dataframe(activity_data)

st.header('Customer Reviews Data')
st.dataframe(reviews_data)

