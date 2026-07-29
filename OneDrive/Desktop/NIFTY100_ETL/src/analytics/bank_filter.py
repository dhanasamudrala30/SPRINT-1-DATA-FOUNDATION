import pandas as pd
from pathlib import Path



PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "processed"
OUTPUT_PATH = PROJECT_ROOT / "output"

OUTPUT_PATH.mkdir(exist_ok=True)



sectors = pd.read_csv(DATA_PATH / "sectors.csv")



banks = sectors[
    sectors["sub_sector"].str.contains(
        "Bank",
        case=False,
        na=False
    )
].copy()

banks["is_bank"] = True



non_banks = sectors[
    ~sectors["company_id"].isin(banks["company_id"])
].copy()

non_banks["is_bank"] = False



banks.to_csv(
    OUTPUT_PATH / "bank_companies.csv",
    index=False
)

non_banks.to_csv(
    OUTPUT_PATH / "non_bank_companies.csv",
    index=False
)


print("Bank Companies :", len(banks))
print("Non-Bank Companies :", len(non_banks))


print("\nSample Bank Companies\n")
print(banks.head())

company_flags = pd.concat(
    [
        banks[["company_id", "is_bank"]],
        non_banks[["company_id", "is_bank"]]
    ],
    ignore_index=True
)

company_flags.to_csv(
    OUTPUT_PATH / "company_flags.csv",
    index=False
)

print("\ncompany_flags.csv generated successfully!")