import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_pacf
from datetime import datetime, timedelta
from arch import arch_model
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Load and preprocess data
df = pd.read_csv("C:\\Users\\Bogdan\\OneDrive - University of Warwick\\Desktop\\Temp prediction\\MIDLAND TEXAS, TX US.csv")
df['DATE'] = pd.to_datetime(df['DATE'], format="%Y-%m-%d")
df = df.set_index('DATE')
df['TCELCIUS'] = (df['TAVG'] - 32) * 5 / 9
df = df.drop(columns=['TMAX', 'TMIN', 'STATION', 'TAVG'])
df = df.asfreq(pd.infer_freq(df.index))
df = df.resample('M').mean()

# Define train and test periods
train_end = datetime(2024, 1, 31)
test_end = datetime(2024, 7, 31)

train_data = df[:train_end + timedelta(days=1)]
test_data = df[train_end + timedelta(days=1):]  # 6 months

# Define model orders
integrated_order = (0, 1, 0)
seasonal_order = (1, 0, 1, 12)

rolling_predictions_SARIMAX = pd.Series(index=test_data.index)
rolling_predictions_GARCH = pd.Series(index=test_data.index)

# SARIMAX Model Forecasting
for i in test_data.index:
    train_data_temp = df[:i]
    model = SARIMAX(train_data_temp, order=integrated_order, seasonal_order=seasonal_order)
    model_fit = model.fit(disp=False)
    forecast = model_fit.get_forecast(steps=1).predicted_mean
    rolling_predictions_SARIMAX.loc[i] = forecast.values[0]

# GARCH Model Forecasting
for i in test_data.index:
    train_data_temp = df[:i]
    residuals = SARIMAX(train_data_temp, order=integrated_order, seasonal_order=seasonal_order).fit(disp=False).resid
    if len(residuals) == 0:
        continue
    model = arch_model(residuals, p=1, q=1)
    model_fit = model.fit(disp="off")
    garch_forecast = model_fit.forecast(horizon=1).variance.values[0]
    rolling_predictions_GARCH.loc[i] = np.sqrt(garch_forecast)

# Combine forecasts
the_actual_forecast = rolling_predictions_SARIMAX + rolling_predictions_GARCH * np.random.normal(size=len(test_data))

# Plot results
plt.figure(figsize=(10, 4))
plt.plot(the_actual_forecast, label='Predictions')
plt.plot(test_data, label='Data')
plt.title('Actual Predictions')
plt.ylabel('Degrees')
plt.xlabel('Time')
plt.legend()
plt.show()