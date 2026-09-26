from pathlib import Path

import pandas as pd

from src.config import RAW_DATA_DIR


def load_csv(
    filename: str,
    data_dir: Path = RAW_DATA_DIR,
) -> pd.DataFrame:
    file_path = data_dir / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    return pd.read_csv(file_path)


def validate_dataframe(
    df: pd.DataFrame,
    name: str,
) -> None:
    if df.empty:
        raise ValueError(
            f"{name} dataset is empty"
        )

    duplicate_count = df.duplicated().sum()

    print(f"\n{name}")
    print("-" * 40)
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns):,}")
    print(
        f"Duplicate rows: "
        f"{duplicate_count:,}"
    )
    print(
        f"Missing values: "
        f"{df.isna().sum().sum():,}"
    )


def load_m5_data(
    data_dir: Path = RAW_DATA_DIR,
):
    print("Loading M5 datasets...")

    sales = load_csv(
        "sales_train_validation.csv",
        data_dir,
    )

    calendar = load_csv(
        "calendar.csv",
        data_dir,
    )

    prices = load_csv(
        "sell_prices.csv",
        data_dir,
    )

    validate_dataframe(
        sales,
        "Sales",
    )

    validate_dataframe(
        calendar,
        "Calendar",
    )

    validate_dataframe(
        prices,
        "Prices",
    )

    return sales, calendar, prices