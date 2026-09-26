import pandas as pd 
import pytest

from src.data_loader import load_csv, validate_dataframe

def test_load_csv(tmp_path):
    df = pd.DataFrame(
        {
            "item_id": ["A", "B"],
            "sales": [10, 20],
        }
    )

    file_path = tmp_path / "sample.csv"
    df.to_csv(file_path, index=False)

    result = load_csv(
        "sample.csv",
        data_dir=tmp_path,
    )
    
    assert len(result) == 2
    assert list(result.columns) == ["item_id", "sales"]

def test_load_csv_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_csv(
            "missing.csv",
            data_dir=tmp_path,
        )

def test_validate_empty_dataframe():
    empty_df = pd.DataFrame()

    with pytest.raises(ValueError):
        validate_dataframe(
            empty_df,
            "Test",
        )
                                    
