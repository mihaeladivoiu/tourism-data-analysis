# 📦 Software Packages Project

This is a student project combining interactive data visualization with statistical and machine learning analysis, using **Python (Streamlit)** and **SAS**.

---

## 📊 Project Overview

The project analyzes three years of monthly activity and customer review data from a tourism business — Casa Timiș. It includes:

- Exploratory Data Analysis (EDA)
- Missing value and outlier handling
- Data encoding and normalization
- Clustering (K-Means)
- Logistic and multiple linear regression
- Geolocation mapping (GeoPandas)
- SAS-based statistical analysis, custom formatting, data transformations, and reporting

---

## 🧰 Technologies Used

- **Python Packages**: `pandas`, `numpy`, `scikit-learn`, `statsmodels`, `streamlit`, `geopandas`
- **SAS Features**: `PROC IMPORT`, `PROC FORMAT`, `PROC SQL`, `PROC MEANS`, `PROC REG`, `PROC SGPLOT`, array processing

---

## 📁 Project Structure

| File/Folder                         | Description                                                  |
|------------------------------------|--------------------------------------------------------------|
| `dashboard.py`                     | Main Streamlit dashboard app                                 |
| `Casa_Timis_Monthly_Activity_3Y.csv` | Monthly performance KPIs                                     |
| `Casa_Timis_Customer_Reviews_3Y.csv` | Customer reviews & ratings                                   |
| `sas_analysis.sas`                 | SAS script with data processing, analysis & visualization    |
| `casa_timis.png`                   | Dashboard header image                                       |
| `requirements.txt`                 | Python dependencies                                          |
| `.streamlit/config.toml`           | Streamlit theme configuration                                |
| `README.md`                        | This file                                                    |

---

## 🧪 Python App Features

- Displays datasets in interactive tables
- Identifies and fixes missing values
- Detects and replaces outliers
- Encodes and scales features for modeling
- Clusters months using K-Means
- Builds and evaluates a logistic regression model
- Performs multiple linear regression using `statsmodels`
- Displays regression summaries and statistics
- Visualizes KPIs over time
- Maps business location with `geopandas`

To run locally:

```bash
pip install -r requirements.txt
streamlit run dashboard.py
