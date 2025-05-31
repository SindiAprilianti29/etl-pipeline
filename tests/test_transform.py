import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
from utils.transform import process_data

class TestProcessData(unittest.TestCase):

    def test_valid_data(self):
        raw_data = [
            {"Price": "$100.00", "Rating": "4.5 / 5", "Colors": "3 Colors", "Title": "Product A"},
            {"Price": "$200.00", "Rating": "4.0 / 5", "Colors": "5 Colors", "Title": "Product B"}
        ]
        expected_data = pd.DataFrame({
            "Price": [1600000.0, 3200000.0],
            "Rating": [4.5, 4.0],
            "Colors": [3, 5],
            "Title": ["Product A", "Product B"]
        })
        result = process_data(raw_data).reset_index(drop=True)
        assert_frame_equal(result, expected_data)

    def test_missing_columns(self):
        raw_data = [{"Price": "$100.00", "Title": "Product A"}]
        result = process_data(raw_data)
        self.assertIsInstance(result, pd.DataFrame)

    def test_empty_dataframe(self):
        result = process_data([])
        self.assertTrue(result.empty)

    def test_invalid_rating(self):
        raw_data = [{"Price": "$50.00", "Rating": "invalid", "Colors": "2 Colors", "Title": "Product C"}]
        result = process_data(raw_data)
        self.assertTrue(result.empty)

    def test_unknown_product_title(self):
        raw_data = [{"Price": "$10.00", "Rating": "3.0 / 5", "Colors": "1 Colors", "Title": "Unknown Product"}]
        result = process_data(raw_data)
        self.assertTrue(result.empty)

if __name__ == '__main__':
    unittest.main()
