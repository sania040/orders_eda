from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "orders_raw.csv"
OUTPUT_DIR = BASE_DIR / "output"
CHARTS_DIR = OUTPUT_DIR / "charts"


def clean_orders(df):
    cleaned = df.copy()

    for column in ["region", "category"]:
        cleaned[column] = cleaned[column].astype("string").str.strip().str.title()

    cleaned["order_date"] = pd.to_datetime(cleaned["order_date"], errors="coerce")

    for column in ["quantity", "unit_price", "order_value"]:
        cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    essential_columns = [
        "order_id",
        "order_date",
        "region",
        "category",
        "quantity",
        "unit_price",
        "order_value",
    ]

    cleaned = cleaned.drop_duplicates()
    cleaned = cleaned.dropna(subset=essential_columns)
    cleaned = cleaned[
        (cleaned["quantity"] > 0)
        & (cleaned["unit_price"] > 0)
        & (cleaned["order_value"] > 0)
    ]

    return cleaned.reset_index(drop=True)


def inspect_data(df):
    print("FIRST FIVE ROWS")
    print(df.head().to_string(index=False))

    print("\nSHAPE")
    print(df.shape)

    print("\nCOLUMN NAMES")
    print(df.columns.tolist())

    print("\nDATA TYPES")
    print(df.dtypes)

    print("\nMISSING VALUES")
    print(df.isna().sum())

    print("\nDUPLICATE ROWS")
    print(df.duplicated().sum())

    print("\nUNIQUE REGIONS")
    print(sorted(df["region"].dropna().unique()))

    print("\nUNIQUE CATEGORIES")
    print(sorted(df["category"].dropna().unique()))

    print("\nTHREE ISSUES NOTICED")
    print("1. Some important numeric and date values are missing or invalid.")
    print("2. Some order values are negative or zero.")
    print("3. Region and category labels have extra spaces and mixed case.")


def explore_data(cleaned_df):
    print("\nORDER VALUE SUMMARY")
    print("Mean:", round(cleaned_df["order_value"].mean(), 2))
    print("Median:", round(cleaned_df["order_value"].median(), 2))
    print("Standard deviation:", round(cleaned_df["order_value"].std(), 2))

    print("\nSALES BY REGION")
    print(cleaned_df.groupby("region")["order_value"].sum().sort_values(ascending=False))

    print("\nCATEGORY COUNTS")
    print(cleaned_df["category"].value_counts())

    print("\nREGION VS CATEGORY")
    print(pd.crosstab(cleaned_df["region"], cleaned_df["category"]))


def draw_charts(cleaned_df):
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 5))
    sns.histplot(cleaned_df["order_value"], bins=20)
    plt.title("Histogram of Order Values")
    plt.xlabel("Order Value")
    plt.ylabel("Number of Orders")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "order_value_histogram.png")
    plt.close()

    sales_by_region = cleaned_df.groupby("region")["order_value"].sum().sort_values(ascending=False)

    plt.figure(figsize=(8, 5))
    sns.barplot(x=sales_by_region.index, y=sales_by_region.values)
    plt.title("Sales by Region")
    plt.xlabel("Region")
    plt.ylabel("Total Sales")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "sales_by_region.png")
    plt.close()

    scatter_df = cleaned_df.dropna(subset=["delivery_days", "order_value"])

    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=scatter_df, x="delivery_days", y="order_value")
    plt.title("Order Value vs Delivery Days")
    plt.xlabel("Delivery Days")
    plt.ylabel("Order Value")
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / "order_value_vs_delivery_days.png")
    plt.close()


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA_PATH)
    inspect_data(df)

    cleaned_df = clean_orders(df)

    print("\nCLEANED DATA PREVIEW")
    print(cleaned_df.head().to_string(index=False))
    print("Cleaned shape:", cleaned_df.shape)

    cleaned_df.to_csv(OUTPUT_DIR / "orders_cleaned.csv", index=False)

    report = pd.DataFrame(
        [
            {
                "rows_before_cleaning": len(df),
                "rows_after_cleaning": len(cleaned_df),
                "rows_removed": len(df) - len(cleaned_df),
            }
        ]
    )
    report.to_csv(OUTPUT_DIR / "data_quality_report.csv", index=False)

    explore_data(cleaned_df)
    draw_charts(cleaned_df)

    print("\nCleaning complete. Check the output folder for CSV files and charts.")


if __name__ == "__main__":
    main()
