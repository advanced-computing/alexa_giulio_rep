import unittest
from unittest.mock import patch, MagicMock
import Spotify_Data_Load

class TestBigQueryFallback(unittest.TestCase):

    @patch("Spotify_Data_Load.pandas_gbq.read_gbq")
    @patch("Spotify_Data_Load.update_bigquery_from_kaggle", return_value=None)
    def test_bigquery_fallback_used(self, mock_etl, mock_read_gbq):
        mock_df = MagicMock()
        mock_df.__getitem__.return_value = ['2025-04-19']
        mock_read_gbq.return_value = mock_df
        
        if Spotify_Data_Load.update_bigquery_from_kaggle() is None:
            latest_date_query = f"SELECT MAX(snapshot_date) AS latest_date FROM `{Spotify_Data_Load.table_ref}`"
            latest_date_df = mock_read_gbq(latest_date_query, project_id=Spotify_Data_Load.project_id, credentials=Spotify_Data_Load.credentials)
            latest_snapshot = latest_date_df['latest_date'][0]

        self.assertEqual(latest_snapshot, '2025-04-19')
        mock_read_gbq.assert_called_once()

if __name__ == "__main__":
    unittest.main()
