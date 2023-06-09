import serial 
from time import sleep 

class Device:
    DEFAULTS = {'write_termination': '\n',
                'read_termination': '\n',
                'encoding': 'ascii',
                'baudrate': 9600,
                'read_timeout': 1, 
                'write_timeout': 1}

    def __init__(self, port):
        self.port = port 
        self.rsc = None 

    def initialize(self):
        self.rsc = serial.Serial(port=self.port, 
                            baudrate=self.DEFAULTS['baudrate'],
                            timeout=self.DEFAULTS['read_timeout'],
                            write_timeout=self.DEFAULTS['write_timeout'])
        sleep(1)

    def query(self, message):
        message = message + self.DEFAULTS['write_termination']
        message = message.encode(self.DEFAULTS['encoding'])
        self.rsc.write(message)
        ans = self.rsc.readline() 
        ans = ans.decode(self.DEFAULTS['encoding']).strip()
        return ans

    def idn(self):
        return self.query('IDN')

    def get_analog_input(self, channel):
        message = 'IN:CH{}'.format(channel)
        ans = self.query(message)
        ans = int(ans)
        return ans
    
    def set_analog_output(self, channel, output_value):
        message = 'OUT:CH{}:{}'.format(channel, output_value)
        self.query(message)

    def finalize(self):
        if self.rsc is not None:
            self.rsc.close()

if __name__ == "__main__":   
    dev = Device('COM3')
    dev.initialize()
    serial_number = dev.idn() 
    print(f'The serial number is: {serial_number}')
    for i in range(10):
        dev.set_analog_output(0, 4000)
        volts = dev.get_analog_input(0)
        print(f'Measured {volts}')
        sleep(.5)
        dev.set_analog_output(0, 0)
        volts = dev.get_analog_input(0)
        print(f'Measured {volts}')
        sleep(.5)
