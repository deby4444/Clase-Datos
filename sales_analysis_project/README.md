# Sales Data Analysis Project

This beginner-friendly Python project analyzes sales data using `pandas` and `matplotlib`.

## What it does
- Generates a sample sales dataset with at least 100 rows
- Cleans the data by removing missing or invalid rows
- Calculates summary statistics for `UnitsSold`, `UnitPrice`, and `TotalSales`
- Identifies the best-selling product by total sales
- Creates three charts and saves them to the `charts/` folder

## Requirements
- Python 3.8+
- `pandas`
- `matplotlib`

## Setup
```bash
python -m pip install -r requirements.txt
```

## Run the analysis
```bash
python src/sales_analysis.py
```

## Output
- `data/sales_data.csv` — generated sample dataset
- `charts/sales_by_product.png`
- `charts/sales_by_category.png`
- `charts/monthly_sales_trend.png`
