import numpy as np

# ---------------- CALCULATION ----------------------------
def weighted_average(df, values, weights):
    # return sum(df[weights] * df[values]) / df[weights].sum()
    average = np.average(df[values], weights=df[weights])
    # Fast and numerically precise:
    variance = np.average((df[values]-average)**2, weights=df[weights])
    return average, np.sqrt(variance)

def weighted_median(df, values, weights):
    df = df.sort_values(values)
    cumsum = df[weights].cumsum()
    cutoff = df[weights].sum() / 2.0
    median = df[values][cumsum >= cutoff].iloc[0]
    cutoff_quant = df[weights].sum() / 4.0 # 25 percentile
    lowquant = df[values][cumsum >= cutoff_quant].iloc[0]
    cutoff_quant = df[weights].sum() * 3.0 / 4.0 # 75 percentile
    highquant = df[values][cumsum >= cutoff_quant].iloc[0]
    return median, lowquant, highquant
