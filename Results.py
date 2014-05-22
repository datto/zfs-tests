"""
A class to track results of tests. It will track the filesystem that was
given to it during its creation. Current stats that it will track are:

-start time
-start TXG
-starting size
-zpool status
-zpool iostat -v
"""
import ZfsApi
import time
import Configs
import subprocess

class ResultsCollector():

    def log(self, message):
        self.log_file_handle.write(message + "\n")

    def __init__(self, filesystem):
        self.filesystem = filesystem
        # Since the filesystem was created with a uniqie name, we can simply
        # take the final part of its name (after the final /) and be given a
        # unique name for the log file.
        fs_name = filesystem[filesystem.rfind('/'):]
        self.logfile = Configs.results_directory +  fs_name

    def gather_start_results(self):
        self.log_file_handle = open(self.logfile, 'a')
        self.log("START")
        self.print_stats_to_file()
        self.log_file_handle.close()

    def gather_end_results(self):
        self.log_file_handle = open(self.logfile, 'a')
        self.log("END")
        self.print_stats_to_file()
        self.log_file_handle.close()

    def print_stats_to_file(self):
        """Since the stats collected at the begingng and end of a run are the
        same, they can be collapsed into a single function"""
        current_time = time.time()
        self.log("time: " + str(current_time))
        current_txg = ZfsApi.get_current_txg(Configs.main_pool)
        self.log("TXG: " + current_txg)
        # If the filesystem does not exist, its size is 0.
        if ZfsApi.fs_exists(self.filesystem):
            current_size = ZfsApi.get_filesystem_size(self.filesystem)
            self.log("size: " + str(current_size))
        else:
            self.log("size: 0")
        self.log("zpool iostat -v:")
        self.log(subprocess.check_output(['zpool', 'iostat', '-v']))
        self.log("zpool status:")
        self.log(subprocess.check_output(['zpool', 'status']))

