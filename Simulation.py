import random
from datetime import datetime, timedelta
import pandas as pd


class Simulation:
    def __init__(self):
        self.df = pd.read_csv('InitialData.csv')
        self.startDate = datetime(2024, 1, 1, 8, 0) # Start date = 1st Jan 2024
        print(self.startDate)
        self.endDate = datetime(2024, 1, 31, 22, 0) # End date = 1st Jan 2025
        self.delta = timedelta(hours=1)  # Iterate by 1 hour
        self.closingHour = 22
        self.hoursTilOpen = 10

    def stockUsed(self):
        options = [0, 1, 2, 3, 4, 99] # 99 indicates restock item
        weights = [40, 8, 4, 2, 2, 1]  # Adjust the weights based on the desired probabilities
        return random.choices(options, weights=weights)[0]
    
    def randomise(self):
        report = []
        stockLevel = self.df['stock_level']
        bathroomID = self.df['bathroom_id']
        itemType = self.df['item_type']
        for index in range(0,len(stockLevel)):
            stockUsed = self.stockUsed()
            if stockUsed != 99:
                remainingStock = stockLevel[index] - stockUsed
                if remainingStock >= 0:
                    self.df.loc[index, 'stock_level'] = remainingStock
                report.append([self.startDate.strftime("%Y"),self.startDate.strftime("%m"),self.startDate.strftime("%d"), self.startDate.strftime("%H"), bathroomID[index], itemType[index], stockLevel[index]])
            else: 
                self.df.loc[index, 'stock_level'] = self.df.loc[index, 'stock_level'] + random.randint(10,15)
                report.append([self.startDate.strftime("%Y"),self.startDate.strftime("%m"),self.startDate.strftime("%d"), self.startDate.strftime("%H"), bathroomID[index], itemType[index], stockLevel[index]])
        return report
    
    def simulateDay(self):
        action = []
        while self.startDate <= self.endDate:
            action.append(self.randomise())
            if self.startDate.hour == self.closingHour: self.startDate += self.hoursTilOpen*self.delta # If time is 10pm move to 8am
            else: self.startDate += self.delta # Add 1 hour to the time
        return action
    
        