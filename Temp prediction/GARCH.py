import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_pacf
from datetime import datetime
from datetime import timedelta
from arch import arch_model


df=pd.read_csv("C:\\Users\\Bogdan\\OneDrive - University of Warwick\\Desktop\\Temp prediction\\MIDLAND TEXAS, TX US.csv")
df['DATE']=pd.to_datetime(df['DATE'],format="%Y-%m-%d")
df=df.set_index('DATE')
df['TCELCIUS']=(df['TAVG']-32)*5/9
df=df.drop(columns=['TMAX','TMIN','STATION','TAVG'])
df = df.asfreq(pd.infer_freq(df.index))
df=df.resample('M').mean()


first_diff=df.diff()[1:]



train_end=datetime(2024,1,31)
test_end=datetime(2024,7,31)

train_data=first_diff[:train_end + timedelta(days=1)]
test_data=first_diff[train_end+timedelta(days=1):]


rolling_predictions=[]
for i in test_data.index:
    train_data=first_diff[:i]
    model=arch_model(train_data,p=1,q=1)
    model_fit=model.fit()
    predictions=model_fit.forecast(horizon=1)
    rolling_predictions.append(np.sqrt(predictions.variance.values[0]))



rolling_predictions_index = pd.date_range(start=test_data.index[0], end=test_data.index[-1], freq='M')
rolling_predictions_df=pd.DataFrame(data=rolling_predictions,index=rolling_predictions_index, columns=['Predictions'])

plt.figure(figsize=(10,4))
plt.plot(rolling_predictions_df['Predictions'], label='Predictions')
plt.plot(test_data, label='Data')
plt.title('Rolling Predictions')
plt.ylabel('Degrees')
plt.xlabel('Time')
plt.legend()
plt.show()









