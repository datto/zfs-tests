import time
import datetime
import subprocess
import multiprocessing
import TestConfig
import Configs
import ZfsApi
import Pid
import Common
import MonitorThread
import ReceiveThread
import Results

# Use TestConfig to ensure this computer is set up properly
TestConfig.check_all()
# This test case will use the test send file, check that it will work
TestConfig.check_testfile()

Pid.create_pid_file()

# Establish where this test will be writing its output
current_min = time.strftime("%Y%m%d%H%M%S")
zfs_receive_path = Configs.test_filesystem_path + '/runs/' + current_min

results_collector = Results.ResultsCollector(zfs_receive_path)
results_collector.gather_start_results()

monitor_thread = MonitorThread.MonitorThread(zfs_receive_path)
monitor_thread.start()

# Create the base FS that each thread will be receiveing into sub filesystem
ZfsApi.create_filesystem(zfs_receive_path)

start_time = time.time()

def receive_file(zfs_filesystem):
    print("receiving on " + zfs_filesystem)
    ZfsApi.zfs_recv(Configs.test_file_full_path, zfs_filesystem)

try:
    zfs_filesystem_list = [zfs_receive_path + "/1", zfs_receive_path + "/2", zfs_receive_path + "/3", zfs_receive_path + "/4"]
    workerPool = multiprocessing.Pool(processes = 4)
    workerPool.map(receive_file, zfs_filesystem_list)
    workerPool.close()
    workerPool.join()
except KeyboardInterrupt:
    pass

end_time = time.time()

results_collector.gather_end_results()

time_elapsed = end_time - start_time

print("that took " + str(datetime.timedelta(seconds=time_elapsed)))

property_dictionary = ZfsApi.get_filesystem_properties(zfs_receive_path, ['used'])

used_in_bytes = property_dictionary["used"]
used_in_mebibytes = Common.bytes_to_mebibyte(used_in_bytes)

print("received " + str(used_in_bytes))

bytes_per_second = used_in_mebibytes / time_elapsed

print("Speed: " + str(bytes_per_second) + " MiB/s")

# Clean up the PID file to allow other runs
Pid.destroy_pid_file()

