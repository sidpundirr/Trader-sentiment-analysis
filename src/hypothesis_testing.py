import pandas as pd
import numpy as np

def compute_f_statistic(groups):
    k = len(groups)
    n_total = sum(len(g) for g in groups)
    overall_mean = np.mean(np.concatenate(groups))
    
    ss_between = sum(len(g) * (np.mean(g) - overall_mean)**2 for g in groups)
    ss_within = sum(sum((x - np.mean(g))**2 for x in g) for g in groups)
    
    df_between = k - 1
    df_within = n_total - k
    
    ms_between = ss_between / df_between
    ms_within = ss_within / df_within
    
    f_stat = ms_between / ms_within
    return f_stat, df_between, df_within

def compute_welch_t(g1, g2):
    m1, m2 = np.mean(g1), np.mean(g2)
    v1, v2 = np.var(g1, ddof=1), np.var(g2, ddof=1)
    n1, n2 = len(g1), len(g2)
    
    se = np.sqrt(v1/n1 + v2/n2)
    t_stat = (m1 - m2) / se if se > 0 else 0.0
    
    # Welch–Satterthwaite degrees of freedom
    df = ((v1/n1 + v2/n2)**2) / ((v1/n1)**2 / (n1 - 1) + (v2/n2)**2 / (n2 - 1)) if se > 0 else 1.0
    return t_stat, df

def compute_chi2(contingency_table):
    obs = np.array(contingency_table)
    row_sums = obs.sum(axis=1)
    col_sums = obs.sum(axis=0)
    total = obs.sum()
    
    exp = np.outer(row_sums, col_sums) / total
    chi2_stat = np.sum((obs - exp)**2 / exp)
    dof = (obs.shape[0] - 1) * (obs.shape[1] - 1)
    return chi2_stat, dof

def test_regime_pnl_anova(df):
    """Test H1: Does Net PnL per trade differ significantly across sentiment regimes?"""
    regimes = ['Fear', 'Neutral', 'Greed', 'Extreme Greed']
    groups = [df[df['sentiment_regime_clean'] == r]['Net_PnL'].dropna().values for r in regimes if len(df[df['sentiment_regime_clean'] == r]) > 0]
    f_stat, df_b, df_w = compute_f_statistic(groups)
    return {
        'Test': 'ANOVA on Net PnL across Sentiment Regimes',
        'F-Statistic': f_stat,
        'df (between, within)': (df_b, df_w),
        'Significant (p < 0.001)': f_stat > 5.0 # Critical value for large N is ~3.8
    }

def test_extreme_greed_degradation(df):
    """Test H2: Is Net PnL significantly lower in Extreme Greed vs Greed?"""
    greed = df[df['sentiment_regime_clean'] == 'Greed']['Net_PnL'].dropna().values
    extreme_greed = df[df['sentiment_regime_clean'] == 'Extreme Greed']['Net_PnL'].dropna().values
    
    t_stat, df_val = compute_welch_t(greed, extreme_greed)
    
    return {
        'Test': 'Greed vs Extreme Greed PnL Comparison (Welch t-test)',
        'Greed Mean PnL ($)': np.mean(greed),
        'Extreme Greed Mean PnL ($)': np.mean(extreme_greed),
        'Welch t-statistic': t_stat,
        'Degrees of Freedom': df_val,
        'Significant (p < 0.001)': abs(t_stat) > 3.29
    }

def test_directional_chi2(df):
    """Test H3: Is trade direction (Long vs Short) dependent on Sentiment Regime?"""
    ct = pd.crosstab(df['sentiment_regime_clean'], df['Is_Long'])
    chi2_stat, dof = compute_chi2(ct)
    return {
        'Test': 'Chi-Square Test: Direction (Long/Short) vs Sentiment Regime',
        'Chi2-Statistic': chi2_stat,
        'Degrees of Freedom': dof,
        'Significant (p < 0.001)': chi2_stat > 18.47 # critical val for df=4 at 0.001 level
    }

def test_majors_vs_altcoins_extreme_greed(df):
    """Test H4: Do Majors perform significantly worse than Altcoins in Extreme Greed?"""
    ext_greed = df[df['sentiment_regime_clean'] == 'Extreme Greed']
    majors = ext_greed[ext_greed['Asset_Class'] == 'Major (BTC/ETH/SOL)']['Net_PnL'].dropna().values
    alts = ext_greed[ext_greed['Asset_Class'] == 'Altcoin']['Net_PnL'].dropna().values
    
    t_stat, df_val = compute_welch_t(alts, majors)
    
    return {
        'Test': 'Altcoins vs Majors PnL in Extreme Greed (Welch t-test)',
        'Altcoins Mean PnL ($)': np.mean(alts),
        'Majors Mean PnL ($)': np.mean(majors),
        't-statistic': t_stat,
        'Degrees of Freedom': df_val,
        'Significant (p < 0.001)': t_stat > 3.29
    }

def run_all_hypothesis_tests(df):
    results = [
        test_regime_pnl_anova(df),
        test_extreme_greed_degradation(df),
        test_directional_chi2(df),
        test_majors_vs_altcoins_extreme_greed(df)
    ]
    return pd.DataFrame(results)

if __name__ == '__main__':
    from data_loader import load_and_preprocess_data
    df, fg = load_and_preprocess_data()
    hyp_df = run_all_hypothesis_tests(df)
    print("=== HYPOTHESIS TESTING RESULTS ===")
    for idx, row in hyp_df.iterrows():
        print(f"\n--- {row['Test']} ---")
        for k, v in row.items():
            if k != 'Test':
                print(f"  {k}: {v}")
