from Simulation import Simulation
from csv import DictWriter

fieldNames = ['year','month','day','hour','bathroom_id','item_type','stock_level']

sim = Simulation()
dayData = sim.simulateDay()


with open('ReportingData.csv', 'w') as file:
    write = DictWriter(file, fieldnames=fieldNames)
    write.writeheader()
    for day in dayData:
        for hour in day:
            dict1 = dict(zip(fieldNames, hour))
            print(dict1)
            write.writerow(dict1)
