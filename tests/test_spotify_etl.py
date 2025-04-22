import os
import pytest
from unittest.mock import patch

# Skip test if no Kaggle credentials
@pytest.mark.skipif(
    not os.getenv("KAGGLE_USERNAME") or not os.getenv("KAGGLE_KEY"),
    reason="Kaggle credentials not set"
)
@patch("spotifydataload.KaggleApi")
def test_update_bigquery_from_kaggle(mock_kaggle_api):
    from spotifydataload import update_bigquery_from_kaggle
    mock_api_instance = mock_kaggle_api.return_value
    mock_api_instance.authenticate.return_value = None
    mock_api_instance.dataset_download_files.return_value = None

    result = update_bigquery_from_kaggle()
    assert result is None or isinstance(result, str)