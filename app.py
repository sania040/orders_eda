from pathlib import Path

import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
CLEANED_DATA_PATH = BASE_DIR / "output" / "orders_cleaned.csv"

st.set_page_config(page_title="Order Insights", layout="wide")
st.title("Order Insights Dashboard")
st.write("Use the sidebar to filter orders by region.")


@st.cache_data
def load_data(path):
    return pd.read_csv(path)


if not CLEANED_DATA_PATH.exists():
    st.error("Cleaned CSV not found. Run python cleaning.py first.")
    st.stop()

df = load_data(CLEANED_DATA_PATH)

regions = ["All"] + sorted(df["region"].dropna().unique())
selected_region = st.sidebar.selectbox("Select region", regions)

if selected_region == "All":
    filtered_df = df
else:
    filtered_df = df[df["region"] == selected_region]

col1, col2, col3 = st.columns(3)
col1.metric("Total Orders", len(filtered_df))
col2.metric("Total Sales", f"${filtered_df['order_value'].sum():,.2f}")
col3.metric("Average Order Value", f"${filtered_df['order_value'].mean():,.2f}")

st.subheader("Sales by Category")
sales_by_category = filtered_df.groupby("category")["order_value"].sum().sort_values(ascending=False)
st.bar_chart(sales_by_category)

st.subheader("Filtered Orders")
st.dataframe(filtered_df, width="stretch")
