import pandas as pd
import numpy as np

trader_df = pd.read_csv('data/historical_trader_data.csv')
fg_df = pd.read_csv('data/fear_greed_index.csv')

print("=== TRADER DATA SUMMARY ===")
print("Accounts:", trader_df['Account'].nunique())
print("Coins:", trader_df['Coin'].nunique())
print("Coin list sample:", trader_df['Coin'].value_counts().head(15).to_dict())

# Check timestamps
print("\nTimestamp IST sample:", trader_df['Timestamp IST'].head())
print("Timestamp raw sample:", trader_df['Timestamp'].head())

# Convert timestamps to datetime in trader_df
# Let's inspect raw Timestamp unit (ms or s)
min_ts = trader_df['Timestamp'].min()
max_ts = trader_df['Timestamp'].max()
print(f"Min raw Timestamp: {min_ts}, Max raw Timestamp: {max_ts}")

trader_df['datetime'] = pd.to_datetime(trader_df['Timestamp'], unit='ms', errors='coerce')
print("Trader Date range:", trader_df['datetime'].min(), "to", trader_df['datetime'].max())

fg_df['datetime'] = pd.to_datetime(fg_df['date'])
print("Fear & Greed Date range:", fg_df['datetime'].min(), "to", fg_df['datetime'].max())

# Check overlap range
overlap_start = max(trader_df['datetime'].min(), fg_df['datetime'].min())
overlap_end = min(trader_df['datetime'].max(), fg_df['datetime'].max())
print(f"Overlap date range: {overlap_start} to {overlap_end}")

print("\nSides:", trader_df['Side'].value_counts().to_dict())
print("Directions:", trader_df['Direction'].value_counts().to_dict())
print("Closed PnL stats:\n", trader_df['Closed PnL'].describe())
print("Size USD stats:\n", trader_df['Size USD'].describe())
