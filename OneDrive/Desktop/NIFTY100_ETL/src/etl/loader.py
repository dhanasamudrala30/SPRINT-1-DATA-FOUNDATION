from pathlib import Path
import pandas as pd
try:
    from .normaliser import normalize_year, normalize_ticker
except ImportError:
    from normaliser import normalize_year, normalize_ticker


RAW_PATH = Path("data/raw")
OUTPUT_PATH = Path("data/processed")

HEADER_ONE_FILES = {
    "analysis.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "companies.xlsx",
    "documents.xlsx",
    "profitandloss.xlsx",
    "prosandcons.xlsx"
}


def load_excel(file_path):
    """
    Load Excel file with the correct header.
    """
    if file_path.name in HEADER_ONE_FILES:
        return pd.read_excel(file_path, header=1)
    else:
        return pd.read_excel(file_path)



datasets = {}


for file in RAW_PATH.glob("*.xlsx"):

    df = load_excel(file)

  
    for column in df.columns:
        if column.lower() == "year":
            df[column] = df[column].apply(normalize_year)

    if "company_id" in df.columns:
        df["company_id"] = df["company_id"].apply(normalize_ticker)

    datasets[file.stem] = df


print("=" * 80)
print("Datasets Loaded Successfully")
print("=" * 80)

for name, df in datasets.items():

    print(f"\n{name}")
    print("-" * 50)
    print("Shape :", df.shape)
    print("Columns :", list(df.columns))


print("\nChecking Normalized Data\n")

for name, df in datasets.items():

    print("=" * 60)
    print(name)

    if "company_id" in df.columns:

        cols = ["company_id"]

        for c in df.columns:
            if c.lower() == "year":
                cols.append(c)

        print(df[cols].head())

    else:
        print(df.head())



OUTPUT_PATH.mkdir(parents=True, exist_ok=True)


for name, df in datasets.items():

    output_file = OUTPUT_PATH / f"{name}.csv"

    df.to_csv(output_file, index=False)

    print(f"Saved -> {output_file}")


print("\n All cleaned datasets saved successfully!")