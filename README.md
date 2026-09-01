# 📊 Tourism Data Analysis

A data analysis project exploring three years of operational metrics and customer reviews for a tourism business using Python, Streamlit, and SAS.

The project combines exploratory data analysis, data preprocessing, clustering, regression models, geospatial visualization, and statistical reporting through an interactive Streamlit dashboard and complementary SAS analysis.

---

## ✨ Key Features

- Exploratory Data Analysis (EDA)
- Missing value and outlier handling
- Data encoding and normalization
- K-Means clustering
- Logistic regression
- Multiple linear regression
- Interactive KPI visualization
- Geospatial visualization with GeoPandas
- Extended statistical analysis and reporting with SAS

---

## 🧰 Technologies Used

- **Python**: `pandas`, `numpy`, `scikit-learn`, `statsmodels`, `streamlit`, `geopandas`
- **SAS**: `PROC IMPORT`, `PROC FORMAT`, `PROC SQL`, `PROC MEANS`, `PROC REG`, `PROC SGPLOT`, array processing

---

## 📁 Project Structure

| File/Folder | Description |
|---|---|
| `.streamlit/config.toml` | Streamlit theme configuration |
| `Casa_Timis_Customer_Reviews_3Y.csv` | Customer reviews and ratings |
| `Casa_Timis_Monthly_Activity_3Y.csv` | Monthly performance KPIs |
| `Project_Documentation_RO.pdf` | Full project documentation in Romanian |
| `README.md` | Project overview and setup instructions |
| `casa_timis.png` | Dashboard header image |
| `dashboard.py` | Main Streamlit dashboard application |
| `requirements.txt` | Python dependencies |
| `sas_analysis.sas` | SAS data processing, analysis, and visualization script |

---

## 🧪 Python Analysis

The Streamlit application provides an interactive interface for exploring and analyzing the datasets.

It includes:

- Interactive dataset visualization
- Missing value identification and handling
- Outlier detection and replacement
- Feature encoding and scaling
- K-Means clustering of monthly activity
- Logistic regression modeling and evaluation
- Multiple linear regression using `statsmodels`
- Regression summaries and statistical metrics
- KPI visualization over time
- Business location mapping with GeoPandas

### ▶️ Run the Streamlit App

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
streamlit run dashboard.py
```

---

## 📘 SAS Analysis

The `sas_analysis.sas` script complements the Python application with additional statistical processing and reporting.

The analysis includes:

- Importing CSV files as SAS datasets
- Creating custom formats for review scores and guest volume
- Conditional categorization of complaints and occupancy levels
- Subsetting observations based on revenue and review scores
- Calculating derived variables using `ARRAY`
- Joining datasets with `PROC SQL`
- Generating descriptive statistics
- Creating monthly and seasonal visualizations
- Running regression models
- Predicting revenue using multiple linear regression

### ▶️ Run the SAS Analysis

1. Open SAS Studio or another compatible SAS environment.
2. Update the dataset paths in `sas_analysis.sas` to match your local environment:

```sas
datafile='/your/local/path/Casa_Timis_Monthly_Activity_3Y.csv'
```

3. Load `sas_analysis.sas` into the SAS editor.
4. Run the script to generate the processed datasets, statistical analyses, and visualizations.

> **Note:** Both CSV files must be accessible from the paths configured in the SAS script.
