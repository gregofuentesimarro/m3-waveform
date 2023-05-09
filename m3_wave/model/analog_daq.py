from m3_wave.controller.pftl_daq import Device
import pint 

ur = pint.UnitRegistry()

# Important. Adding features to the controller would imply violating
# the separation of models and controllers. 
# Write one model per device. 

class AnalogDaq:
    def __init__(self, port):
        self.port = port 
        self.driver = Device(self.port)

    def __str__(self):
        '''
        This method lets Python know how to transform an object to a string.
        '''
        return "Analog Daq"

    def initialize(self):
        self.driver.initialize()
        self.set_voltage(0, ur('0V'))
        self.set_voltage(1, ur('0V'))
    
    def get_voltage(self, channel):
        '''
        Output is given in volts
        '''
        voltage_bits = self.driver.get_analog_input(channel)
        voltage = voltage_bits*ur('3.3V')/1023

        return voltage

    def set_voltage(self, channel, volts):
        '''
        Input is given in volts.
        '''
        value_volts = volts.m_as('V')
        value_int = round(value_volts / 3.3 * 4095) 
        self.driver.set_analog_output(channel, value_int)
    
    def finalize(self):
        '''
        Sets the voltages to 0 and finalizes the controller (driver).
        '''
        self.set_voltage(0, ur('0V'))
        self.set_voltage(1, ur('0V'))
        self.driver.finalize()

if __name__ == "__main__":
    daq = AnalogDaq('COM3')
    daq.initialize()
    voltage = ur('3000mV')
    daq.set_voltage(0, voltage)
    input_volts = daq.get_voltage(0)
    print(input_volts)
    daq.finalize()