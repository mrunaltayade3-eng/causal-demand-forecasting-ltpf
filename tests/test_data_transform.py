import pandas as pd

from src.data_transform import (
    filter_sales,
    reshape_sales_long,
    merge_calendar,
    merge_prices,
)


def create_sales_sample():
    return pd.DataFrame(
        {
            "id": ["A_validation", "B_validation"],
            "item_id": ["A", "B"],
            "dept_id": ["FOODS_1", "FOODS_1"],
            "cat_id": ["FOODS", "FOODS"],
            "store_id": ["CA_1", "CA_1"],
            "state_id": ["CA", "CA"],
            "d_1": [1, 2],
            "d_2": [3, 4],
        }
    )


def create_calendar_sample():
    return pd.DataFrame(
        {
            "d": ["d_1", "d_2"],
            "date": ["2011-01-29", "2011-01-30"],
            "wm_yr_wk": [11101, 11101],
            "wday": [1, 2],
            "weekday": ["Saturday", "Sunday"],
            "month": [1, 1],
            "year": [2011, 2011],
            "event_name_1": [None, None],
            "event_type_1": [None, None],
            "event_name_2": [None, None],
            "event_type_2": [None, None],
            "snap_CA": [0, 0],
            "snap_TX": [0, 0],
            "snap_WI": [0, 0],
        }
    )


def test_filter_sales():
    sales = create_sales_sample()

    result = filter_sales(
        sales,
        store_id="CA_1",
        cat_id="FOODS",
        max_items=1,
    )

    assert len(result) == 1
    assert result["item_id"].nunique() == 1
    assert result["store_id"].iloc[0] == "CA_1"
    assert result["cat_id"].iloc[0] == "FOODS"


def test_reshape_sales_long():
    sales = create_sales_sample()

    result = reshape_sales_long(sales)

    assert len(result) == 4
    assert "d" in result.columns
    assert "sales" in result.columns
    assert set(result["d"]) == {"d_1", "d_2"}


def test_merge_calendar():
    sales = create_sales_sample()
    calendar = create_calendar_sample()

    long_sales = reshape_sales_long(sales)

    result = merge_calendar(
        long_sales,
        calendar,
    )

    assert "date" in result.columns
    assert "wm_yr_wk" in result.columns
    assert "event_name_1" in result.columns
    assert result["date"].notna().all()
    assert result["wm_yr_wk"].notna().all()


def test_merge_prices():
    sales = create_sales_sample()
    calendar = create_calendar_sample()

    long_sales = reshape_sales_long(sales)

    merged_calendar = merge_calendar(
        long_sales,
        calendar,
    )

    prices = pd.DataFrame(
        {
            "store_id": ["CA_1", "CA_1"],
            "item_id": ["A", "B"],
            "wm_yr_wk": [11101, 11101],
            "sell_price": [2.50, 3.00],
        }
    )

    result = merge_prices(
        merged_calendar,
        prices,
    )

    assert "sell_price" in result.columns
    assert result["sell_price"].notna().all()

    assert set(
        result["sell_price"].unique()
    ) == {2.50, 3.00}