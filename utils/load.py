import pandas as pd
import os

def save_to_csv(df: pd.DataFrame, filename="products.csv"):
    if df.empty:
        print("Data kosong!")
        return False  # Mengembalikan False jika data kosong
    else:
        try:
            file_path = os.path.join(os.getcwd(), filename)  # Menyimpan di direktori kerja saat ini
            df.to_csv(file_path, index=False)
            print(f"[CSV] Data berhasil disimpan ke {file_path}")
            return True  # Mengembalikan True jika penyimpanan berhasil
        except Exception as e:
            print(f"Terjadi kesalahan saat menyimpan ke CSV: {e}")
            return False  # Mengembalikan False jika ada kesalahan saat menyimpan
