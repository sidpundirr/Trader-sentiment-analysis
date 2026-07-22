import pandas as pd
import numpy as np

def analyze_sentiment_regimes(merged_df):
    regimes = ['Extreme Fear', 'Fear', 'Neutral', 'Greed', 'Extreme Greed']
    
    regime_stats = []
    
    for regime in regimes:
        sub = merged_df[merged_df['sentiment_regime_clean'] == regime]
        num_trades = len(sub)
        if num_trades == 0:
            continue
            
        tot_net_pnl = sub['Net_PnL'].sum()
        avg_net_pnl = sub['Net_PnL'].mean()
        median_net_pnl = sub['Net_PnL'].median()
        
        tot_closed_pnl = sub['Closed PnL'].sum()
        tot_fee = sub['Fee'].sum()
        
        tot_vol = sub['Size USD'].sum()
        avg_trade_size = sub['Size USD'].mean()
        
        # Win Rate on closing/P&L realized trades
        pnl_trades = sub[sub['Closed PnL'] != 0]
        num_closing = len(pnl_trades)
        wins = pnl_trades[pnl_trades['Net_PnL'] > 0]
        losses = pnl_trades[pnl_trades['Net_PnL'] < 0]
        
        win_rate = (len(wins) / num_closing * 100) if num_closing > 0 else 0.0
        
        gain_sum = wins['Net_PnL'].sum() if len(wins) > 0 else 0.0
        loss_sum = abs(losses['Net_PnL'].sum()) if len(losses) > 0 else 0.0
        profit_factor = (gain_sum / loss_sum) if loss_sum > 0 else (gain_sum if gain_sum > 0 else 1.0)
        
        # Directional bias
        long_trades = sub[sub['Is_Long']]
        short_trades = sub[sub['Is_Short']]
        pct_long = (len(long_trades) / (len(long_trades) + len(short_trades)) * 100) if (len(long_trades) + len(short_trades)) > 0 else 50.0
        
        regime_stats.append({
            'Sentiment Regime': regime,
            'Total Trades': num_trades,
            'Total Volume (USD)': tot_vol,
            'Total Net PnL ($)': tot_net_pnl,
            'Avg Net PnL/Trade ($)': avg_net_pnl,
            'Median Net PnL ($)': median_net_pnl,
            'Win Rate (%)': win_rate,
            'Profit Factor': profit_factor,
            'Avg Trade Size ($)': avg_trade_size,
            'Long Ratio (%)': pct_long,
            'Total Fees ($)': tot_fee
        })
        
    res_df = pd.DataFrame(regime_stats)
    return res_df

def analyze_asset_class_sentiment(merged_df):
    results = []
    for (asset, regime), sub in merged_df.groupby(['Asset_Class', 'sentiment_regime_clean']):
        pnl_trades = sub[sub['Closed PnL'] != 0]
        wins = pnl_trades[pnl_trades['Net_PnL'] > 0]
        win_rate = (len(wins) / len(pnl_trades) * 100) if len(pnl_trades) > 0 else 0.0
        
        long_trades = sub[sub['Is_Long']]
        short_trades = sub[sub['Is_Short']]
        pct_long = (len(long_trades) / (len(long_trades) + len(short_trades)) * 100) if (len(long_trades) + len(short_trades)) > 0 else 50.0
        
        results.append({
            'Asset Class': asset,
            'Sentiment Regime': regime,
            'Trades': len(sub),
            'Total Net PnL ($)': sub['Net_PnL'].sum(),
            'Avg Net PnL ($)': sub['Net_PnL'].mean(),
            'Win Rate (%)': win_rate,
            'Long Ratio (%)': pct_long,
            'Total Volume ($)': sub['Size USD'].sum()
        })
    return pd.DataFrame(results)

def analyze_cohort_sentiment(merged_df, trader_stats_df):
    merged_with_cohort = pd.merge(merged_df, trader_stats_df[['Account', 'Cohort']], on='Account', how='left')
    results = []
    for (cohort, regime), sub in merged_with_cohort.groupby(['Cohort', 'sentiment_regime_clean']):
        pnl_trades = sub[sub['Closed PnL'] != 0]
        wins = pnl_trades[pnl_trades['Net_PnL'] > 0]
        win_rate = (len(wins) / len(pnl_trades) * 100) if len(pnl_trades) > 0 else 0.0
        
        long_trades = sub[sub['Is_Long']]
        short_trades = sub[sub['Is_Short']]
        pct_long = (len(long_trades) / (len(long_trades) + len(short_trades)) * 100) if (len(long_trades) + len(short_trades)) > 0 else 50.0
        
        results.append({
            'Cohort': cohort,
            'Sentiment Regime': regime,
            'Trades': len(sub),
            'Total Net PnL ($)': sub['Net_PnL'].sum(),
            'Avg Net PnL ($)': sub['Net_PnL'].mean(),
            'Win Rate (%)': win_rate,
            'Long Ratio (%)': pct_long,
            'Avg Trade Size ($)': sub['Size USD'].mean()
        })
    return pd.DataFrame(results)

if __name__ == '__main__':
    from data_loader import load_and_preprocess_data
    from trader_cohorts import compute_trader_stats
    
    df, fg = load_and_preprocess_data()
    acc_stats = compute_trader_stats(df)
    
    print("=== OVERALL SENTIMENT REGIME ANALYSIS ===")
    regime_res = analyze_sentiment_regimes(df)
    print(regime_res.to_string())
    
    print("\n=== ASSET CLASS SENTIMENT ANALYSIS ===")
    asset_res = analyze_asset_class_sentiment(df)
    print(asset_res.head(15).to_string())
