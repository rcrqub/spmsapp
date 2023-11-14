import random
from datetime import datetime, timedelta
import time

def stockUsed():
    options = [0, 1, 2, 3, 4, "Restock"]
    weights = [20, 4, 2, 1, 1, 3]  # Adjust the weights based on the desired probabilities

    return str(random.choices(options, weights=weights)[0])


start_date = datetime(2024, 1, 1, 8, 0) # Start date = 1st Jan 2024
end_date = datetime(2025, 1, 1, 0, 0) # End date = 1st Jan 2025
delta = timedelta(hours=1)  # Iterate by 1 hour
while start_date <= end_date:
    action = stockUsed()
    if action != "Restock":
        print(start_date.strftime("%Y-%m-%d %H:%M, Stock used = " + action))
    else: print(start_date.strftime("%Y-%m-%d %H:%M, RESTOCK"))
    time.sleep(0.5)
    if start_date.hour == 22: start_date += 10*delta # If time is 10pm move to 8am
    else: start_date += delta # Add 1 hour to the time


