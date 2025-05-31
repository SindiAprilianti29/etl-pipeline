import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import re

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
HEADERS = {'User-Agent': USER_AGENT}
ROOT_URL = 'https://fashion-studio.dicoding.dev/'

def fetch_page_content(page_number):
    url = ROOT_URL if page_number == 1 else f"{ROOT_URL}page{page_number}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Gagal scraping page {page_number}: {e}")
        return None

def get_product(card):
    try:
        name = card.select_one('.product-title').get_text(strip=True)
        price_block = card.select_one('.price-container')
        price = price_block.get_text(strip=True) if price_block else "N/A"

        data = {
            'Title': name,
            'Price': price,
            'Rating': 'N/A',
            'Colors': 'N/A',
            'Size': 'N/A',
            'Gender': 'N/A',
            'Timestamp': datetime.now().isoformat()
        }

        for p in card.find_all('p'):
            text = p.get_text(strip=True)

            if 'Rating:' in text:
                data['Rating'] = text.replace('Rating:', '').replace('⭐', '').strip()
            elif re.search(r'\d+\s*Colors$', text):
                match = re.search(r'(\d+\s*Colors)', text)
                data['Colors'] = match.group(1) if match else 'N/A'
            elif 'Size:' in text:
                data['Size'] = text.replace('Size:', '').strip()
            elif 'Gender:' in text:
                data['Gender'] = text.replace('Gender:', '').strip()

        return data

    except Exception as e:
        print(f"Error extracting product data: {e}")
        return None

def collect_all_products():
    all_items = []
    page = 1

    while True:
        print(f"Scraping page {page}")
        soup = fetch_page_content(page)

        if not soup:
            break

        product_cards = soup.select('.collection-card')
        if not product_cards:
            print(f"page {page} tidak berisi produk")
            break

        for card in product_cards:
            product_data = get_product(card)
            if product_data:
                all_items.append(product_data)

        page += 1
        time.sleep(1.5)

    return all_items