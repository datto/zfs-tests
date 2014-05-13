"""
A class to track results of tests. It will track the filesystem that was
given to it during its creation. Current stats that it will track are:

BEGIN
-start time
-start TXG
-starting size
-zpool iostat -v

END
-end TXG
-end time
-ending size (note, will not help in the case of deletions, record it anyways)
-zpool iostat -v
"""
import ZfsApi
import time
import Configs

class ResultsCollector():

    def log(self, log_file_handle, message):
        log_file_handle.write(message + "\n")

    def __init__(self, filesystem):
        self.filesystem = filesystem
        # Since the filesystem was created with a uniqie name, we can simply
        # take the final part of its name (after the final /) and be given a
        # unique name for the log file.
        fs_name = filesystem[filesystem.rfind('/'):]
        self.logfile = Configs.results_directory +  fs_name
        print("log file is " + self.logfile)

    def gather_start_results(self):
        log_file_handle = open(self.logfile, 'a')
        current_time = time.time()
        self.log(log_file_handle, "start time: " + str(current_time))
        current_txg = ZfsApi.get_current_txg(Configs.main_pool)
        self.log(log_file_handle, "start TXG: " + current_txg)
        current_size = ZfsApi.get_filesystem_size(self.filesystem)
        self.log(log_file_handle, "start size: " + str(current_size))
        log_file_handle.close()

    def gather_end_results():
        print(hello)
