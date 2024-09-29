import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea, QAction
import sn, module_random, module_logger #Self made scripts
import threading
from windows import *

class MainWindow(QMainWindow):
    def __init__(self, snRef):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.time_last = 0

        self.mdi_area = QMdiArea()
        self.setCentralWidget(self.mdi_area)

        self.create_menu()
        self.sn = snRef

        # Initialize the status bar
        self.status_bar = self.statusBar()

        # Setup statistics tracking
        self.timer_stats = QTimer()
        self.timer_stats.setInterval(1000) 
        self.timer_stats.timeout.connect(self.statistics)
        self.timer_stats.start()

    def create_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')
        module_menu = menu_bar.addMenu('Modules')

        new_action = QAction('New', self)
        #new_action.triggered.connect(self.open_sub_window)
        file_menu.addAction(new_action)

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        action = QAction('SN', self)
        action.triggered.connect(self.open_sn_window)
        module_menu.addAction(action)

        action = QAction('Logger', self)
        action.triggered.connect(self.open_logger_window)
        module_menu.addAction(action)

        action = QAction('Graph', self)
        action.triggered.connect(self.open_graph_window)
        module_menu.addAction(action)

    def open_sn_window(self):
        sub_window = SNSubWindow(self.sn)
        self.mdi_area.addSubWindow(sub_window)
        sub_window.show()

    def open_logger_window(self):
        sub_window = LoggerSubWindow(self.sn)
        self.mdi_area.addSubWindow(sub_window)
        sub_window.show()

    def open_graph_window(self):
        sub_window = GraphSubWindow(self.sn)
        self.mdi_area.addSubWindow(sub_window)
        sub_window.show()

    def statistics(self):
        time_now = time.time()
        time_diff = round((time_now - self.time_last)*1000)/10
        self.sn.set_name('tiCycle', time_diff)
        if self.sn.get_name('stLogger') == 1:
            self.status_bar.showMessage(("Logger Running     Cycle Time: " + str(time_diff) + "ms"),1000)
        else:
            self.status_bar.showMessage(("Cycle Time: " + str(time_diff) + "ms"),1000)
        self.time_last = time_now 

class GUI_Main:
    def __init__(self):
        snRef = sn.SN()
        self.sn = snRef
        random_thread = threading.Thread(target=module_random.randomnumbers, args=(snRef,))
        random_thread.start()
        logger_thread = threading.Thread(target=module_logger.logger, args=(snRef,))
        logger_thread.start()
        self.run()

    def run(self):
        app = QApplication(sys.argv)
        main_window = MainWindow(self.sn)
        main_window.setGeometry(100, 100, 1400, 800)
        main_window.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    gui = GUI_Main()
