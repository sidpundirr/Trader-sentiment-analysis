import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

# Set global aesthetic style
plt.style.use('dark_background')
plt.rcParams['font.sans-serif'] = 'Helvetica, Arial, DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#444444'
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['grid.color'] = '#333333'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.5

PALETTE = ['#00E676', '#29B6F6', '#AB47BC', '#FF7043', '#FFD54F']

def generate_all_charts(df, fg, acc_stats, regime_res, asset_res, cohort_res, backtest_res, df_bt, output_dir='output/charts'):
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Sentiment Distribution & Time Series
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Time Series
    fg_sorted = fg.sort_values('date')
    fg_sorted['date_dt'] = pd.to_datetime(fg_sorted['date'])
    ax1.plot(fg_sorted['date_dt'], fg_sorted['sentiment_value'], color='#29B6F6', alpha=0.8, linewidth=1.5)
    ax1.axhline(25, color='#FF5252', linestyle=':', label='Extreme Fear (<=24)')
    ax1.axhline(45, color='#FF7043', linestyle=':', label='Fear (25-44)')
    ax1.axhline(55, color='#FFD54F', linestyle=':', label='Neutral (45-55)')
    ax1.axhline(75, color='#00E676', linestyle=':', label='Greed (56-75)')
    ax1.set_title('Bitcoin Fear & Greed Index Over Time (2023 - 2025)', fontsize=14, pad=12, fontweight='bold')
    ax1.set_ylabel('Sentiment Score (0 - 100)')
    ax1.legend(loc='upper right', framealpha=0.3)
    ax1.grid(True)
    
    # Regime Distribution Pie Chart
    regime_counts = fg['sentiment_regime_clean'].value_counts().reindex(['Extreme Fear', 'Fear', 'Neutral', 'Greed', 'Extreme Greed']).fillna(0)
    colors = ['#FF5252', '#FF7043', '#FFD54F', '#00E676', '#00B0FF']
    ax2.pie(regime_counts, labels=regime_counts.index, autopct='%1.1f%%', colors=colors, startangle=140, explode=[0.05]*5, textprops={'fontsize': 11})
    ax2.set_title('Market Days Proportion by Sentiment Regime', fontsize=14, pad=12, fontweight='bold')
    
    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, '01_sentiment_distribution.png'), dpi=300)
    plt.close(fig)
    print("Saved 01_sentiment_distribution.png")

    # 2. PnL by Sentiment Regime
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    regimes = regime_res['Sentiment Regime']
    tot_pnl_m = regime_res['Total Net PnL ($)'] / 1e6
    avg_pnl = regime_res['Avg Net PnL/Trade ($)']
    
    bars1 = ax1.bar(regimes, tot_pnl_m, color=['#FF5252', '#FF7043', '#FFD54F', '#00E676', '#00B0FF'], edgecolor='white', alpha=0.85)
    ax1.set_title('Total Net Trader PnL by Sentiment Regime ($ Millions)', fontsize=14, pad=12, fontweight='bold')
    ax1.set_ylabel('Net PnL ($ Millions)')
    ax1.grid(True, axis='y')
    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 0.1, f"${yval:.2f}M", ha='center', va='bottom', fontweight='bold', color='white')
        
    bars2 = ax2.bar(regimes, avg_pnl, color=['#FF5252', '#FF7043', '#FFD54F', '#00E676', '#00B0FF'], edgecolor='white', alpha=0.85)
    ax2.set_title('Average Net PnL Per Trade by Sentiment Regime ($)', fontsize=14, pad=12, fontweight='bold')
    ax2.set_ylabel('Avg Net PnL ($/trade)')
    ax2.grid(True, axis='y')
    for bar in bars2:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 2, f"${yval:.1f}", ha='center', va='bottom', fontweight='bold', color='white')

    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, '02_pnl_by_sentiment_regime.png'), dpi=300)
    plt.close(fig)
    print("Saved 02_pnl_by_sentiment_regime.png")

    # 3. Win Rate & Profit Factor by Regime
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax2 = ax1.twinx()
    
    x = np.arange(len(regimes))
    width = 0.35
    
    rects1 = ax1.bar(x - width/2, regime_res['Win Rate (%)'], width, label='Win Rate (%)', color='#29B6F6', alpha=0.85)
    rects2 = ax2.bar(x + width/2, regime_res['Profit Factor'], width, label='Profit Factor', color='#00E676', alpha=0.85)
    
    ax1.set_xlabel('Sentiment Regime', fontsize=12)
    ax1.set_ylabel('Win Rate (%)', color='#29B6F6', fontsize=12)
    ax2.set_ylabel('Profit Factor', color='#00E676', fontsize=12)
    ax1.set_xticks(x)
    ax1.set_xticklabels(regimes)
    ax1.set_title('Win Rate & Profit Factor Across Sentiment Regimes', fontsize=14, pad=12, fontweight='bold')
    ax1.grid(True, axis='y')
    
    # Legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, '03_winrate_profitfactor_by_regime.png'), dpi=300)
    plt.close(fig)
    print("Saved 03_winrate_profitfactor_by_regime.png")

    # 4. Asset Class Heatmap
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    piv_pnl = asset_res.pivot(index='Asset Class', columns='Sentiment Regime', values='Avg Net PnL ($)').reindex(columns=['Extreme Fear', 'Fear', 'Neutral', 'Greed', 'Extreme Greed'])
    piv_win = asset_res.pivot(index='Asset Class', columns='Sentiment Regime', values='Win Rate (%)').reindex(columns=['Extreme Fear', 'Fear', 'Neutral', 'Greed', 'Extreme Greed'])
    
    sns.heatmap(piv_pnl, annot=True, fmt=".1f", cmap="RdYlGn", center=0, ax=ax1, cbar_kws={'label': 'Avg Net PnL ($)'})
    ax1.set_title('Average Net PnL ($/Trade) by Asset Class & Sentiment', fontsize=13, pad=10, fontweight='bold')
    
    sns.heatmap(piv_win, annot=True, fmt=".1f", cmap="Blues", ax=ax2, cbar_kws={'label': 'Win Rate (%)'})
    ax2.set_title('Win Rate (%) by Asset Class & Sentiment', fontsize=13, pad=10, fontweight='bold')

    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, '04_asset_class_sentiment_heatmaps.png'), dpi=300)
    plt.close(fig)
    print("Saved 04_asset_class_sentiment_heatmaps.png")

    # 5. Cumulative Strategy Backtest Curves
    fig, ax = plt.subplots(figsize=(14, 7))
    
    daily_pnl_baseline = df_bt.groupby('date')['PnL_Baseline'].sum().cumsum()
    daily_pnl_strat1 = df_bt.groupby('date')['PnL_Strat1'].sum().cumsum()
    daily_pnl_strat2 = df_bt.groupby('date')['PnL_Strat2'].sum().cumsum()
    daily_pnl_strat3 = df_bt.groupby('date')['PnL_Strat3'].sum().cumsum()
    
    dates_dt = pd.to_datetime(daily_pnl_baseline.index)
    
    ax.plot(dates_dt, daily_pnl_baseline / 1e6, label='Baseline Trader Execution', color='#888888', linestyle='--', linewidth=2)
    ax.plot(dates_dt, daily_pnl_strat1 / 1e6, label='Strategy 1: Extreme Greed Major Filter', color='#29B6F6', linewidth=2)
    ax.plot(dates_dt, daily_pnl_strat2 / 1e6, label='Strategy 2: Dynamic Sentiment Position Sizing (+$1.79M)', color='#00E676', linewidth=2.5)
    ax.plot(dates_dt, daily_pnl_strat3 / 1e6, label='Strategy 3: Contrarian Sentiment Filter', color='#FFD54F', linewidth=2)
    
    ax.set_title('Cumulative Trader Net PnL: Baseline vs Sentiment-Informed Strategies', fontsize=15, pad=14, fontweight='bold')
    ax.set_ylabel('Cumulative Net PnL ($ Millions)', fontsize=12)
    ax.set_xlabel('Date', fontsize=12)
    ax.legend(loc='upper left', framealpha=0.4, fontsize=11)
    ax.grid(True)
    
    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, '05_strategy_backtest_performance.png'), dpi=300)
    plt.close(fig)
    print("Saved 05_strategy_backtest_performance.png")

if __name__ == '__main__':
    from data_loader import load_and_preprocess_data
    from trader_cohorts import compute_trader_stats
    from eda_sentiment import analyze_sentiment_regimes, analyze_asset_class_sentiment, analyze_cohort_sentiment
    from strategy_backtest import run_strategy_backtest
    
    df, fg = load_and_preprocess_data()
    acc_stats = compute_trader_stats(df)
    regime_res = analyze_sentiment_regimes(df)
    asset_res = analyze_asset_class_sentiment(df)
    cohort_res = analyze_cohort_sentiment(df, acc_stats)
    backtest_res, df_bt = run_strategy_backtest(df)
    
    generate_all_charts(df, fg, acc_stats, regime_res, asset_res, cohort_res, backtest_res, df_bt)
