from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton 

from pftl.model.experiment import Experiment
from PyQt5.QtWidgets import QApplication
from pftl.view.main_window import MainWindow

experiment = Experiment("C:/Users/grego/Box/Cornell Spring 2023/ADVANCED LAB/SKILL/pftl/examples/experiment.yml")
experiment.load_config()
experiment.load_daq()

app = QApplication([])
window = MainWindow(experiment)
window.show()
app.exec()

experiment.finalize()