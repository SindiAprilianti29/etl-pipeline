import unittest
import pandas as pd
import os
import tempfile
from utils.load import save_to_csv

class TestSaveToCSV(unittest.TestCase):

    def test_save_successful(self):
        df = pd.DataFrame({
            "Title": ["Produk A", "Produk B"],
            "Price": [1600000, 3200000],
            "Rating": [4.5, 4.0],
            "Colors": [3, 5]
        })

        with tempfile.TemporaryDirectory() as tmpdirname:
            file_path = os.path.join(tmpdirname, "test_products.csv")
            result = save_to_csv(df, filename=file_path)
            self.assertTrue(result)
            self.assertTrue(os.path.exists(file_path))
            saved_df = pd.read_csv(file_path)
            pd.testing.assert_frame_equal(df, saved_df)

    def test_save_empty_dataframe(self):
        empty_df = pd.DataFrame()
        result = save_to_csv(empty_df, filename="should_not_create.csv")
        self.assertFalse(result)
        self.assertFalse(os.path.exists(os.path.join(os.getcwd(), "should_not_create.csv")))

    def test_save_raises_exception(self):
        df = pd.DataFrame({
            "Title": ["Produk C"],
            "Price": [10000],
            "Rating": [5.0],
            "Colors": [2]
        })

        invalid_path = "Z:/invalid_folder/test.csv" if os.name == 'nt' else "/invalid_folder/test.csv"
        result = save_to_csv(df, filename=invalid_path)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
