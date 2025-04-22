import pytest
import spotifydataload
from unittest import mock

@mock.patch("spotifydataload.get_kaggle_api")
@mock.patch("spotifydataload.get_bq_credentials")
@mock.patch("spotifydataload.storage.Client")
@mock.patch("spotifydataload.bigquery.Client")
@mock.patch("spotifydataload.pd.read_csv")
@mock.patch("spotifydataload.zipfile.ZipFile")
def test_update_bigquery_from_kaggle(
    mock_zipfile, mock_read_csv, mock_bq_client,
    mock_storage_client, mock_get_bq_credentials, mock_get_kaggle_api
):
    # --- Setup mocks ---
    mock_api = mock.Mock()
    mock_get_kaggle_api.return_value = mock_api

    mock_credentials = mock.Mock()
    mock_credentials.project_id = "test-project"
    mock_get_bq_credentials.return_value = mock_credentials

    mock_bucket = mock.Mock()
    mock_blob = mock.Mock()
    mock_bucket.blob.return_value = mock_blob
    mock_storage_client.return_value.bucket.return_value = mock_bucket

    mock_bq = mock.Mock()
    mock_bq_client.return_value = mock_bq
    mock_bq.load_table_from_uri.return_value.result.return_value = None

    mock_df = mock.Mock()
    mock_df.__getitem__.return_value.max.return_value = "2024-12-31"
    mock_df.__getitem__.side_effect = lambda col: ["US", "FR", "IT", "ES", "MX"] if col == "country" else ["2024-12-31"]
    mock_df["snapshot_date"].max.return_value = "2024-12-31"
    mock_read_csv.return_value = mock_df

    # --- Run test ---
    result = spotifydataload.update_bigquery_from_kaggle()

    # --- Assert ---
    assert result == "2024-12-31"
    mock_api.dataset_download_files.assert_called_once()
    mock_bq.load_table_from_uri.assert_called_once()
    mock_blob.upload_from_filename.assert_called_once()
    mock_read_csv.assert_called_once()
    mock_zipfile.assert_called_once()