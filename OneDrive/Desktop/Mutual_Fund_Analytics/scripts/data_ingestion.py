import pandas as pd
import os

folder_path = "../data/raw"

files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

for file in files:

    print("\n" + "="*70)
    print(f"Dataset: {file}")

    df = pd.read_csv(os.path.join(folder_path, file))

    print(f"\nShape: {df.shape}")

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    print(df.isnull().sum())

    duplicate_count = df.duplicated().sum()

    print("\nDuplicate Rows:")
    print(duplicate_count)

    print("\nFirst 5 Rows:")
    print(df.head())



    print("\nANOMALY CHECK")

    anomalies = []


    missing_values = df.isnull().sum().sum()
    if missing_values > 0:
        anomalies.append(
            f"Missing Values Found: {missing_values}"
        )

    
    if duplicate_count > 0:
        anomalies.append(
            f"Duplicate Rows Found: {duplicate_count}"
        )

   
    object_cols = df.select_dtypes(include="object").columns

    for col in object_cols:
        if "date" in col.lower():
            anomalies.append(
                f"Date column '{col}' stored as Object datatype"
            )

  
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

    for col in numeric_cols:
        negative_count = (df[col] < 0).sum()

        if negative_count > 0:
            anomalies.append(
                f"{negative_count} negative values found in '{col}'"
            )

    
    if anomalies:
        print("\nAnomalies Found:")
        for a in anomalies:
            print("-", a)
    else:
        print("\nNo anomalies detected.")