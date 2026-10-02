import os
import random
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd


def generate_sales_dataset(csv_path: str, num_rows: int = 120) -> pd.DataFrame:
    """Generate a sample sales dataset and save it to CSV."""
    products = [
        {"Product": "Laptop", "Category": "Electronics", "UnitPrice": 1200},
        {"Product": "Smartphone", "Category": "Electronics", "UnitPrice": 800},
        {"Product": "Headphones", "Category": "Accessories", "UnitPrice": 120},
        {"Product": "Monitor", "Category": "Electronics", "UnitPrice": 300},
        {"Product": "Printer", "Category": "Office", "UnitPrice": 200},
        {"Product": "Desk Chair", "Category": "Furniture", "UnitPrice": 180},
        {"Product": "Coffee Maker", "Category": "Home", "UnitPrice": 90},
        {"Product": "Backpack", "Category": "Accessories", "UnitPrice": 70},
        {"Product": "Webcam", "Category": "Electronics", "UnitPrice": 110},
        {"Product": "Notebook", "Category": "Office", "UnitPrice": 15},
    ]
    regions = ["North", "South", "East", "West"]
    start_date = datetime(2025, 1, 1)

    rows = []
    for i in range(1, num_rows + 1):
        row_date = start_date + timedelta(days=random.randint(0, 180))
        item = random.choice(products)
        units_sold = random.randint(1, 15)
        total_sales = units_sold * item["UnitPrice"]

        rows.append(
            {
                "OrderID": f"ORD{i:04d}",
                "Date": row_date.strftime("%Y-%m-%d"),
                "Product": item["Product"],
                "Category": item["Category"],
                "UnitsSold": units_sold,
                "UnitPrice": item["UnitPrice"],
                "TotalSales": total_sales,
                "Region": random.choice(regions),
            }
        )

    # Add a few rows with missing values to demonstrate cleaning.
    rows.append(
        {
            "OrderID": "ORD9999",
            "Date": "2025-07-01",
            "Product": None,
            "Category": "Electronics",
            "UnitsSold": 3,
            "UnitPrice": 1200,
            "TotalSales": 3600,
            "Region": "North",
        }
    )
    rows.append(
        {
            "OrderID": "ORD10000",
            "Date": "2025-07-02",
            "Product": "Smartphone",
            "Category": "Electronics",
            "UnitsSold": None,
            "UnitPrice": 800,
            "TotalSales": None,
            "Region": "East",
        }
    )

    df = pd.DataFrame(rows)
    df.to_csv(csv_path, index=False)
    return df


def load_and_clean_data(csv_path: str) -> pd.DataFrame:
    """Load sales data from CSV and clean missing or invalid values."""
    df = pd.read_csv(csv_path)
    print("Initial dataset loaded:", len(df), "rows")

    # Remove rows with missing required information.
    df = df.dropna(subset=["Product", "Category", "UnitsSold", "UnitPrice"])
    print("After dropping missing values:", len(df), "rows")

    # Convert numeric columns to the right type and keep only valid positive values.
    df["UnitsSold"] = pd.to_numeric(df["UnitsSold"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
    df = df.dropna(subset=["UnitsSold", "UnitPrice"])
    df = df[df["UnitsSold"] > 0]
    df = df[df["UnitPrice"] > 0]

    # Recalculate TotalSales to ensure consistency.
    df["TotalSales"] = df["UnitsSold"] * df["UnitPrice"]

    # Remove exact duplicate rows if any.
    df = df.drop_duplicates()
    print("After cleaning and deduplication:", len(df), "rows")

    return df


def calculate_summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate statistics for numeric sales columns."""
    summary = df[["UnitsSold", "UnitPrice", "TotalSales"]].describe()
    print("\nSummary statistics:")
    print(summary)
    return summary


def identify_best_selling_product(df: pd.DataFrame) -> pd.Series:
    """Find the product with the highest total sales."""
    product_summary = (
        df.groupby("Product")["TotalSales", "UnitsSold"]
        .sum()
        .sort_values(by="TotalSales", ascending=False)
    )
    best_product = product_summary.iloc[0]
    print("\nBest-selling product:")
    print(product_summary.head(5))
    return best_product


def create_charts(df: pd.DataFrame, chart_dir: str) -> None:
    """Create and save three charts based on the cleaned sales data."""
    os.makedirs(chart_dir, exist_ok=True)

    # Chart 1: Total sales by product
    sales_by_product = df.groupby("Product")["TotalSales"].sum().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    sales_by_product.plot(kind="bar", color="#4C72B0")
    plt.title("Total Sales by Product")
    plt.xlabel("Product")
    plt.ylabel("Total Sales")
    plt.tight_layout()
    chart_path = os.path.join(chart_dir, "sales_by_product.png")
    plt.savefig(chart_path)
    plt.close()
    print("Saved chart:", chart_path)

    # Chart 2: Units sold by category
    units_by_category = df.groupby("Category")["UnitsSold"].sum()
    plt.figure(figsize=(8, 8))
    units_by_category.plot(kind="pie", autopct="%.1f%%", startangle=140)
    plt.title("Units Sold by Category")
    plt.ylabel("")
    plt.tight_layout()
    chart_path = os.path.join(chart_dir, "sales_by_category.png")
    plt.savefig(chart_path)
    plt.close()
    print("Saved chart:", chart_path)

    # Chart 3: Monthly sales trend
    df["Date"] = pd.to_datetime(df["Date"])
    monthly_sales = df.resample("M", on="Date")["TotalSales"].sum()
    plt.figure(figsize=(10, 6))
    monthly_sales.plot(marker="o", linestyle="-")
    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Sales")
    plt.grid(True)
    plt.tight_layout()
    chart_path = os.path.join(chart_dir, "monthly_sales_trend.png")
    plt.savefig(chart_path)
    plt.close()
    print("Saved chart:", chart_path)


def main() -> None:
    """Main entry point for the sales data analysis project."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    chart_dir = os.path.join(base_dir, "charts")
    os.makedirs(data_dir, exist_ok=True)

    csv_path = os.path.join(data_dir, "sales_data.csv")

    # Generate the dataset if it does not exist.
    if not os.path.exists(csv_path):
        print("Generating sample dataset...")
        generate_sales_dataset(csv_path)
        print(f"Dataset saved to {csv_path}\n")
    else:
        print(f"Using existing dataset at {csv_path}\n")

    sales_df = load_and_clean_data(csv_path)
    calculate_summary_statistics(sales_df)
    best_product = identify_best_selling_product(sales_df)

    print("\nTop-performing product:")
    print(best_product)

    create_charts(sales_df, chart_dir)


if __name__ == "__main__":
    main()
