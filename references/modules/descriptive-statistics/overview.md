# Descriptive statistics

Use for summarizing distributions, spread, percentiles, missingness, high-cardinality categories and candidate outliers. This module is descriptive; it does not perform hypothesis tests or establish causality.

## Input and script

The script accepts a bounded, already-fetched JSON list of row objects or `{"rows": [...]}`. It performs no network or database calls.

```bash
python scripts/descriptive-statistics/summarize.py --input /path/to/rows.json --column amount
```

Check missingness and parsing counts. Numeric strings can be parsed, but invalid values must be disclosed rather than silently imputed. No data is automatically deleted or winsorized.

## Choose statistics to match the shape

| Data pattern | Prefer | Avoid |
|---|---|---|
| Roughly symmetric numeric values | mean, standard deviation, n | mean without spread or sample size |
| Skew or heavy tails | median, IQR/MAD, p50/p90, range | mean alone as the headline |
| Categories | counts, percentages, mode | average of category codes |
| Missing values | null count/rate and sensitivity discussion | silently dropping missing rows |
| Potential outliers | robust summaries + investigated examples | automatic deletion just because a value is extreme |

Always pair a center with spread and sample size; report null rate and relevant inclusion criteria. Plot a histogram/box plot when shape matters and the visualization can be generated honestly from the actual data.

A high or low value is only a *potential outlier*. Check for data-entry/unit issues, duplicates, valid rare events, and population differences. If an outlier remains valid, keep it and explain its impact; a robust median/IQR/MAD can complement the mean/SD.

Do not average ratios or rates without checking numerator/denominator weights. Do not infer causation from a histogram, a correlation matrix, or descriptive summaries. For tests, confidence intervals, or causal claims, use a separate inferential design with assumptions and a pre-specified question.
