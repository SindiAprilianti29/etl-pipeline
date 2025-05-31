import pandas as pd

nilai_tukar = 16000

def process_data(raw_data):
    try:
        df = pd.DataFrame(raw_data).copy()
        if df.empty:
            print("Dataframe kosong")
            return df

        required_cols = ["Price", "Rating", "Colors", "Title"]
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            print(f"Kolom yang hilang: {', '.join(missing_cols)}")

        df["Price"] = df["Price"].str.replace(r'[^0-9.]', '', regex=True)
        df["Price"] = pd.to_numeric(df["Price"], errors='coerce') * nilai_tukar

        df["Rating"] = df["Rating"].astype(str).str.extract(r"([\d.]+)").astype(float)

        df["Colors"] = df["Colors"].astype(str).str.extract(r"(\d+)").astype(float).fillna(0).astype(int)

        df.dropna(subset=["Rating"], inplace=True)

        df.drop_duplicates(inplace=True)
        df.dropna(inplace=True)

        df = df[df["Title"].notnull() & (df["Title"] != "Unknown Product")]

        print(f"Jumlah data setelah transformasi: {len(df)}")
        return df

    except Exception as e:
        print(f"Terjadi error saat transformasi data: {e}")
        return pd.DataFrame()
