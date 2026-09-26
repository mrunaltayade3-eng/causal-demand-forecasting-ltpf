from pathlib import Path

import pandas as pd 

from src.config import RAW_DATA_DIR

def load_csv(filename: str, data_dir: Path = RAW_DATA_DIR) -> pd.DataFrame:
    """"
    Load a CSV file from the raw data directory
    """
    file_path = data_dir / filename

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    return pd.read_csv(file_path)

def validate_dataframe(df: pd.DataFrame, name: str) -> None:
    """
    Perfrom basic validation checks on a dataframe.
    """
    if df. empty:
        raise ValueError(f"{name} dataset is empty")
    
    duplicate_count = df.duplicate().sum

    print(f"{name}")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns):,}")
    print(f"Duplicate rows: {duplicate_count:,}")
    print(f"Missing values: {df.isna().sum().sum():,}")
    print("-" * 40)

def load_m5_data(
    data_dir: Path = RAW_DATA_DIR,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load the three core M5 forecasting datasets.
    """

    sales = load_csv(
        "sales_train_validation.csv",
        data_dir,
    )

    calender = load_csv(
        "calender.csv",
        data_dir,
    )
    
    prices = load_csv(
        "sell_prices.csv",
        data_dir,
    )

    validate_dataframe(sales, "Sales")
    validate_dataframe(calender, "Calender")
    validate_dataframe(prices, "Prices")

    return sales, calender, prices
