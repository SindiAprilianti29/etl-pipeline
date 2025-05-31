from utils.extract import collect_all_products
from utils.transform import process_data
from utils.load import save_to_csv

def main():
    all_products = collect_all_products()
    print(f"Jumlah data hasil scraping: {len(all_products)}")

    print("Memulai proses transformasi data")
    df = process_data(all_products)

    if df.empty:
        print("Data kosong setelah proses transformasi")
    else:
        print("Menyimpan data ke CSV")
        save_to_csv(df)

if __name__ == "__main__":
    main()
