# Forecasting monthly sunspot activity

Python · ARIMA · Forecast evaluation

I compared ARIMA models using 2015–2017 for training and 2018 for model selection. ARIMA(1,1,0) recorded a validation RMSE of 4.34 sunspots.

| Stage | Training years | Evaluation year | RMSE (sunspots) |
|---|---|---|---:|
| Select model order | 2015–2017 | 2018 | 4.34 |
| Evaluate selected order | 2015–2018 | 2019 | 3.88 |

After selecting the order, I refit the model through December 2018 and forecast the 12 months of 2019. The test RMSE was 3.88 sunspots. Reserving the final year kept the model selection decision independent of the test score.
