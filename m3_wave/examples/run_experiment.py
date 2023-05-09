import sys 
import os 
from time import sleep
import pyqtgraph as pg
import threading 

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from m3_wave.model.experiment import Experiment

experiment = Experiment("C:/Users/grego/Box/Cornell Spring 2023/ADVANCED LAB/SKILL/m3_wave/examples/experiment.yml")
experiment.load_config()
experiment.load_daq()
experiment.load_wave()
experiment.start_wave()
sleep(120)
experiment.finalize()
# Need to be able to stop this somehow
#experiment.finalize()

