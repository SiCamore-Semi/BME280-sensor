import matplotlib.pyplot as plt
import BME280_reader
import time
plt.ion()
temps = []
#plt.ylim(30,100)
while 1:
    time.sleep(.2)
    temps.append(BME280_reader.get_fahrenheit())
    plt.plot(temps)
    plt.show()
    plt.pause(0.0001)
