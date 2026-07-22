import pandas as pd
import numpy as np
import os

MEMECOINS = {
    'FARTCOIN', 'MELANIA', 'TRUMP', 'kPEPE', 'kBONK', 'DOGE', 'SHIB', 'WIF', 
    'POPCAT', 'MOG', 'PNUT', 'GOAT', 'PEPE', 'BONK', 'FLOKI', 'MEME', 'BOME', 
    'MEW', 'NEIRO', 'TURBO', 'BRETT', 'GIGA', 'SPX', 'MOODENG', 'CHILLGUY'
}

MAJORS = {'BTC', 'ETH', 'SOL'}

def get_asset_class(coin):
    if not isinstance(coin, str):
        return 'Other'
    coin_upper = coin.upper().split('/')[0].replace('@', '')
    if coin_upper in MAJORS:
        return 'Major (BTC/ETH/SOL)'
    for m in MEMECOINS:
        if m in coin_upper:
            return 'Memecoin'
    return 'Altcoin'

def load_and_preprocess_data(trader_path='data/historical_trader_data.csv', fg_path='data/fear_greed_index.csv'):
    print("Loading raw datasets...")
    trader_df = pd.read_csv(trader_path)
    fg_df = pd.read_csv(fg_path)
    
    # Preprocess Fear & Greed Data
    fg_df['date'] = pd.to_datetime(fg_df['date']).dt.strftime('%Y-%m-%d')
    fg_df = fg_df.rename(columns={
        'value': 'sentiment_value',
        'classification': 'sentiment_class'
    })
    # Clean classification whitespace
    fg_df['sentiment_class'] = fg_df['sentiment_class'].astype(str).str.strip()
    
    # Recategorize sentiment values into canonical 5 regimes
    def categorize_regime(val):
        if val <= 24:
            return '1_Extreme Fear'
        elif val <= 44:
            return '2_Fear'
        elif val <= 55:
            return '3_Neutral'
        elif val <= 75:
            return '4_Greed'
        else:
            return '5_Extreme Greed'
            
    fg_df['sentiment_regime'] = fg_df['sentiment_value'].apply(categorize_regime)
    fg_df['sentiment_regime_clean'] = fg_df['sentiment_regime'].apply(lambda x: x.split('_')[1])
    
    # Preprocess Trader Data
    # Timestamp is in milliseconds
    trader_df['dt_utc'] = pd.to_datetime(trader_df['Timestamp'], unit='ms', errors='coerce')
    trader_df['date'] = trader_df['dt_utc'].dt.strftime('%Y-%m-%d')
    
    # Financial metrics
    trader_df['Net_PnL'] = trader_df['Closed PnL'] - trader_df['Fee']
    trader_df['Asset_Class'] = trader_df['Coin'].apply(get_asset_class)
    
    # Direction & Side flags
    trader_df['Is_Long'] = trader_df['Direction'].astype(str).str.contains('Long|Buy', case=False, regex=True)
    trader_df['Is_Short'] = trader_df['Direction'].astype(str).str.contains('Short|Sell', case=False, regex=True)
    
    trader_df['Is_Open'] = trader_df['Direction'].astype(str).str.contains('Open|Buy', case=False, regex=True)
    trader_df['Is_Close'] = trader_df['Direction'].astype(str).str.contains('Close|Sell', case=False, regex=True)
    
    # Win/Loss flag for closing trades or trades with non-zero PnL
    trader_df['Is_Win'] = trader_df['Net_PnL'] > 0
    trader_df['Is_Loss'] = trader_df['Net_PnL'] < 0
    
    # Merge datasets on date
    merged_df = pd.merge(trader_df, fg_df[['date', 'sentiment_value', 'sentiment_class', 'sentiment_regime', 'sentiment_regime_clean']], on='date', how='inner')
    
    print(f"Merged dataset shape: {merged_df.shape}")
    print(f"Date range: {merged_df['date'].min()} to {merged_df['date'].max()}")
    
    return merged_df, fg_df

if __name__ == '__main__':
    df, fg = load_and_preprocess_data()
    print(df.head())
