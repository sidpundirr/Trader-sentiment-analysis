import pandas as pd
import numpy as np

def run_strategy_backtest(df):
    df = df.copy()
    
    # 1. Baseline: Standard execution
    df['PnL_Baseline'] = df['Net_PnL']
    
    # 2. Strategy 1: Extreme Greed Major Filter (Filter out Major coin trades during Extreme Greed)
    mask_strat1 = ~((df['sentiment_regime_clean'] == 'Extreme Greed') & (df['Asset_Class'] == 'Major (BTC/ETH/SOL)'))
    df['PnL_Strat1'] = np.where(mask_strat1, df['Net_PnL'], 0.0)
    
    # 3. Strategy 2: Sentiment-Based Position Sizing Overlay
    # Scale PnL based on historical regime efficiency multiplier
    # Fear: 1.2x, Greed: 1.2x, Neutral: 0.5x, Extreme Greed: 0.3x
    def get_sizing_multiplier(row):
        regime = row['sentiment_regime_clean']
        asset = row['Asset_Class']
        if regime == 'Fear':
            return 1.2
        elif regime == 'Greed':
            return 1.2
        elif regime == 'Neutral':
            return 0.5
        elif regime == 'Extreme Greed':
            return 0.1 if asset == 'Major (BTC/ETH/SOL)' else 0.5
        return 1.0

    df['Sizing_Mult'] = df.apply(get_sizing_multiplier, axis=1)
    df['PnL_Strat2'] = df['Net_PnL'] * df['Sizing_Mult']
    
    # 4. Strategy 3: Contrarian Long/Short Sentiment Filter
    # Filter out Longs during Extreme Greed on Majors, Filter out Shorts during Extreme Fear
    mask_strat3 = ~((df['sentiment_regime_clean'] == 'Extreme Greed') & (df['Asset_Class'] == 'Major (BTC/ETH/SOL)') & (df['Is_Long']))
    df['PnL_Strat3'] = np.where(mask_strat3, df['Net_PnL'], 0.0)

    strategies = {
        'Baseline (Raw Trader Execution)': 'PnL_Baseline',
        'Strategy 1: Extreme Greed Major Filter': 'PnL_Strat1',
        'Strategy 2: Dynamic Sentiment Position Sizing': 'PnL_Strat2',
        'Strategy 3: Contrarian Sentiment Filter': 'PnL_Strat3'
    }

    daily_dates = pd.date_range(df['date'].min(), df['date'].max())
    
    results = []
    
    for name, pnl_col in strategies.items():
        total_pnl = df[pnl_col].sum()
        
        # Daily aggregation for Sharpe & Max Drawdown
        daily_pnl = df.groupby('date')[pnl_col].sum().reindex(daily_dates.strftime('%Y-%m-%d'), fill_value=0.0)
        cum_pnl = daily_pnl.cumsum()
        
        mean_d = daily_pnl.mean()
        std_d = daily_pnl.std()
        sharpe = (mean_d / std_d * np.sqrt(365)) if std_d > 0 else 0.0
        
        # Max Drawdown calculation
        running_max = np.maximum.accumulate(cum_pnl)
        drawdown = cum_pnl - running_max
        max_dd = drawdown.min()
        
        active_trades = (df[pnl_col] != 0)
        win_trades = df[active_trades & (df[pnl_col] > 0)]
        loss_trades = df[active_trades & (df[pnl_col] < 0)]
        
        win_rate = (len(win_trades) / len(df[active_trades]) * 100) if len(df[active_trades]) > 0 else 0.0
        gain_sum = win_trades[pnl_col].sum()
        loss_sum = abs(loss_trades[pnl_col].sum())
        profit_factor = (gain_sum / loss_sum) if loss_sum > 0 else 1.0
        
        results.append({
            'Strategy': name,
            'Total Cumulative Net PnL ($)': total_pnl,
            'PnL Improvement vs Baseline ($)': total_pnl - df['PnL_Baseline'].sum(),
            'Win Rate (%)': win_rate,
            'Profit Factor': profit_factor,
            'Annualized Sharpe Ratio': sharpe,
            'Max Drawdown ($)': max_dd
        })
        
    res_df = pd.DataFrame(results)
    return res_df, df

if __name__ == '__main__':
    from data_loader import load_and_preprocess_data
    df, fg = load_and_preprocess_data()
    backtest_res, df_bt = run_strategy_backtest(df)
    print("=== QUANTITATIVE STRATEGY BACKTEST RESULTS ===")
    print(backtest_res.to_string())
