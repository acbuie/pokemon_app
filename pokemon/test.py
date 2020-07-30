import time
from utility import StopWatch

t = StopWatch()

x = 0

t.start()
while x < 100000:
    print(x)
    t.lap(store= True)
    x += 1

print(f'Average Lap: {t.average_lap:.4f} Seconds')
print(t.stop())
