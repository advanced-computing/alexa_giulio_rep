import pytest
from unittest import mock
import spotifydataload


@mock.patch("spotifydataload.get_kaggle_api")
@mock.patch("spotifydataload.get_bq_credentials")
@mock.patch("spotifydataload.storage.Client")
@mock.patch("spotifydataload.bigquery.Client")
@mock.patch("spotifydataload.pd.read_csv")
@mock.patch("spotifydataload.zipfile.ZipFile")
def test_update_bigquery_from_kaggle(
    mock_zipfile, mock_read_csv, mock_bq_client, mock_storage_client, mock_get_credentials, mock_get_kaggle
):
    # Set up mocks
    mock_get_kaggle.return_value.dataset_download_files.return_value = None
    mock_get_credentials.return_value.project_id = "test-project"

    # Fake CSV data
    df_mock = mock.Mock()
    df_mock.__getitem__.return_value.max.return_value = "2024-12-31"
    df_mock["snapshot_date"].max.return_value = "2024-12-31"
    df_mock.__getitem__.side_effect = lambda key: df_mock
    df_mock[(df_mock["snapshot_date"] == "2024-12-31") & (df_mock["country"].isin.return_value)] = df_mock
    mock_read_csv.return_value = df_mock

    # Run
    result = spotifydataload.update_bigquery_from_kaggle()

    # Assert
    assert result == "2024-12-31"