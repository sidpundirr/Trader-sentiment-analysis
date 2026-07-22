import pandas as pd
import numpy as np

def compute_trader_stats(df):
    account_stats = []
    for account, grp in df.groupby('Account'):
        total_closed_pnl = grp['Closed PnL'].sum()
        total_fee = grp['Fee'].sum()
        total_net_pnl = grp['Net_PnL'].sum()
        total_vol = grp['Size USD'].sum()
        num_trades = len(grp)
        
        closing_trades = grp[grp['Closed PnL'] != 0]
        num_closing = len(closing_trades)
        wins = closing_trades[closing_trades['Net_PnL'] > 0]
        losses = closing_trades[closing_trades['Net_PnL'] < 0]
        
        win_rate = len(wins) / num_closing if num_closing > 0 else 0.0
        
        total_gain = wins['Net_PnL'].sum() if len(wins) > 0 else 0.0
        total_loss = abs(losses['Net_PnL'].sum()) if len(losses) > 0 else 0.0
        profit_factor = (total_gain / total_loss) if total_loss > 0 else (total_gain if total_gain > 0 else 1.0)
        
        avg_trade_size = grp['Size USD'].mean()
        
        # Daily Net PnL volatility for Sharpe calculation
        daily_pnl = grp.groupby('date')['Net_PnL'].sum()
        mean_daily = daily_pnl.mean()
        std_daily = daily_pnl.std()
        sharpe = (mean_daily / std_daily * np.sqrt(365)) if (std_daily > 0 and not np.isnan(std_daily)) else 0.0
        
        account_stats.append({
            'Account': account,
            'Short_Account': account[:6] + '...' + account[-4:],
            'Total_Net_PnL': total_net_pnl,
            'Total_Closed_PnL': total_closed_pnl,
            'Total_Fee': total_fee,
            'Total_Volume_USD': total_vol,
            'Num_Trades': num_trades,
            'Num_Closing_Trades': num_closing,
            'Win_Rate': win_rate,
            'Profit_Factor': profit_factor,
            'Avg_Trade_Size_USD': avg_trade_size,
            'Sharpe_Ratio': sharpe
        })
        
    stats_df = pd.DataFrame(account_stats).sort_values(by='Total_Net_PnL', ascending=False)
    
    # Assign Cohorts: Top 25% (Smart Money/Whales), Bottom 25% (Retail/Unprofitable), Middle 50% (Mid/Scalpers)
    # Or based on Net PnL thresholds
    def assign_cohort(row):
        if row['Total_Net_PnL'] > 10000:
            return 'Smart Money (Top Traders)'
        elif row['Total_Net_PnL'] < -10000:
            return 'Retail / Unprofitable'
        else:
            return 'Mid-Tier / Scalpers'
            
    stats_df['Cohort'] = stats_df.apply(assign_cohort, axis=1)
    return stats_df

if __name__ == '__main__':
    from data_loader import load_and_preprocess_data
    df, fg = load_and_preprocess_data()
    acc_stats = compute_trader_stats(df)
    print("=== TRADER ACCOUNT STATS ===")
    print(acc_stats[['Short_Account', 'Total_Net_PnL', 'Total_Fee', 'Num_Trades', 'Win_Rate', 'Profit_Factor', 'Cohort']])
    print("\nCohort distribution:")
    print(acc_stats['Cohort'].value_counts())
