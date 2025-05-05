import pandas as pd
import numpy as np
import streamlit as st
import geopandas as gpd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.cluster import KMeans
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler

# ----- Load Data -----

activity_data = pd.read_csv('Casa_Timis_Monthly_Activity_3Y.csv')
reviews_data = pd.read_csv('Casa_Timis_Customer_Reviews_3Y.csv')

# ----- Streamlit App Start -----

st.image('casa_timis.png', use_container_width=True)
st.title('Casa Timis - Activity Dashboard') #  -> ex 1
st.divider()

st.subheader('📈 Monthly Activity Data')
st.dataframe(activity_data)

st.subheader('⭐ Customer Reviews Data')
st.dataframe(reviews_data)

# ----- Using the geopandas package -----

gdf = gpd.GeoDataFrame(
    {'Organization': ['Casa Timis']},
    geometry=gpd.points_from_xy([26.122790776872254], [44.981385052765894]),
    crs='EPSG:4326' # standard EPSG:4326 - classic GPS coordinate system
)

gdf['latitude'] = gdf.geometry.y
gdf['longitude'] = gdf.geometry.x

st.divider()
st.subheader('📍 Casa Timis - Location Map')
st.map(gdf[['latitude','longitude']])
st.divider()

# ----- Handling missing and extreme values -----

# Detecting missing values in all columns
st.subheader('🔍 Complete check for missing values')
missing_activity = activity_data.isna().sum()
missing_reviews = reviews_data.isna().sum()

if missing_activity.sum() == 0 and missing_reviews.sum() == 0:
    st.success('There are no missing values in any of the datasets.')
else:
    st.warning('❌ Missing values detected:')
    
    # Extract only columns with missing values
    missing_activity_display = missing_activity[missing_activity > 0].reset_index()
    missing_activity_display.columns = ['Column', 'Missing Values']
    st.write('**Activity Data:**')
    st.dataframe(missing_activity_display, hide_index=True)
    
    missing_reviews_display = missing_reviews[missing_reviews > 0].reset_index()
    missing_reviews_display.columns = ['Column', 'Missing Values']
    st.write('**Reviews Data:**')
    st.dataframe(missing_reviews_display, hide_index=True)

# Handle missing values
def fill_missing_values(df):
    for column in df.columns:
        if df[column].dtype in [np.float64, np.int64]:
            df[column].fillna(df[column].median(), inplace=True)
        else:
            df[column].fillna(df[column].mode()[0], inplace=True)
    return df

# Apply the handling function to both datasets
activity_data = fill_missing_values(activity_data)
reviews_data = fill_missing_values(reviews_data)

# Final check
missing_activity_after = activity_data.isna().sum().sum()
missing_reviews_after = reviews_data.isna().sum().sum()

if missing_activity_after == 0 and missing_reviews_after == 0:
    st.success('✔️ All missing values have been successfully handled.')
else:
    st.warning('⚠️ Some missing values remain unhandled.')

# Display datasets after cleaning
st.subheader('📄 Data after cleaning - Activity Data')
st.dataframe(activity_data)
st.subheader('📄 Data after cleaning - Customer Reviews')
st.dataframe(reviews_data)
st.divider()

# Handle extreme values in Number_of_Guests
st.subheader('📛 Outlier check for number of guests')
# Set threshold
outlier_threshold = 1500
# Detect outliers
outliers_df = activity_data[activity_data['Number_of_Guests'] > outlier_threshold]
num_outliers = len(outliers_df)

# Replacing outliers with the median
if num_outliers == 0:
    st.success('There are no outliers in Number_of_Guests.')
else:
    st.warning(f'⚠️ {num_outliers} outlier(s) detected in Number_of_Guests (value > {outlier_threshold}):')
    st.dataframe(outliers_df[['Month_Year', 'Number_of_Guests']])

    # Replace outliers with median of non-outliers
    median_guests = activity_data.loc[activity_data['Number_of_Guests'] <= outlier_threshold, 'Number_of_Guests'].median()
    activity_data.loc[activity_data['Number_of_Guests'] > outlier_threshold, 'Number_of_Guests'] = median_guests

    st.info(f'✅ Replaced {num_outliers} extreme values with the median: {median_guests}')
    st.divider()

# ----- Data encoding methods -----

# Extract year and month as new variables (OneHotEncoder for month)
activity_data['Year'] = activity_data['Month_Year'].apply(lambda x: x.split(' ')[-1])
activity_data['Month'] = activity_data['Month_Year'].apply(lambda x: x.split(' ')[0])
encoder = OneHotEncoder(sparse_output=False)
month_encoded = encoder.fit_transform(activity_data[['Month']])

# Display data after month encoding
st.subheader('🗓️ Encoded Month Data')
encoded_month_df = pd.DataFrame(month_encoded, columns=encoder.get_feature_names_out(['Month']))
st.dataframe(encoded_month_df)
st.divider()

# ----- Scaling methods -----

scalar = StandardScaler()
# Scale selected numerical columns
columns_to_scale = [
    'Number_of_Guests',
    'Occupancy_Rate_Percent',
    'Average_Room_Price_EUR'
]
activity_data[columns_to_scale] = scalar.fit_transform(activity_data[columns_to_scale])

# Display data after scaling 
st.subheader('📐 Scaled Numerical Data')
st.dataframe(activity_data[['Number_of_Guests', 'Occupancy_Rate_Percent', 'Average_Room_Price_EUR']])
# Update the columns Number_of_Guests, Occupancy_Rate_Percent, Average_Room_Price_EUR in activity_data with the new scaled values

# ----- Statistical processing: grouping and aggregation -----

with st.container():
    st.divider()
    st.subheader('📊 Yearly Trends')

    # Average revenue per year
    revenue_per_year = activity_data.groupby('Year')['Total_Revenue_EUR'].mean()
    st.write('**Average Total Revenue per Year**')
    st.bar_chart(revenue_per_year)

    # Group by year and calculate average number of guests
    guests_group = activity_data.groupby('Year')['Number_of_Guests'].mean()
    st.write('**Average Number of Guests per Year**')
    st.line_chart(guests_group)

# ----- Using the scikit-learn package -----

# Clustering months based on revenue and number of guests
k_means = KMeans(n_clusters=3, random_state=42)
activity_data['Cluster']=k_means.fit_predict(activity_data[['Total_Revenue_EUR', 'Number_of_Guests']])
st.divider()
st.subheader('🔍 Cluster Assignments') 
st.dataframe(activity_data[['Month_Year', 'Cluster']])
st.divider()

# Logistic regression
st.subheader('Logistic Regression Model Evaluation')
# Data preparation
x = activity_data[['Total_Revenue_EUR', 'Number_of_Guests']]
y = activity_data['Cluster']

# Splitting the data into training and test sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Data normalization
scalar = StandardScaler()
x_train_scaler = scalar.fit_transform(x_train)
x_test_scaled = scalar.transform(x_test)

# Training the model
log_reg = LogisticRegression(multi_class='ovr', random_state=42)
log_reg.fit(x_train_scaler, y_train)

# Predictions
y_pred = log_reg.predict(x_test_scaled)

# Model evaluation
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, output_dict=True)

# Display results
st.write(f'**Accuracy:** {accuracy:.2f}')
st.write('### Detailed Classification Report:')
st.dataframe(pd.DataFrame(report).transpose().round(2))
st.divider()

# ----- Using the statsmodels package (Multiple regression) -----

with st.container():
    st.subheader('📉 Regression Analysis')
    # Predicting total revenue based on number of guests and occupancy rate    
    x = activity_data[['Number_of_Guests', 'Occupancy_Rate_Percent']]
    x = sm.add_constant(x) # Add constant for intercept
    y = activity_data['Total_Revenue_EUR']

    model = sm.OLS(y, x).fit()
    st.write('**Multiple Regression Summary**')

    # Create summary DataFrame with regression coefficients and statistics
    results_summary = pd.DataFrame({
        'Coefficient': model.params,
        'Standard Error': model.bse,
        't-statistic': model.tvalues,
        'P>|t|': model.pvalues,
        '2.5% Interval': model.conf_int()[0],
        '97.5% Interval': model.conf_int()[1]
    }).round(3)
    st.dataframe(results_summary)

    # Create summary DataFrame with additional model statistics
    additional_info = pd.DataFrame({
        'Statistic': ['R-squared', 'Adj. R-squared', 'F-statistic', 'Prob (F-statistic)'],
        'Value': [model.rsquared, model.rsquared_adj, model.fvalue, model.f_pvalue]
    }).round(3)
    st.write('**Additional Model Statistics**')
    st.dataframe(additional_info)

