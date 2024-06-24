import pandas as pd
import matplotlib.pyplot as plt

file_path = "C:\\Users\\Bogdan\\OneDrive - University of Warwick\\Desktop\\weather + OIL data\\Data\\Dubai_Texas_Temperature.xlsx"

data = pd.read_excel(file_path)

# Calculate rolling correlation with a 30-day window
data['Temp_Rolling_Corr'] = data['Temperature_Dubai'].rolling(window=30).corr(data['Temperature_Texas'])
correlation = data['Temperature_Dubai'].corr(data['Temperature_Texas'])

# Plot the rolling correlation
plt.figure(figsize=(10, 5))
plt.plot(data['Date'], data['Temp_Rolling_Corr'], label= f"Overall corr={correlation}")
plt.xlabel('Date')
plt.ylabel('Rolling Correlation')
plt.title('Rolling Correlation between Temperatures in Dubai and Texas (30-day rolling window)')
plt.legend()
plt.show()