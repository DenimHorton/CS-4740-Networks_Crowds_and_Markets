import time, os
import logging

save_log_path = ".\\Outputs\\"

if not os.path.exists(save_log_path):
    os.makedirs(save_log_path)
    
logging.basicConfig(filename=f"{save_log_path}loginfo.log", filemode='w', level=logging.INFO)

def recursiveMethodTester(func, num_calls = 5000):
    def timerwrapper(*args, **kwargs):
        time_strt = time.time()
        logging.info(f"Function:  {func.__name__}()")
        logging.info(f"\t\t[Execute Start:\t\t{time.gmtime(time_strt).tm_hour}:{time.gmtime(time_strt).tm_min}:{time.gmtime(time_strt).tm_sec}]")
        for recursive_cal in range(num_calls):
            result = func(*args, **kwargs)
        time_stp = time.time()
        logging.info(f"\t\t[Execute Stop:\t\t{time.gmtime(time_stp).tm_hour}:{time.gmtime(time_stp).tm_min}:{time.gmtime(time_stp).tm_sec}]")
        timeDiff = (time_stp - time_strt)
        logging.info(f"\t\t[Overall Execution: {timeDiff:.3f}  Sec ({timeDiff / 100000:.8f} Micro Sec )]")
        return result
    return timerwrapper