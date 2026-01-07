import pandas as pd
from pathlib import Path

# --------------------------------------------------
# Locate data directory
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# --------------------------------------------------
# Read and combine all CSV files
# --------------------------------------------------

dataframes = []

for csv_file in DATA_DIR.glob("*.csv"):
    df = pd.read_csv(csv_file)
    dataframes.append(df)

if not dataframes:
    raise ValueError("No CSV files found in the data directory.")

df_all = pd.concat(dataframes, ignore_index=True)

# --------------------------------------------------
# Filter only Pink Morsel
# --------------------------------------------------

df_all["product"] = df_all["product"].str.strip().str.lower()
df_all = df_all[df_all["product"] == "pink morsel"]

# --------------------------------------------------
# Clean price column (remove $ and convert to float)
# --------------------------------------------------

df_all["price"] = (
    df_all["price"]
    .str.replace("$", "", regex=False)
    .astype(float)
)

# --------------------------------------------------
# Calculate sales
# --------------------------------------------------

df_all["Sales"] = df_all["quantity"] * df_all["price"]

# --------------------------------------------------
# Select and rename final columns
# --------------------------------------------------

final_df = df_all[["Sales", "date", "region"]].rename(
    columns={
        "date": "Date",
        "region": "Region"
    }
)

# --------------------------------------------------
# Output processed CSV
# --------------------------------------------------

output_file = BASE_DIR / "processed_sales.csv"
final_df.to_csv(output_file, index=False)

print(" Data processing complete")
print(f" Output file: {output_file}")
print(f" Rows generated: {len(final_df)}")
