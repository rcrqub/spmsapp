import random
from datetime import datetime, timedelta
import time
import pandas as pd



df = pd.read_csv('BathroomData.csv')

# Iterate through each bathroom and product type and choose how much stock has been used per call
def randomise():
    stockLevel = df['stock_level']
    for index in range(0,len(stockLevel)-1):
        remainingStock = stockLevel[index] - stockUsed()
        if remainingStock >= 0:
            df.loc[index, 'stock_level'] = remainingStock

def stockUsed():
    options = [0, 1, 2, 3, 4] 
    weights = [20, 4, 2, 1, 1]  # Adjust the weights based on the desired probabilities
    return random.choices(options, weights=weights)[0]

start_date = datetime(2024, 1, 1, 8, 0) # Start date = 1st Jan 2024
end_date = datetime(2024, 1, 1, 22, 0) # End date = 1st Jan 2024
delta = timedelta(hours=1)  # Iterate by 1 hour

zeroAlerts = [] #Keeps track of whether the "stock empty" alert has come up yet
for itemID in df['stock_level']:
    zeroAlerts.append(False)

print(df)
while start_date <= end_date:
    action = randomise()
    print(start_date.strftime("%Y-%m-%d %H:%M"))
    #time.sleep(.5)
    if start_date.hour == 22: start_date += 10*delta # If time is 10pm move to 8am
    else: start_date += delta # Add 1 hour to the time
    
    #alert if [bathroom/product] empty
    for index in range(0,len(df['stock_level'])-1):
        if (df['stock_level'][index] == 0) and (not zeroAlerts[index]):
            zeroAlerts[index] = True #sets alert flag
            print("ALERT: Empty stock! Bathroom " + str(df['bathroom_id'][index]) + ", item " + str(df['item_type'][index]))
print(df)
