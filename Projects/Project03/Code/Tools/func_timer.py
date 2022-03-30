import time
import logging

save_log_path = ".\\Outputs\\TimeAnaylisis\\"
logging.basicConfig(filename=f"{save_log_path}loginfo.log", filemode='w', level=logging.INFO)

def timer(func):
    def timerwrapper(*args, **kwargs):
        time_strt = time.time()
        time_stp = time.time()
        print(f"--- {func.__name__}() ---")
        print(f"\t[Execute Start:\t\t{time.gmtime(time_strt).tm_hour}:{time.gmtime(time_strt).tm_min}:{time.gmtime(time_strt).tm_sec}]")
        print(f"\t[Execute Start:\t\t{time.gmtime(time_stp).tm_hour}:{time.gmtime(time_stp).tm_min}:{time.gmtime(time_stp).tm_sec}]")
        print(f"\t[Overall Execution: {(time_stp - time_strt) / 60 :3.5} (Mins)]".format())
        try:
            logging.info(f"Function:  {func.__name__}()")
            logging.info(f"\t\t[Execute Start:\t\t{time.gmtime(time_strt).tm_hour}:{time.gmtime(time_strt).tm_min}:{time.gmtime(time_strt).tm_sec}]")
            logging.info(f"\t\t[Execute Start:\t\t{time.gmtime(time_stp).tm_hour}:{time.gmtime(time_stp).tm_min}:{time.gmtime(time_stp).tm_sec}]")
            logging.info(f"\t\t[Overall Execution: {(time_stp - time_strt)}]".format())
            # logging.info(f"\t[Overall Execution: {(time_stp - time_strt) / 60 :3.5} (Mins)]".format())
        except:
            print("No logged info")
        return None
    return timerwrapper