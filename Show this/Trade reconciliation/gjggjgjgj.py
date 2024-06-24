import pandas as pd
import numpy as np

np.random.seed(0) #if you use np.random from now on each time you hit run youe get the same values else different random variables will be created

# Generate sample internal oil trading data
internal_oil_data = pd.DataFrame({#create a table
    'trade_id': np.arange(1, 101),#denote the column trade_id as an array starting from 1 going up to 101 but not including 1o1. Ascending order by default.
    'contract': np.random.choice(['Brent', 'WTI', 'Dubai', 'Oman'], size=100), # denote the column contract as an array of 100 names taken randomly from the list
    'quantity': np.random.randint(1000, 10000, size=100),  # creates size amount of random integers between the lower bound (1000,inclusive) and upper bound (10000, exclusive) 
    'price': np.round(np.random.uniform(50, 120, size=100), 2),  #creates 100 floats from a random distribution with ranges of 50 and 120 exclusinve and rounds the numbers to 2 decimals
    'trade_date': pd.date_range(start='2024-01-01', periods=100, freq='B') #create a range of dates strating from 1st/01/2024, 100 days, Business days
})
internal_oil_data['value'] = internal_oil_data['quantity'] * internal_oil_data['price'] #must be outside cause u need to create table['price/quant'] first

# Generate sample external oil pricing data (introducing some discrepancies)
external_oil_data = internal_oil_data.copy() #copy the table
external_oil_data['price'] = external_oil_data['price'] + np.round(np.random.uniform(-2, 2, size=100), 2)  # you alter the price column by smth between -2 and 2
external_oil_data['value'] = external_oil_data['quantity'] * external_oil_data['price'] #otherwise the value column doesn't change

# Merge internal and external data
merged_oil_data = pd.merge(internal_oil_data, external_oil_data, on='trade_id', suffixes=('_internal', '_external')) #merges the 2 tables on the comon trade_id column. The internal on the left, external on the right, and adds th efirst suffix to the left table's column's and the second //--//--// (this is a smart thing)
# Validate data
merged_oil_data['price_diff'] = np.abs(merged_oil_data['price_internal'] - merged_oil_data['price_external']) #new column with the difference between internal and external prices
merged_oil_data['value_diff'] = np.abs(merged_oil_data['value_internal'] - merged_oil_data['value_external']) #new column with the difference between internal and external prices

# Define a threshold for discrepancies
price_threshold = 1  # don't exceed this
value_threshold = 5000  # don't exceed this

# Flag discrepancies
merged_oil_data['price_discrepancy'] = merged_oil_data['price_diff'] > price_threshold #false/true
merged_oil_data['value_discrepancy'] = merged_oil_data['value_diff'] > value_threshold #false/true

#Copy last table to alter and only desplay the flagged entries (last 2 columns with TRUE, either column)
flagged_discrepancies = merged_oil_data[(merged_oil_data['price_discrepancy']) | (merged_oil_data['value_discrepancy'])] #smart, inside you will have TRUE OR FALSE which results in either TRUE/FALSE. Now, only the entries with TRUE, cause you will have each entry of the df with a boolean value, will be displayed. Boolean indexing.
#print (flagged_discrepancies)
NOT_flagged_discrepancies = merged_oil_data[~((merged_oil_data['price_discrepancy']) | (merged_oil_data['value_discrepancy']))] #added not inside so false is now true and is spit
print(NOT_flagged_discrepancies)

#flagged_discrepancies.to_csv('reconciliation_report.csv', index=False)