import pandas as pd
import matplotlib.pyplot as plt

path_file= "C:\\Users\\Bogdan\\OneDrive - University of Warwick\\Desktop\\weather + OIL data\\Data\\lets see\\price_spread.xlsx"

data_price = pd.read_excel(path_file)

data_price["Daily P&L"]=0.0
net_position=0 # +1 for long Dubai / short Texas, -1 for short Dubai / long Texas
spread_mean = data_price["Spread"].mean()

for i in range(1, len(data_price) - 1):
    current_spread=data_price.at[i,"Spread"] #accesses the value in the ith row of the Spread column of the dataset
    next_spread = data_price.at[i+1,"Spread"]
    #previous_spread=data_price.at[i-1,"Spread"]
    signal = data_price.at[i,'Spread_Signal']

    if signal == 1:
        net_position = net_position + 1
    elif signal == -1:
        net_position = net_position -1
    elif abs(current_spread - spread_mean) < 0.01:#floating-point numbers are an approximation of real numbers. Due to this approximation, two numbers that are mathematically equal might not be exactly equal in their floating-point representation
        net_position = 0
   
    if net_position == 1:
        data_price.at[i+1,"Daily P&L"] = next_spread - current_spread
    elif net_position == -1:
        data_price.at[i+1,"Daily P&L"] = current_spread - next_spread

data_price["Cumulative P&L"] = data_price["Daily P&L"].cumsum()
plt.figure(figsize=(14,7))
plt.plot(data_price["Date"], data_price["Cumulative P&L"], label = f"Final P&L = {data_price['Cumulative P&L'].iloc[-1]:.2f}")
plt.title("P&L evolution")
plt.ylabel("P&L")
plt.xlabel("Date")
plt.legend()
plt.show()