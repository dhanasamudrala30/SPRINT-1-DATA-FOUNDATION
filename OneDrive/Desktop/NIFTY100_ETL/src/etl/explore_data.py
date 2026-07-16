from pathlib import Path
import pandas as pd

RAW_PATH = Path("data/raw")

for file in RAW_PATH.glob("*.xlsx"):

    print("=" * 80)
    print("FILE :", file.name)

    # Show sheet names
    excel = pd.ExcelFile(file)
    print("Sheets :", excel.sheet_names)

    # Read normally
    df = pd.read_excel(file)

    print("Shape :", df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 5 Rows:")
    print(df.head())

    print("\n")