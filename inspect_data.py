import pandas as pd
import numpy as np

print("=== FEAR AND GREED INDEX DATASET ===")
fg_df = pd.read_csv('data/fear_greed_index.csv')
print("Shape:", fg_df.shape)
print("Columns:", fg_df.columns.tolist())
print("\nHead:\n", fg_df.head())
print("\nInfo:")
fg_df.info()

print("\n=== HISTORICAL TRADER DATASET ===")
trader_df = pd.read_csv('data/historical_trader_data.csv')
print("Shape:", trader_df.shape)
print("Columns:", trader_df.columns.tolist())
print("\nHead:\n", trader_df.head())
print("\nInfo:")
trader_df.info()

print("\nUnique accounts count:", trader_df['account'].nunique() if 'account' in trader_df.columns else "N/A")
print("Unique symbols count:", trader_df['symbol'].nunique() if 'symbol' in trader_df.columns else "N/A")
if 'symbol' in trader_df.columns:
    print("Top symbols:", trader_df['symbol'].value_counts().head(10).to_dict())

