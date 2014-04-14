import threading
import time
import ZfsApi
import Common
'''
This class will monitor the size of a zfs filesytem, and report the size
progress over time
'''

class MonitorThread(threading.Thread):
    def __init__(self, filesystem):
        threading.Thread.__init__(self)
        self.daemon = True
        self.filesystem = filesystem

    def run(self):
        # Wait for the filesystem that is being monitored to exist.
        while not ZfsApi.fs_exists(self.filesystem):
            time.sleep(1)
        start_time = time.time()
        start_size = ZfsApi.get_filesystem_size(self.filesystem)
        while True:
            time.sleep(1)
            current_size = ZfsApi.get_filesystem_size(self.filesystem)
            size_diff = current_size - start_size
            size_diff_in_mib = Common.bytes_to_mebibyte(size_diff)
            current_time = time.time()
            time_diff = current_time - start_time
            mib_per_second = size_diff_in_mib / time_diff
            print("Average speed: " + str(mib_per_second) + " mib/sec")

