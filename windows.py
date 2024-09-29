from custom_elements import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import time


class SNSubWindow(QMdiSubWindow):
    def __init__(self, snRef):
        super().__init__()
        self.setWindowTitle("SN")
        self.setGeometry(200, 200, 300, 700)

        self.table_widget = QTableWidget()
        self.snRef = snRef
        self.update_table()

        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)

        widget = QWidget()
        widget.setLayout(layout)

        self.setWidget(widget)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_table)
        self.timer.start(100)  # Trigger every 1000 milliseconds (1 second)

    def update_table(self):
        dictionary = self.snRef.names_dict
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(['Key', 'Value'])
        self.table_widget.setRowCount(len(dictionary))
        self.table_widget.verticalHeader().setVisible(False)  # Hide vertical header

        row = 0
        for key, value in dictionary.items():
            key_item = QTableWidgetItem(str(key))
            value_item = QTableWidgetItem(str(value))

            self.table_widget.setItem(row, 0, key_item)
            self.table_widget.setItem(row, 1, value_item)

            row += 1
          
class LoggerSubWindow(QMdiSubWindow):
    def __init__(self, snRef):
        super().__init__()
        self.setWindowTitle("Logger")
        self.setGeometry(200, 200, 300, 200)
        self.snRef = snRef

        layout = QVBoxLayout()

        self.start_logger_button = QPushButton("Start Logger", self)
        self.start_logger_button.clicked.connect(self.start_logger)
        layout.addWidget(self.start_logger_button)

        self.stop_logger_button = QPushButton("Stop Logger", self)
        self.stop_logger_button.clicked.connect(self.stop_logger)
        layout.addWidget(self.stop_logger_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setWidget(widget)
    
    def start_logger(self):
        self.snRef.set_name('stLogger',1)

    def stop_logger(self):
        self.snRef.set_name('stLogger',0)

class GraphSubWindow(QMainWindow):
    def __init__(self, snref):    
        super().__init__()

        self.snref = snref
        self.selected_signals_left = None
        ### RIGHT AXIS - self.selected_signals_right = None ## RIGHT AXIS
        self.plot_max = 1200

        self.setWindowTitle("Live Graph")
        self.setGeometry(100, 100, 800, 600)

        # Create a QWidget and set it as the central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create a vertical layout and add the Matplotlib canvas to it
        layout = QVBoxLayout(self.central_widget)

        # Create a horizontal layout to place widgets on the same line
        h_layout = QHBoxLayout()

        # Create a custom multi-select combo box
        self.multi_select_combo_leftaxis = MultiSelectComboBox(self.snref.get_all_names(), "Left Axis")
        h_layout.addWidget(self.multi_select_combo_leftaxis)

        # Create a ComboBox (drop-down box) for signal selection
        self.combo_box = QComboBox(self)
        self.combo_box.addItems(["1hz", "10hz"])  
        h_layout.addWidget(self.combo_box)

        ### RIGHT AXIS - self.multi_select_combo_rightaxis = MultiSelectComboBox(self.snref.get_all_names(), "Right Axis")
        ### RIGHT AXIS - h_layout.addWidget(self.multi_select_combo_rightaxis)

        # Create a button to print selected items
        self.print_button = QPushButton('Update', self)
        self.print_button.clicked.connect(self.on_signal_change)
        h_layout.addWidget(self.print_button)

        # Add the horizontal layout to the main vertical layout
        layout.addLayout(h_layout)

        # Create a Matplotlib figure and axis
        self.figure, self.ax1 = plt.subplots()
        self.ax1.tick_params('both', labelsize=10)
        ### RIGHT AXIS - self.ax2 = self.ax1.twinx()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Data for plotting
        self.x_data = []
        self.y_data_left = []
        ### RIGHT AXIS - self.y_data_right = []

        # Timers
        self.timer_data = QTimer()
        self.timer_data.setInterval(1000) 
        self.timer_data.timeout.connect(self.update_data)
        self.timer_data.start()

        self.timer_plot = QTimer()
        self.timer_plot.setInterval(1000) 
        self.timer_plot.timeout.connect(self.update_plot)
        self.timer_plot.start()

    def update_data(self):
        if self.selected_signals_left != None:
            self.x_data.append(time.time())

            if len(self.x_data) > self.plot_max:
                self.x_data.pop(0)

            self.new_data = []

            for signal in self.selected_signals_left:
                self.new_data.append(self.snref.get_name(signal))
            self.y_data_left = self.y_data_left + [self.new_data]

            if len(self.y_data_left) > self.plot_max:
                self.y_data_left.pop(0)

        ### RIGHT AXIS - if self.selected_signals_right != None:
        ### RIGHT AXIS -    self.new_data = []
        ### RIGHT AXIS -    for signal in self.selected_signals_right:
        ### RIGHT AXIS -        self.new_data.append(self.snref.get_name(signal))  # Random data
        ### RIGHT AXIS -    self.y_data_right = self.y_data_right + [self.new_data]

        ### RIGHT AXIS -    if len(self.y_data_right) > self.plot_max:
        ### RIGHT AXIS -        self.y_data_right.pop(0)

    def update_plot(self):
        if self.selected_signals_left != None:
            # Clear the axis and redraw the plot
            self.ax1.clear()
            self.ax1.plot(self.x_data, self.y_data_left, label=self.selected_signals_left)
            self.ax1.legend()
       
        ### RIGHT AXIS -    # Clear the axis and redraw the plot
        ### RIGHT AXIS -    self.ax2.clear()
        ### RIGHT AXIS -    self.ax2.plot(self.x_data, self.y_data_right, label=self.selected_signals_right)
        ### RIGHT AXIS -    self.ax2.legend()

        # Redraw the canvas
        self.canvas.draw()
    
    def on_signal_change(self):
        self.selected_signals_left = self.multi_select_combo_leftaxis.get_selected_items()
        ### RIGHT AXIS - self.selected_signals_right = self.multi_select_combo_rightaxis.get_selected_items()

        if self.selected_signals_left == []:
            self.selected_signals_left = None
        
        ### RIGHT AXIS - if self.selected_signals_right == []:
        ### RIGHT AXIS -     self.selected_signals_right = None

        if self.combo_box.currentText() == "1hz":
            self.timer_data.setInterval(1000) 
        if self.combo_box.currentText() == "10hz":
            self.timer_data.setInterval(100) 

        self.x_data = [] 
        self.y_data_left = []
        ### RIGHT AXIS - self.y_data_right = []
