#  Software Packages Project 📦

Interactive data analysis dashboard using **Python (Streamlit)** and complementary statistical processing using **SAS**. The project explores operational metrics and customer reviews for a tourism business.

---

## 📊 Project Overview

The project analyzes three years of monthly activity and customer review data from a tourism business — Casa Timiș. It includes:

- Exploratory Data Analysis (EDA)
- Missing value and outlier handling
- Data encoding and normalization
- Clustering (K-Means)
- Logistic and multiple linear regression
- Geolocation mapping (GeoPandas)
- Extended statistical analysis and reporting using SAS

---

## 🧰 Technologies Used

- **Python Packages**: `pandas`, `numpy`, `scikit-learn`, `statsmodels`, `streamlit`, `geopandas`
- **SAS Features**: `PROC IMPORT`, `PROC FORMAT`, `PROC SQL`, `PROC MEANS`, `PROC REG`, `PROC SGPLOT`, array processing

---

## 📁 Project Structure

| File/Folder                         | Description                                                  |
|------------------------------------|--------------------------------------------------------------|
| `.streamlit/config.toml`           | Streamlit theme configuration                                |
| `Casa_Timis_Customer_Reviews_3Y.csv` | Customer reviews & ratings                                   |
| `Casa_Timis_Monthly_Activity_3Y.csv` | Monthly performance KPIs                                     |
| `Project_Documentation_RO.pdf`     | Full project documentation (in Romanian)                     |
| `README.md`                        | You're reading it 😉                                         |
| `casa_timis.png`                   | Dashboard header image                                       |
| `dashboard.py`                     | Main Streamlit dashboard app                                 |
| `requirements.txt`                 | Python dependencies                                          |
| `sas_analysis.sas`                 | SAS script with data processing, analysis & visualization    |

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

### ▶️ How to Run the Python App Locally

```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

---

## 📘 SAS Analysis Features

The `sas_analysis.sas` script extends the Python-based dashboard with traditional statistical processing using SAS. It includes:

- Importing `.csv` files as SAS datasets  
- Creating custom formats for review scores and guest volume  
- Conditional categorization of complaints and occupancy levels  
- Subsetting months by low revenue or low scores  
- Calculating new variables via `ARRAY` (e.g., revenue per guest)  
- Joining datasets with SQL for integrated reporting  
- Generating monthly and seasonal charts  
- Running descriptive statistics and regression models  
- Visualizing trends with `PROC SGPLOT`  
- Predicting revenue with multiple linear regression  


### ▶️ How to Run the SAS Analysis Locally

To execute the SAS script and generate all outputs:

1. **Open** SAS Studio (or your preferred SAS environment).
2. **Update the file paths** in `sas_analysis.sas` to reflect your local setup. For example:

   ```sas
   datafile='/your/local/path/Casa_Timis_Monthly_Activity_3Y.csv'
   ```

3. **Load the script** `sas_analysis.sas` into the SAS editor.
4. **Run the full program** to generate all processed datasets, charts, and statistical results.

> ⚠️ *Make sure both CSV files are accessible from the updated paths for the import procedures to work correctly.*
