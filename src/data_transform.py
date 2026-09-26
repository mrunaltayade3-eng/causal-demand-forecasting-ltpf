from typing import Optional

import pandas as pd


ID_COLUMNS = [
    "id",
    "item_id",
    "dept_id",
    "cat_id",
    "store_id",
    "state_id",
]


def filter_sales(
    sales: pd.DataFrame,
    store_id: Optional[str] = None,
    cat_id: Optional[str] = None,
    max_items: Optional[int] = None,
) -> pd.DataFrame:
    """
    Filter the wide M5 sales table before reshaping.

    Filtering first avoids converting the entire M5 dataset
    into tens of millions of long-format rows.
    """

    data = sales.copy()

    if store_id is not None:
        data = data[data["store_id"] == store_id]

    if cat_id is not None:
        data = data[data["cat_id"] == cat_id]

    if max_items is not None:
        selected_items = (
            data["item_id"]
            .drop_duplicates()
            .head(max_items)
        )

        data = data[
            data["item_id"].isin(selected_items)
        ]

    return data


def reshape_sales_long(
    sales: pd.DataFrame,
) -> pd.DataFrame:
    """
    Convert M5 sales data from wide daily columns
    (d_1, d_2, ...) into long format.
    """

    day_columns = [
        column
        for column in sales.columns
        if column.startswith("d_")
    ]

    long_sales = sales.melt(
        id_vars=ID_COLUMNS,
        value_vars=day_columns,
        var_name="d",
        value_name="sales",
    )

    return long_sales


def merge_calendar(
    sales_long: pd.DataFrame,
    calendar: pd.DataFrame,
) -> pd.DataFrame:
    """
    Join daily calendar, holiday, event,
    and SNAP information.
    """

    columns = [
        "d",
        "date",
        "wm_yr_wk",
        "wday",
        "weekday",
        "month",
        "year",
        "event_name_1",
        "event_type_1",
        "event_name_2",
        "event_type_2",
        "snap_CA",
        "snap_TX",
        "snap_WI",
    ]

    data = sales_long.merge(
        calendar[columns],
        on="d",
        how="left",
        validate="many_to_one",
    )

    data["date"] = pd.to_datetime(data["date"])

    return data


def merge_prices(
    data: pd.DataFrame,
    prices: pd.DataFrame,
) -> pd.DataFrame:
    """
    Add weekly selling price information using
    store, item, and Walmart week identifiers.
    """

    merged = data.merge(
        prices,
        on=[
            "store_id",
            "item_id",
            "wm_yr_wk",
        ],
        how="left",
        validate="many_to_one",
    )

    return merged


def build_forecasting_dataset(
    sales: pd.DataFrame,
    calendar: pd.DataFrame,
    prices: pd.DataFrame,
    store_id: Optional[str] = None,
    cat_id: Optional[str] = None,
    max_items: Optional[int] = None,
) -> pd.DataFrame:
    """
    Build a forecasting-ready M5 dataset.
    """

    filtered = filter_sales(
        sales,
        store_id=store_id,
        cat_id=cat_id,
        max_items=max_items,
    )

    long_sales = reshape_sales_long(filtered)

    data = merge_calendar(
        long_sales,
        calendar,
    )

    data = merge_prices(
        data,
        prices,
    )

    data = data.sort_values(
        ["store_id", "item_id", "date"]
    ).reset_index(drop=True)

    return data