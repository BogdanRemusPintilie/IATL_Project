import pandas as pd 
import matplotlib.pyplot as plt

file_path = "C:\\Users\\Bogdan\\OneDrive - University of Warwick\\Desktop\\weather + OIL data\\Data\\cleaned.xlsx"

data = pd.read_excel(file_path)

data["Price_Rolling_Corr"] = data["Dubai_Prices"].rolling(window=30).corr(data["Texas_Prices"])
correlation = data["Dubai_Prices"].corr(data["Texas_Prices"])

plt.figure(figsize=(10,5))
plt.plot(data["Date"], data["Price_Rolling_Corr"], label = f"Overall corr={correlation}")
plt.title("Rolling correlation (30-dya window) Dubai - Texas  Prices")
plt.ylabel("Rolling correlation")
plt.xlabel("Date")
plt.legend()
plt.show()