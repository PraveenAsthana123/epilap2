# Time-Series Analysis — Seizure Diary (EP001)

> **Why (this doc):** Seizure frequency is longitudinal, so it is modelled as a time series with the
> proper controls (time-based split, stationarity, seasonality) rather than as i.i.d. rows. **How:**
> `analysis/timeseries.py` runs parse/sort → duplicate + missing-timestamp handling → resampling →
> rolling/lag/calendar features → decomposition → ADF stationarity + differencing → time-based split
> + time-series CV → SARIMAX + gradient-boosting → MAE/RMSE/MAPE/MASE.

**Series:** 180 days (EP001). Cleaning removed duplicate timestamps and filled
2 missing day(s) by interpolation; timestamps normalised to UTC.

## Stationarity (Augmented Dickey-Fuller)
ADF p = 0.0 (stationary);
after first differencing p = 0.0 → differencing applied where needed.

## Decomposition (trend + weekly seasonality)
![decomposition](analysis/outputs/timeseries/decomposition.png)

## Forecast — time-based holdout (5-fold time-series CV; NO random split)
| model | MAE | RMSE | MAPE | MASE |
|---|---|---|---|---|
| SARIMAX(1,1,1)(1,0,1,7) | 0.694 | 0.886 | 52.400 | 0.021 |
| GradientBoosting(lags) | 0.691 | 0.852 | 58.300 | 0.019 |

![forecast](analysis/outputs/timeseries/forecast.png)

**Reason:** Forecast next-period seizure counts under time-aware validation. **Why:** Random splits leak the future; time-based split + TimeSeriesSplit prevent it. **What is happening:** Weekly seasonality (worse Fri-Sun) + slight upward trend are captured; SARIMAX and a lag-based GBM are compared. **How it is happening:** MAE/RMSE/MAPE/MASE quantify error; MASE<1 beats seasonal-naive. **Reference:** Hyndman & Athanasopoulos (2021); Box & Jenkins (1970).

## Professor Readiness (Defense Q&A)

**Q1: Why never a random split for time series?** Random splits place future points in training,
leaking information; a chronological split + expanding-window CV respect temporal order.

**Q2: Why MASE?** It is scale-free and compares against a seasonal-naive baseline, so <1 means the
model genuinely beats "next week = last week".

**Q3: Which model wins here?** See the table — the lag-based gradient-boosting and SARIMAX are
compared on identical time-based holdout.

## References

Box, G. E. P., & Jenkins, G. M. (1970). *Time series analysis: Forecasting and control*. Holden-Day.

Hyndman, R. J., & Athanasopoulos, G. (2021). *Forecasting: Principles and practice* (3rd ed.). OTexts.
