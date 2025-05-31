import unittest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from datetime import datetime
import sys
import os
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.extract import fetch_page_content, get_product, collect_all_products

class TestExtract(unittest.TestCase):

    def setUp(self):
        self.html = """
        <div class="collection-card">
            <h3 class="product-title">Cool T-shirt</h3>
            <div class="price-container">$25.99</div>
            <p>Rating: 4.5⭐</p>
            <p>3 Colors</p>
            <p>Size: M</p>
            <p>Gender: Unisex</p>
        </div>
        """
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.card = self.soup.select_one('.collection-card')

    def test_get_product_valid(self):
        product = get_product(self.card)
        self.assertEqual(product['Title'], "Cool T-shirt")
        self.assertEqual(product['Price'], "$25.99")
        self.assertEqual(product['Rating'], "4.5")
        self.assertEqual(product['Colors'], "3 Colors")
        self.assertEqual(product['Size'], "M")
        self.assertEqual(product['Gender'], "Unisex")
        self.assertIn("Timestamp", product)

    def test_get_product_missing_price(self):
        html_missing_price = """
        <div class="collection-card">
            <h3 class="product-title">No Price Shirt</h3>
        </div>
        """
        soup = BeautifulSoup(html_missing_price, 'html.parser')
        card = soup.select_one('.collection-card')
        product = get_product(card)
        self.assertEqual(product['Price'], "N/A")

    @patch('requests.get')
    def test_fetch_page_content_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><body><div class="collection-card"></div></body></html>'
        mock_get.return_value = mock_response

        soup = fetch_page_content(1)
        self.assertIsNotNone(soup)
        self.assertTrue(soup.find('div', class_='collection-card'))

    @patch('requests.get')
    def test_fetch_page_content_failure(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Failed")
        soup = fetch_page_content(1)
        self.assertIsNone(soup)

    @patch('utils.extract.fetch_page_content')
    @patch('time.sleep', return_value=None)
    def test_collect_all_products(self, mock_sleep, mock_fetch):

        html_page1 = """
        <div class="collection-card">
            <h3 class="product-title">Product 1</h3>
            <div class="price-container">$10</div>
            <p>Rating: 4.0⭐</p>
            <p>1 Colors</p>
            <p>Size: L</p>
            <p>Gender: Male</p>
        </div>
        """
        html_page2 = "<div>No products here</div>"

        soup_page1 = BeautifulSoup(html_page1, 'html.parser')
        soup_page2 = BeautifulSoup(html_page2, 'html.parser')

        mock_fetch.side_effect = [soup_page1, soup_page2]

        products = collect_all_products()

        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]['Title'], 'Product 1')

if __name__ == '__main__':
    unittest.main()
