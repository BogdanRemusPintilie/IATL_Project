import pandas as pd 
import matplotlib.pyplot as plt

file_path_price = "C:\\Users\\Bogdan\\OneDrive - University of Warwick\\Desktop\\weather + OIL data\\Data\\cleaned.xlsx"
file_path_temp = "C:\\Users\\Bogdan\\OneDrive - University of Warwick\\Desktop\\weather + OIL data\\Data\\Dubai_Texas_Temperature.xlsx"

data_price = pd.read_excel(file_path_price)
data_temp = pd.read_excel(file_path_temp)

data_price["Price_Rolling_Corr"] = data_price["Dubai_Prices"].rolling(window=30).corr(data_price["Texas_Prices"])
data_temp['Temp_Rolling_Corr'] = data_temp['Temperature_Dubai'].rolling(window=30).corr(data_temp['Temperature_Texas'])

avg_rolling_corr_price = data_price["Price_Rolling_Corr"].mean()
avg_rolling_corr_temp = data_temp["Temp_Rolling_Corr"].mean()

std_rolling_corr_price = data_price["Price_Rolling_Corr"].std()
std_rolling_corr_temp = data_temp["Temp_Rolling_Corr"].std()

upper_bound_price = avg_rolling_corr_price + std_rolling_corr_price
upper_bound_temp = avg_rolling_corr_temp + std_rolling_corr_temp

lower_bound_price = avg_rolling_corr_price - std_rolling_corr_price
lower_bound_temp = avg_rolling_corr_temp - std_rolling_corr_temp

data_price["Signal"]= 0 # 0=no action
data_temp["Signal"]= 0
data_price.loc[data_price["Price_Rolling_Corr"]>upper_bound_price, 'Signal'] = -1 # Short x / Long the question is which one, who is x? Dubai or Texas #loc locks on the rows where a condition is met and assigns the value in the column you give
data_price.loc[data_price["Price_Rolling_Corr"]<lower_bound_price, 'Signal'] = 1 # Long x / Short the question is which one, who is x? Dubai or Texas
data_temp.loc[data_temp["Temp_Rolling_Corr"]>upper_bound_temp, 'Signal'] = -1 # Short x / Long the question is which one, who is x? Dubai or Texas #loc locks on the rows where a condition is met and assigns the value in the column you give
data_temp.loc[data_temp["Temp_Rolling_Corr"]<lower_bound_temp, 'Signal'] = 1 # Long x / Short the question is which one, who is x? Dubai or Texas

correlation_price = data_price["Dubai_Prices"].corr(data_price["Texas_Prices"])
correlation_temp = data_temp['Temperature_Dubai'].corr(data_temp['Temperature_Texas'])

plt.figure(figsize=(14,7))
plt.plot(data_price["Date"], data_price["Price_Rolling_Corr"], label = f"Price corr={round(correlation_price,2)}", color = 'blue')
plt.plot(data_temp['Date'], data_temp['Temp_Rolling_Corr'], label= f"Temp corr={round(correlation_temp,2)}", color = 'purple')

plt.axhline(y=avg_rolling_corr_price, linestyle='--', label='Avg Rolling Price Correlation', color='orange')
plt.axhline(y=upper_bound_price, linestyle='--', label='Upper Bound Price', color='red')
plt.axhline(y=lower_bound_price, linestyle='--', label='Lower Bound Price', color='green')

plt.axhline(y=avg_rolling_corr_temp, linestyle='--', label='Avg Rolling Temp Correlation', color='orange')
plt.axhline(y=upper_bound_temp, linestyle='--', label='Upper Bound Temp', color='red')
plt.axhline(y=lower_bound_temp, linestyle='--', label='Lower Bound Temp', color='green')

plt.title('Rolling Correlation and Trading Signals')
plt.xlabel('Date')
plt.ylabel('Rolling Correlation')
plt.legend()
plt.tight_layout()
plt.show()

updated_price_file_path = "C:\\Users\\Bogdan\\OneDrive - University of Warwick\\Desktop\\weather + OIL data\\Data\\lets see\\price.xlsx"
updated_temp_file_path = "C:\\Users\\Bogdan\\OneDrive - University of Warwick\\Desktop\\weather + OIL data\\Data\\lets see\\temp.xlsx"

data_price.to_excel(updated_price_file_path, index=False)
data_temp.to_excel(updated_temp_file_path, index=False)