import numpy as np 
from pftl import ur

from pftl.model.analog_daq import AnalogDaq

V = ur('V')

daq = AnalogDaq('COM3') # <-- Remember to change the port
daq.initialize()
# 11 Values with units in a numpy array... 0, 0.3, 0.6, etc.
volt_range = np.linspace(0, 3, 11) * V
currents = [] # Empty list to store the values

for volt in volt_range:
    daq.set_voltage(0, volt)
    measured_voltage = daq.get_voltage(0)
    print(measured_voltage)
#    current = measured_voltage/ur('1000ohm')
#    currents.append(current)

daq.finalize()
#print(current)