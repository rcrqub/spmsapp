from Simulation import Simulation
from csv import DictWriter

fieldNames = ['year','month','day','hour','bathroom_id','item_type','stock_level']

sim = Simulation()
data = sim.simulate()

with open('ReportingDataMonth.csv', 'w') as file:
    write = DictWriter(file, fieldnames=fieldNames)
    write.writeheader()
    for day in data:
        for hour in day:
            dict1 = dict(zip(fieldNames, hour))
            print(dict1)
            write.writerow(dict1)