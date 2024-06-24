import pandas as pd 
import matplotlib.pyplot as plt

file_path_price = "C:\\Users\\Bogdan\\OneDrive - University of Warwick\\Desktop\\weather + OIL data\\Data\\cleaned.xlsx"

data_price = pd.read_excel(file_path_price)

# Calculate the spread
data_price['Spread'] = data_price['Dubai_Prices'] - data_price['Texas_Prices']

# Calculate the mean and standard deviation of the spread
spread_mean = data_price['Spread'].mean()
spread_std = data_price['Spread'].std()

# Define thresholds
upper_threshold_spread = spread_mean + spread_std
lower_threshold_spread = spread_mean - spread_std

# Generate signals based on spread
data_price['Spread_Signal'] = 0
data_price.loc[data_price['Spread'] > upper_threshold_spread, 'Spread_Signal'] = -1  # Short Dubai / Long Texas
data_price.loc[data_price['Spread'] < lower_threshold_spread, 'Spread_Signal'] = 1   # Long Dubai / Short Texas

# Plot to visualize
plt.figure(figsize=(14, 7))
plt.plot(data_price['Date'], data_price['Spread'], label=f'Spread mean =${round(spread_mean,2)}', color='blue')
plt.axhline(y=spread_mean, color='orange', linestyle='--', label='Mean Spread')
plt.axhline(y=upper_threshold_spread, color='red', linestyle='--', label='Upper Threshold')
plt.axhline(y=lower_threshold_spread, color='green', linestyle='--', label='Lower Threshold')
plt.title('Price Spread and Trading Signals')
plt.xlabel('Date')
plt.ylabel('Spread (Dubai - Texas) $')
plt.legend()
plt.show()

# Display the DataFrame with spread signals
file_path_price_uploaded= "C:\\Users\\Bogdan\\OneDrive - University of Warwick\\Desktop\\weather + OIL data\\Data\\lets see\\price_spread.xlsx"
data_price.to_excel(file_path_price_uploaded,index=False)