from pathlib import Path

from src.data_loader import load_m5_data
from src.data_transform import build_forecasting_dataset


SAMPLE_DIR = Path("data/sample")


def main():
    SAMPLE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    sales, calendar, prices = load_m5_data()

    print("\nBuilding forecasting dataset...")

    dataset = build_forecasting_dataset(
        sales=sales,
        calendar=calendar,
        prices=prices,

        # Start small and validate pipeline first
        store_id="CA_1",
        cat_id="FOODS",
        max_items=25,
    )

    print("\nForecasting dataset:")
    print(dataset.head())

    print(
        f"\nRows: {len(dataset):,}"
    )

    print(
        f"Columns: {len(dataset.columns)}"
    )

    print(
        f"Date range: "
        f"{dataset['date'].min()} "
        f"to "
        f"{dataset['date'].max()}"
    )

    output_path = (
        SAMPLE_DIR /
        "m5_forecasting_sample.csv"
    )

    dataset.to_csv(
        output_path,
        index=False,
    )

    print(
        f"\nSaved sample dataset to "
        f"{output_path}"
    )


if __name__ == "__main__":
    main()