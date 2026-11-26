# Order Insights Assignment

A beginner-to-intermediate pandas project that loads raw order data, checks quality, cleans it, explores it and builds a simple Streamlit dashboard.

## Project files

- `data/orders_raw.csv` - raw dataset copied from the workbook
- `order_insights_notebook.ipynb` - step-by-step notebook for Questions 2 to 9
- `cleaning.py` - script that produces the cleaned CSV, quality report and charts
- `app.py` - Streamlit dashboard for Question 10
- `requirements.txt` - only the libraries used in this assignment
- `output/orders_cleaned.csv` - cleaned dataset
- `output/data_quality_report.csv` - before, after and removed row counts
- `output/charts/` - three PNG charts
- `output/dashboard_screenshot.png` - add your dashboard screenshot here

## Setup

From this folder:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run the cleaning script

```powershell
python cleaning.py
```

This prints the data checks and creates the cleaned CSV, quality report and chart images in the `output` folder.

## Open the notebook

Open `order_insights_notebook.ipynb` in Jupyter or VS Code and run the cells in order. The notebook uses relative paths, so open it from this project folder.

## Run the dashboard

Run the cleaning script first so `output/orders_cleaned.csv` exists.

```powershell
python -m streamlit run app.py
```

Then use the sidebar to filter by region.

## Three issues noticed

1. Some values are missing or written as text such as `unknown` and `not_available`.
2. Some order values are negative or zero.
3. Region and category labels have extra spaces and mixed case.

## Cleaning decisions

- Extra spaces are removed and text is standardised in `region` and `category`.
- `order_date` is converted to datetime with invalid dates treated as missing.
- `quantity`, `unit_price` and `order_value` are converted to numeric values with invalid text treated as missing.
- Duplicate rows and rows missing essential order details are removed.
- Rows with `quantity`, `unit_price` or `order_value` of zero or less are removed.
- Rows with missing `delivery_days` are kept.

## Quality report

- Rows before cleaning: 223
- Rows after cleaning: 195
- Rows removed: 28
