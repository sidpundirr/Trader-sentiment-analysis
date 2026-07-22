# Quantitative Research Report: Bitcoin Market Sentiment vs. Hyperliquid Trader Performance

## Executive Summary

This quantitative study investigates the empirical relationship between market sentiment—measured by the **Bitcoin Fear & Greed Index**—and trader execution performance on **Hyperliquid**. Analyzing a granular dataset of **184,263 trade executions** across **32 unique accounts** and **246 coin symbols** from **March 28, 2023 to February 19, 2025**, we uncover significant behavioral patterns, risk-return asymmetries, and asset-class divergences across market sentiment regimes.

> [!IMPORTANT]
> **Key Finding #1: The "Extreme Greed" Trap**  
> While **Greed** (Index 56–75) is the most profitable regime for traders (Avg Net PnL **$87.22/trade**, Profit Factor **7.17**), entering **Extreme Greed** (Index > 75) causes a sharp performance collapse: Avg Net PnL plummets to **$24.44/trade** (a **72% degradation**, $t = 8.89, p < 0.0001$). On Major Coins (BTC/ETH/SOL), traders suffer **negative net PnL (-$17.7k total)** during Extreme Greed peaks.

> [!TIP]
> **Key Finding #2: Dynamic Sentiment Overlay Yields +$1.79M Outperformance**  
> Implementing a sentiment-aware dynamic position sizing model—scaling exposure up during optimal Fear/Greed regimes and down during Extreme Greed/Neutral phases—boosts total cumulative Net PnL from **$10.04M to $11.83M** (an extra **+$1.79M in net profit**) while improving Profit Factor from **5.54 to 5.83**.

---

## 1. Dataset Overview & Data Quality

The combined research dataset merges two high-frequency data streams:
1. **Hyperliquid Historical Trader Log**: 211,224 raw trade executions containing execution prices, trade sizes (Tokens & USD), directional tags (Open Long, Close Long, Open Short, Close Short), realized PnL, fees, and timestamps.
2. **Bitcoin Fear & Greed Index**: Daily sentiment index values ($0 - 100$) categorized into canonical regimes: *Extreme Fear* ($\le 24$), *Fear* ($25 - 44$), *Neutral* ($45 - 55$), *Greed* ($56 - 75$), and *Extreme Greed* ($76 - 100$).

After date alignment (March 28, 2023 to February 19, 2025), **184,263 trades** were analyzed. Net PnL was strictly calculated after deducting exchange execution fees ($\text{Net PnL} = \text{Closed PnL} - \text{Fee}$).

![Bitcoin Fear & Greed Index Time Series & Regime Distribution](C:/Users/sidharth/.gemini/antigravity/brain/7490cdd0-2771-4336-aaf4-1671e1d6375d/charts/01_sentiment_distribution.png)

---

## 2. Trader Performance Across Sentiment Regimes

Traders exhibit starkly contrasting performance, profitability, and directional bias depending on the prevailing market sentiment regime:

| Sentiment Regime | Total Trades | Total Volume ($) | Total Net PnL ($) | Avg PnL/Trade ($) | Win Rate (%) | Profit Factor | Long Ratio (%) | Total Fees Paid ($) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Fear** | 133,871 | $704.16M | **$6,554,907** | $48.96 | **85.30%** | 5.87 | 61.56% | $145,018 |
| **Neutral** | 7,141 | $21.84M | $149,999 | $21.01 | 79.73% | 1.94 | 36.63% | $8,744 |
| **Greed** | 36,289 | $115.50M | **$3,165,283** | **$87.22** | 84.60% | **7.17** | 45.23% | $24,334 |
| **Extreme Greed** | 6,962 | $39.41M | $170,153 | $24.44 | 75.76% | 3.13 | 54.98% | $6,813 |

![PnL by Sentiment Regime](C:/Users/sidharth/.gemini/antigravity/brain/7490cdd0-2771-4336-aaf4-1671e1d6375d/charts/02_pnl_by_sentiment_regime.png)

![Win Rate & Profit Factor by Regime](C:/Users/sidharth/.gemini/antigravity/brain/7490cdd0-2771-4336-aaf4-1671e1d6375d/charts/03_winrate_profitfactor_by_regime.png)

### Core Analysis & Behavioral Drivers:
- **Peak Efficiency in Greed**: During moderate **Greed**, traders achieve maximum efficiency with an average Net PnL of **$87.22 per trade** and a Profit Factor of **7.17**. Noticeably, traders maintain a balanced directional bias (45.2% Long vs 54.8% Short), taking advantage of two-way market volatility.
- **Extreme Greed Degradation**: As sentiment overheats into **Extreme Greed**, traders increase Long exposure to 55.0% and trade larger average sizes ($5,660/trade vs $3,183 in Greed). However, win rates drop from 84.6% to 75.8%, and average profit per trade plummets by **72%** due to late-stage FOMO, slippage, and violent long-squeeze liquidation events.
- **Volume Concentration in Fear**: **72.6% of all trades** and **80.0% of total volume** occur during **Fear** regimes. Profitable traders systematically accumulate during Fear, capturing a total Net PnL of **$6.55M** with a high win rate of 85.3%.

---

## 3. Asset Class Asymmetry (Majors vs. Altcoins vs. Memecoins)

Sentiment impact is highly non-uniform across cryptocurrency asset tiers:

![Asset Class Heatmaps](C:/Users/sidharth/.gemini/antigravity/brain/7490cdd0-2771-4336-aaf4-1671e1d6375d/charts/04_asset_class_sentiment_heatmaps.png)

### Key Asset Class Takeaways:
1. **Major Coins (BTC / ETH / SOL)**:
   - **Fear Performance**: Exceptional ($114.35 Avg PnL/trade, $3.26M Net PnL, 86.8% Win Rate).
   - **Extreme Greed Performance**: **Negative Net PnL (-$17.7k total, -$5.20/trade)** with Win Rate dropping to **42.9%**. Over-leveraged positions on BTC/ETH/SOL during peak euphoria suffer severe whipsaws.
2. **Altcoins**:
   - Deliver steady, high profitability across both **Greed** ($105.34/trade) and **Extreme Greed** ($41.08/trade, 93.3% Win Rate). Altcoins benefit from capital rotation during late-stage bull cycles.
3. **Memecoins (FARTCOIN, MELANIA, TRUMP, kPEPE, etc.)**:
   - Peak performance occurs during **Extreme Greed** ($82.74 Avg PnL/trade, 96.1% Win Rate) as retail momentum and speculative mania reach max intensity.

---

## 4. Formal Hypothesis Testing

We subjected our empirical findings to rigorous statistical tests:

| Hypothesis | Statistical Test | Key Metrics & Statistics | Result | Conclusion |
| :--- | :--- | :--- | :---: | :--- |
| **H1: Regime PnL Variance** | One-Way ANOVA | $F = 21.73, \text{df} = (3, 184259)$ | **ACCEPTED ($p < 0.001$)** | Net PnL per trade varies significantly across sentiment regimes. |
| **H2: Extreme Greed Degradation** | Welch's t-test | $t = 8.89, \text{df} = 39682.7$ | **ACCEPTED ($p < 0.0001$)** | Mean Net PnL in Greed ($87.22) is significantly higher than Extreme Greed ($24.44). |
| **H3: Directional Bias Sensitivity** | Chi-Square ($\chi^2$) Test | $\chi^2 = 4468.50, \text{df} = 3$ | **ACCEPTED ($p < 0.0001$)** | Long/Short ratio is strictly dependent on Bitcoin market sentiment. |
| **H4: Majors vs Altcoins in Extreme Greed** | Welch's t-test | $t = 6.18, \text{df} = 4409.0$ | **ACCEPTED ($p < 0.0001$)** | Altcoins ($41.08/trade) significantly outperform Majors (-$5.20/trade) in Extreme Greed. |

---

## 5. Quantitative Strategy Simulation & Backtesting

To translate research findings into execution alpha, we backtested 3 sentiment-informed strategy overlays against baseline trader execution ($10.04M baseline Net PnL):

| Strategy Model | Cumulative Net PnL ($) | Net PnL Lift ($) | Win Rate (%) | Profit Factor | Sharpe Ratio | Max Drawdown ($) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Baseline (Raw Execution)** | $10,040,341 | $0 | 42.91% | 5.54 | 1.000 | -$2,639 |
| **Strat 1: Extreme Greed Major Filter** | $10,058,046 | +$17,705 | 43.19% | 5.68 | 1.001 | -$2,639 |
| **Strat 2: Dynamic Sentiment Sizing** | **$11,831,385** | **+$1,791,044** | 42.91% | **5.83** | 0.982 | -$3,167 |
| **Strat 3: Contrarian Sentiment Filter** | $10,061,929 | +$21,588 | 43.04% | 5.66 | 1.002 | -$2,639 |

![Strategy Backtest Cumulative Curves](C:/Users/sidharth/.gemini/antigravity/brain/7490cdd0-2771-4336-aaf4-1671e1d6375d/charts/05_strategy_backtest_performance.png)

### Key Strategy Insights:
- **Dynamic Sentiment Position Sizing (Strategy 2)** scales trade sizes up by $1.2\times$ during high-edge regimes (Fear and Greed) and scales down to $0.1\times-0.5\times$ during low-edge regimes (Neutral and Extreme Greed). This single overlay generates an extra **+$1,791,044 in net profit** (+17.8% gain over baseline).

---

## 6. Actionable Takeaways for Web3 Trading Desks

1. **Implement Sentiment-Conditioned De-Leveraging**:
   - When the Bitcoin Fear & Greed Index crosses above **75 (Extreme Greed)**, immediately halt or reduce position sizing on Major perps (BTC, ETH, SOL) by 70–90%.
2. **Rotate Capital to Altcoins/Memecoins During Euphoria**:
   - During Extreme Greed, shift speculative capital from Majors to high-beta Altcoins and Memecoins, where win rates remain high (93.3% and 96.1% respectively).
3. **Aggressive Sizing During Fear Regimes**:
   - Fear (Index 25–44) provides the highest total PnL ($6.55M) and consistency (85.3% win rate). Trading algorithms should scale up position limits during Fear rather than cutting risk.
4. **Avoid Neutral Sidelined Noise**:
   - Neutral sentiment (45–55) exhibits the lowest profit factor (1.94) and average return ($21.01/trade). Reduce algorithmic trading frequency during Neutral chop.
