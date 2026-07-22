import sys
import os
import pandas as pd
import numpy as np

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_loader import load_and_preprocess_data
from trader_cohorts import compute_trader_stats
from eda_sentiment import analyze_sentiment_regimes, analyze_asset_class_sentiment, analyze_cohort_sentiment
from hypothesis_testing import run_all_hypothesis_tests
from strategy_backtest import run_strategy_backtest

def main():
    print("==========================================================")
    print(" BITCOIN SENTIMENT VS HYPERLIQUID TRADER PERFORMANCE ANALYSIS ")
    print("==========================================================")
    
    # 1. Load Data
    df, fg = load_and_preprocess_data()
    
    # 2. Trader Account Stats & Cohorts
    acc_stats = compute_trader_stats(df)
    
    # 3. Sentiment EDA
    regime_res = analyze_sentiment_regimes(df)
    asset_res = analyze_asset_class_sentiment(df)
    cohort_res = analyze_cohort_sentiment(df, acc_stats)
    
    # 4. Hypothesis Testing
    hyp_res = run_all_hypothesis_tests(df)
    
    # 5. Backtesting Quantitative Strategies
    backtest_res, df_bt = run_strategy_backtest(df)
    
    # 6. Export Tables to CSV
    os.makedirs('output/tables', exist_ok=True)
    acc_stats.to_csv('output/tables/trader_account_stats.csv', index=False)
    regime_res.to_csv('output/tables/sentiment_regime_summary.csv', index=False)
    asset_res.to_csv('output/tables/asset_class_sentiment_summary.csv', index=False)
    cohort_res.to_csv('output/tables/cohort_sentiment_summary.csv', index=False)
    hyp_res.to_csv('output/tables/hypothesis_testing_results.csv', index=False)
    backtest_res.to_csv('output/tables/strategy_backtest_results.csv', index=False)
    print("\nSaved all tabular datasets to output/tables/")
    
    # 7. Generate Visualizations
    try:
        from visualizer import generate_all_charts
        generate_all_charts(df, fg, acc_stats, regime_res, asset_res, cohort_res, backtest_res, df_bt)
        print("Generated all charts in output/charts/")
    except Exception as e:
        print(f"Error generating charts: {e}")
        
    print("\n=== MASTER PIPELINE RUN COMPLETE ===")

if __name__ == '__main__':
    main()
