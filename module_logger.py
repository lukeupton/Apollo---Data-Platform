import csv
import os
from datetime import datetime, timedelta
from time import sleep

class logger():
    def __init__(self, ref_sn) -> None:
        self.sn = ref_sn
        self.log_frequency = 10 #hz
        self.log_file_name = ""
        self.log_file_new = True
        self.log_file_size_max = 1000 #kb
        self.log_data()
        
    def get_all_names(self):
        self.names_dict = self.sn.names_dict

    def get_datetime(self):
        self.current_datetime = datetime.now()

    def create_new_logfile(self):
        # Get the date and time for the log file name
        self.get_datetime()
        self.log_file_name = os.path.join("data", self.current_datetime.strftime("%Y%m%d%H%M%S") + '.csv')

        #Build the headers from the existing SN list
        self.get_all_names()
        headers = list(self.names_dict.keys())
        headers.insert(0, "DateTime")

        with open(self.log_file_name, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(headers)
        
    def write_line_of_data(self):
        self.get_all_names()
        self.get_datetime()
        new_data = list(self.names_dict.values())
        new_data.insert(0, str(self.current_datetime.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]))
        
        with open(self.log_file_name, 'a', newline='') as csvfile:
            # Create a CSV writer object
            csv_writer = csv.writer(csvfile)
            
            # Write the new data to the CSV file
            csv_writer.writerow(new_data)

    def log_data(self):
        while True:
            if self.sn.get_name('stLogger') == 1:
                if self.log_file_name == "" or self.log_file_new == True:
                    self.create_new_logfile()
                    self.get_datetime()
                    t1 = self.current_datetime.utcnow()
                    t2 = self.current_datetime.utcnow()
                    self.log_file_new = False
                else:
                    if (t2-t1) > timedelta(seconds=1/self.log_frequency):
                        self.write_line_of_data()
                        self.get_datetime()
                        t1 = self.current_datetime
                    else:
                        sleep(0.001)
                        self.get_datetime()
                        t2 = self.current_datetime

                # File size manager 
                file_size_kbytes = os.path.getsize(self.log_file_name) /1024
                if file_size_kbytes >= self.log_file_size_max:
                    self.log_file_new = True
            else:
                self.log_file_new = True
                sleep(1)
            







