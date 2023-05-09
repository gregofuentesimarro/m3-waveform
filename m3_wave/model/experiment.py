import yaml
from m3_wave.model.analog_daq import AnalogDaq
from m3_wave import ur
from time import sleep
import numpy as np
import os
from datetime import datetime
import threading

Q_ = ur.Quantity

class Experiment:
    def __init__(self, config_file):
        self.is_running = False
        self.config_file = config_file
        #self.scan_range = np.array([0]) * ur('V')
        #self.scan_data = np.array([0]) * ur('V')
        self.config = None
        self.daq = None
        self.sine_wave = None
        self.wave_thread = None
        self.keep_running = True
        self.is_running = None

    def load_config(self):
        with open(self.config_file, 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        self.config = data

    def load_daq(self):
        '''
        Having a config file in YAML format makes it very easy to navigate
        and locate the information for the DAQ port. Include if-else 
        statements to choose between several different DAQs.
        '''
        self.daq = AnalogDaq(self.config['DAQ']['port'])
        self.daq.initialize()

    def load_wave(self):
        dc_offset = ur(self.config['Wave']['dc_offset']).m_as('V')
        amplitude = ur(self.config['Wave']['amplitude']).m_as('V')
        resolution = int(self.config['Wave']['resolution'])
        self.sine_wave = [dc_offset + amplitude*np.sin(2*np.pi*i/resolution) 
                     for i in range(0, resolution)]*ur('V')
    
    def start_wave(self):
        self.wave_thread = threading.Thread(target=self.send_wave)
        self.wave_thread.start()

    def stop_wave(self):
        self.keep_running = False

    def send_wave(self):
        if self.is_running:
            print('Wave already running')
            return
        self.is_running = True 

        i = 0
        while self.keep_running:
            self.daq.set_voltage(self.config['Wave']['channel_out'], self.sine_wave[i])
            i = (i+1) % len(self.sine_wave)

        self.is_running = False

    # def save_data(self):
        # data_folder = self.config['Saving']['folder']
        # today_folder = f'{datetime.today():%y-%m-%d}'
        # saving_folder = os.path.join(data_folder, today_folder)
        # if not os.path.isdir(saving_folder):
        #     os.makedirs(saving_folder)

        # data = np.vstack([self.scan_range, self.scan_data]).T 
        # header = "Scan range in 'V, Scan Data in 'V'"
        
        # filename = self.config['Saving']['filename']
        # base_name = filename.split('.')[0]
        # ext = filename.split('.')[-1]
        # i = 1
        # while os.path.isfile(os.path.join(saving_folder, f'{base_name}_{i:04d}.{ext}')):
        #     i += 1
        # data_file = os.path.join(saving_folder, f'{base_name}_{i:04d}.{ext}')
        # metadata_file = os.path.join(saving_folder, f'{base_name}_{i:04d}_metadata.yml')
        # np.savetxt(data_file, data.m_as('V'), header=header)
        
        # with open(metadata_file, 'w') as f:
        #     f.write(yaml.dump(self.config, default_flow_style=False))

    def finalize(self):
        print('Finalizing experiment')
        self.stop_wave()
        while self.is_running:
            sleep(.1)
        self.daq.finalize()