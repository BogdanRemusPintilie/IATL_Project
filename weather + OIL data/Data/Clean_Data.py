import pandas as pd

# Load the Excel file
file_path = "C:\\Users\\Bogdan\\OneDrive - University of Warwick\\Desktop\\weather + OIL data\\Data\\Dubai_Texas_Prices.xlsx"
df = pd.read_excel(file_path)

# Drop rows where both 'Dubai_Prices' and 'Texas_Prices' are NaN
cleaned_df = df.dropna(subset=['Dubai_Prices', 'Texas_Prices'], how='all') #"any" is for either columns having NaN

# Save the cleaned dataframe to a new Excel file
cleaned_file_path = "C:\\Users\\Bogdan\\OneDrive - University of Warwick\\Desktop\\weather + OIL data\\Data\\cleaned.xlsx"
cleaned_df.to_excel(cleaned_file_path, index=False)