from datetime import datetime
import time
import os
import datetime



class Logger():
    def __init__(self):
        self.month = time.gmtime(time.time()).tm_mon
        self.day = time.gmtime(time.time()).tm_mday
        self.year = time.gmtime(time.time()).tm_year
        self.min = time.gmtime(time.time()).tm_min
        self.hour = time.gmtime(time.time()).tm_hour
        self.logger_file_path = f"log-{self.month}-{self.day}-{self.year}--{self.hour}_{self.min}.txt"
        
        
    def trace(self, trace_data):
        local_files_lst = list(os.listdir('./Outputs'))
        print(self.logger_file_path)
        print(local_files_lst)
        if self.logger_file_path not in local_files_lst:
            print(self.logger_file_path in local_files_lst)
            with open(f"./OutPuts/{self.logger_file_path}", 'w') as file:
                run_start = datetime.datetime.now()
                file.write("--------------------New compialation-------------------\n")
                file.write(run_start.strftime("------------------%Y-%m-%d %H:%M:%S------------------\n"))
                file.write(trace_data)
        else:
            print(self.logger_file_path in local_files_lst)
            with open(f"./OutPuts/{self.logger_file_path}", 'a') as file:
                file.write(trace_data)  

        