import threading
import time
import ZfsApi
import Common
import MovingAverage
'''
This class will monitor the size of a zfs filesytem, and report the size
progress over time. It also reports the TXGs/time.
'''

class MonitorThread(threading.Thread):
    def __init__(self, filesystem):
        threading.Thread.__init__(self)
        self.daemon = True
        self.filesystem = filesystem
        self.size_ma = MovingAverage.moving_average([5, 15, 30])
        self.poolname = ZfsApi.get_pool_name_for_fs(self.filesystem)
        self.txg_ma = MovingAverage.moving_average([5, 15, 30])

    def run(self):
        # Wait for the filesystem that is being monitored to exist.
        while not ZfsApi.fs_exists(self.filesystem):
            time.sleep(1)
        while True:
            time.sleep(1)
            self.txg_ma.insert_value(ZfsApi.linux_get_current_txg(self.poolname))
            txg_result_string = ""
            for txg_delta,diff in self.txg_ma.get_diffs():
                txg_diff = float(diff)/txg_delta
                reasonable_string = '%.3f' % txg_diff
                txg_result_string = txg_result_string + reasonable_string.rjust(9)
            print("TXGs per second, should be .200")
            print(txg_result_string)
            self.size_ma.insert_value(ZfsApi.get_filesystem_size(self.filesystem))
            result_string = ""
            for size_delta,diff in self.size_ma.get_diffs():
                size_diff_in_bytes = float(diff)/size_delta
                size_diff_in_mib = Common.bytes_to_mebibyte(size_diff_in_bytes)
                reasonable_string = '%.3f' % size_diff_in_mib
                result_string = result_string + reasonable_string.rjust(9)
            print("Average speed in mib/sec")
            print(result_string)

