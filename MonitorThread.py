import threading
import time
import ZfsApi
import Common
import MovingAverage
'''
This class will monitor the size of a zfs filesytem, and report the size
progress over time
'''

class MonitorThread(threading.Thread):
    def __init__(self, filesystem):
        threading.Thread.__init__(self)
        self.daemon = True
        self.filesystem = filesystem
        self.ma = MovingAverage.moving_average([5, 15, 30])

    def run(self):
        # Wait for the filesystem that is being monitored to exist.
        while not ZfsApi.fs_exists(self.filesystem):
            time.sleep(1)
        while True:
            time.sleep(1)
            self.ma.insert_value(ZfsApi.get_filesystem_size(self.filesystem))
            result_string = ""
            for size_delta,diff in self.ma.get_diffs():
                size_diff_in_bytes = float(diff)/size_delta
                size_diff_in_mib = Common.bytes_to_mebibyte(size_diff_in_bytes)
                reasonable_string = '%.3f' % size_diff_in_mib
                result_string = result_string + reasonable_string.rjust(9)
            print("Average speed in mib/sec")
            print(result_string)

