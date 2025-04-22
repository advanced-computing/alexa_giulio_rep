import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # noqa: E402
import spotifydataload

import pytest
from unittest.mock import patch, MagicMock
import spotifydataload

@patch("spotifydataload.KaggleApi")
@patch("spotifydataload.storage.Client")
@patch("spotifydataload.bigquery.Client")
@patch("spotifydataload.pd.read_csv")
@patch("spotifydataload.zipfile.ZipFile")
def test_update_bigquery_from_kaggle(
    mock_zip, mock_read_csv, mock_bigquery_client, mock_storage_client, mock_kaggle_api
):
    # Mock Kaggle API
    mock_kaggle = MagicMock()
    mock_kaggle.dataset_download_files.return_value = None
    mock_kaggle_api.return_value = mock_kaggle

    # Mock reading CSV
    df_mock = MagicMock()
    df_mock['snapshot_date'].max.return_value = "2024-12-31"
    df_mock.__getitem__.return_value = df_mock
    mock_read_csv.return_value = df_mock

    # Mock BigQuery & GCS clients
    mock_storage = MagicMock()
    mock_storage.bucket.return_value.blob.return_value.upload_from_filename.return_value = None
    mock_storage_client.return_value = mock_storage

    mock_bq = MagicMock()
    mock_bq.load_table_from_uri.return_value.result.return_value = None
    mock_bigquery_client.return_value = mock_bq

    # Run
    result = spotifydataload.update_bigquery_from_kaggle()
    
    assert result == "2024-12-31"

class TestBigQueryFallback(unittest.TestCase):

    @patch("spotifydataload.pandas_gbq.read_gbq")
    @patch("spotifydataload.update_bigquery_from_kaggle", return_value=None)
    def test_bigquery_fallback_used(self, mock_etl, mock_read_gbq):
        mock_df = MagicMock()
        mock_df.__getitem__.return_value = ['2025-04-19']
        mock_read_gbq.return_value = mock_df
        
        if spotifydataload.update_bigquery_from_kaggle() is None:
            latest_date_query = f"SELECT MAX(snapshot_date) AS latest_date FROM `{spotifydataload.table_ref}`"
            latest_date_df = mock_read_gbq(latest_date_query, project_id=spotifydataload.project_id, credentials=spotifydataload.credentials)
            latest_snapshot = latest_date_df['latest_date'][0]

        self.assertEqual(latest_snapshot, '2025-04-19')
        mock_read_gbq.assert_called_once()

if __name__ == "__main__":
    unittest.main()
