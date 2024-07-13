import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import yfinance as yf

ticker_symbol = "AAPL"
start_date = "2000-01-01"
end_date = "2019-12-17"

df = yf.download(ticker_symbol, start=start_date, end=end_date)

data = df.filter(["Close"])
dataset = data.values
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(dataset)

training_data_len = int(len(dataset) * 0.8)
train_data = scaled_data[0:training_data_len, :]
test_data = scaled_data[training_data_len - 60:, :]

def create_dataset(data, window_size):
    x, y = [], []
    for i in range(window_size, len(data)):
        x.append(data[i-window_size:i, 0])
        y.append(data[i, 0])
    return np.array(x), np.array(y)

window_size = 60
x_train, y_train = create_dataset(train_data, window_size)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(window_size, 1)))
model.add(LSTM(50, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(x_train, y_train, batch_size=1, epochs=1)

x_test, y_test = create_dataset(test_data, window_size)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

train = data[:training_data_len]
valid = data[training_data_len:]
valid.loc[:, 'Predictions'] = predictions

plt.figure(figsize=(10, 6))
plt.title("Model")
plt.xlabel("Date", fontsize=10)
plt.ylabel("Price", fontsize=10)
plt.plot(train["Close"], label="Train")
plt.plot(valid["Close"], label="Val")
plt.plot(valid["Predictions"], label="Predictions")
plt.legend(loc="lower right")
plt.show()