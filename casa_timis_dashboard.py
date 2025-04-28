import pandas as pd
import numpy as np
import streamlit as st
import geopandas as gpd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.cluster import KMeans
import statsmodels.api as sm

# --- Load Data ---
activity_data = pd.read_csv('Casa_Timis_Monthly_Activity_3Y.csv')
reviews_data = pd.read_csv('Casa_Timis_Customer_Reviews_3Y.csv')

# --- Streamlit App Start ---

st.image('casa_timis.png', use_container_width=True)
st.title('Casa Timis - Activity Dashboard') #  -> ex 1
st.divider()

st.subheader('📈 Monthly Activity Data')
st.dataframe(activity_data)

st.subheader('⭐ Customer Reviews Data')
st.dataframe(reviews_data)

# --- Utilizarea pachetului geopandas ---   -> ex 2
#crs Coordinate Reference System
gdf = gpd.GeoDataFrame(
    {'Organization': ['Casa Timis']},
    geometry=gpd.points_from_xy([26.122790776872254], [44.981385052765894]),
    crs='EPSG:4326' # standard EPSG:4326 - sistemul de coordonate GPS clasic
)

gdf['latitude'] = gdf.geometry.y
gdf['longitude'] = gdf.geometry.x

st.divider()
st.subheader('📍 Casa Timis - Location Map')
st.map(gdf[['latitude','longitude']])
st.divider()

# --- Tratare valori lipsa si valori extreme ---    -> ex 3

#conversie
activity_data['Spa_Revenue_EUR'] = activity_data['Spa_Revenue_EUR'].astype(float)
reviews_data['Average_Review_Score'] = reviews_data['Average_Review_Score'].astype(float)

#tratare valori lipsa
activity_data['Spa_Revenue_EUR'].fillna(activity_data['Spa_Revenue_EUR'].median(), inplace=True)
reviews_data['Average_Review_Score'].fillna(reviews_data['Average_Review_Score'].mean(), inplace=True)

#tratare valori extreme -> Number_of_Guests > 1500 outlier
activity_data.loc[activity_data['Number_of_Guests']>1500, 'Number_of_Guests'] = activity_data['Number_of_Guests'].median()

# --- Metode de codificare a datelor ---    -> ex 4
# Extragem anul si luna ca variabile noi (OneHotEncoder pentru luna)
activity_data['Year'] = activity_data['Month_Year'].apply(lambda x: x.split(' ')[-1])
activity_data['Month'] = activity_data['Month_Year'].apply(lambda x: x.split(' ')[0])
encoder = OneHotEncoder(sparse_output=False)
month_encoded = encoder.fit_transform(activity_data[['Month']])

# --- Metode de scalare ---   -> ex 5
scalar = StandardScaler()
activity_data[['Number_of_Guests', 
               'Occupancy_Rate_%', 
               'Average_Room_Price_EUR']] = scalar.fit_transform(activity_data[['Number_of_Guests', 
                                                                                'Occupancy_Rate_%', 
                                                                                'Average_Room_Price_EUR']])

#Actualizează coloanele Number_of_Guests, Occupancy_Rate_%, Average_Room_Price_EUR în activity_data cu noile valori scalate.

# --- Prelucrari statistice: grupare si agregare ---  -> ex 6

with st.container():
    st.subheader('📊 Yearly Trends')
    #Media veniturilor pe fiecare an
    revenue_per_year = activity_data.groupby('Year')['Total_Revenue_EUR'].mean()
    st.write('**Average Total Revenue per Year**')
    st.bar_chart(revenue_per_year)

    # --- Utilizarea functiilor de grup ---   -> ex 7
    #grupare dupa an si calcul medie oaspeti
    guests_group = activity_data.groupby('Year')['Number_of_Guests'].mean()
    st.write('**Average Number of Guests per Year**')
    st.line_chart(guests_group)

# --- Utilizarea pachetului scikit-learn (Clusterizare) ---   -> ex 8  

#TODO REGRESIE LINIARA !!!!!!!!!

#clusterizare luni in functie de venit si oaspeti
k_means = KMeans(n_clusters=3, random_state=42)
activity_data['Cluster']=k_means.fit_predict(activity_data[['Total_Revenue_EUR', 'Number_of_Guests']])
st.divider()
st.subheader('🔍 Cluster Assignments')
st.dataframe(activity_data[['Month_Year', 'Cluster']])
st.divider()

# --- Utilizarea pachetului statmodels (Regresie multipla) ---  -> ex 9

with st.container():
    st.subheader('📉 Regression Analysis')
    #predictie venit total pe baza numarului de oaspeti si rata ocuparii
    X = activity_data[['Number_of_Guests', 'Occupancy_Rate_%']]
    X = sm.add_constant(X) # adaugam constanta pentru intercept
    Y = activity_data['Total_Revenue_EUR']

    model = sm.OLS(Y, X).fit()
    st.write('**Multiple Regression Summary**')
    # st.text(model.summary())

    #creare DataFrame organizat pentru afisare rezultate
    results_summary = pd.DataFrame({
        'Coefficient': model.params,
        'Standard Error': model.bse,
        't-statistic': model.tvalues,
        'P>|t|': model.pvalues,
        '2.5% Interval': model.conf_int()[0],
        '97.5% Interval': model.conf_int()[1]
    }).round(3)

    st.dataframe(results_summary)

    additional_info = pd.DataFrame({
        'Statistic': ['R-squared', 'Adj. R-squared', 'F-statistic', 'Prob (F-statistic)'],
        'Value': [model.rsquared, model.rsquared_adj, model.fvalue, model.f_pvalue]
    }).round(3)

    st.write('**Additional Model Statistics**')
    st.dataframe(additional_info)

