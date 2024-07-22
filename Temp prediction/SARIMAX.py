import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from datetime import datetime
from datetime import timedelta
from statsmodels.tsa.statespace.sarimax import SARIMAX
import numpy as np
from arch import arch_model

df=pd.read_csv("C:\\Users\\Bogdan\\OneDrive - University of Warwick\\Desktop\\Temp prediction\\MIDLAND TEXAS, TX US.csv")
df['DATE'] = pd.to_datetime(df['DATE'],format='%Y-%m-%d')
df=df.set_index('DATE')
df['TCELSIUS'] = (df['TAVG'] - 32) * 5/9
df=df.drop(columns=['TMAX','TMIN','STATION','TAVG'])
df = df.asfreq(pd.infer_freq(df.index))
#too many datapoints for an SARIMAX (0,1,0)(4,0,4,365)
df = df.resample('M').mean()

train_end=datetime(2024,1,31)
test_end=datetime(2024,7,31)

train_data=df[:train_end+timedelta(days=1)]
test_data=df[train_end+timedelta(days=1):] #6 months

integrated_order=(0,1,0)
seasonal_order = (1,0,1,12)

rolling_predictions=pd.Series(index=test_data.index)

for i in test_data.index:
    train_data=df[:i-timedelta(days=1)]
    model=SARIMAX(train_data, order=integrated_order, seasonal_order=seasonal_order)
    model_fit=model.fit()
    predictions=model_fit.forecast()
    rolling_predictions.loc[i]=predictions
print(rolling_predictions)












