import time
import datetime
import subprocess
import multiprocessing
import argparse
import TestConfig
import Configs
import ZfsApi
import Pid
import Common
import MonitorThread
import ReceiveThread
import Results

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action="store_true",
        help="The script will periodically print stats about TXGs and "
        " receive speed")
parser.add_argument('-t', '--threads', type=int, default=4,
        choices=xrange(1,32),
        help="The number of concurrent receives to perform")
args = parser.parse_args()

# Use TestConfig to ensure this computer is set up properly
TestConfig.check_all()
# This test case will use the test send file, check that it will work
TestConfig.check_testfile()

Pid.create_pid_file()

# Establish where this test will be writing its output
current_min = time.strftime("%Y%m%d%H%M%S")
zfs_receive_path = Configs.test_filesystem_path + '/runs/' + current_min

start_txg = ZfsApi.get_current_txg(Configs.main_pool)

results_collector = Results.ResultsCollector(zfs_receive_path)
results_collector.gather_start_results()

if args.verbose:
    monitor_thread = MonitorThread.MonitorThread(zfs_receive_path)
    monitor_thread.start()

# Create the base FS that each thread will be receiveing into sub filesystem
ZfsApi.create_filesystem(zfs_receive_path)

start_time = time.time()

def receive_file(zfs_filesystem):
    ZfsApi.zfs_recv(Configs.test_file_full_path, zfs_filesystem)

try:
    zfs_filesystem_list = []
    for count in xrange(args.threads):
        zfs_filesystem_list.append(zfs_receive_path + '/' + str(count))
    workerPool = multiprocessing.Pool(processes=args.threads)
    workerPool.map(receive_file, zfs_filesystem_list)
    workerPool.close()
    workerPool.join()
except KeyboardInterrupt:
    pass

end_time = time.time()

results_collector.gather_end_results()

end_txg = ZfsApi.get_current_txg(Configs.main_pool)

time_elapsed = end_time - start_time

print("that took " + str(datetime.timedelta(seconds=time_elapsed)))

elapsed_txgs = end_txg - start_txg
txgs_per_second = elapsed_txgs / time_elapsed

print("TXGs/second: " + str(txgs_per_second))

property_dictionary = ZfsApi.get_filesystem_properties(zfs_receive_path, ['used'])

used_in_bytes = property_dictionary["used"]
used_in_mebibytes = Common.bytes_to_mebibyte(used_in_bytes)

print("received " + str(used_in_bytes))

bytes_per_second = used_in_mebibytes / time_elapsed

print("Speed: " + str(bytes_per_second) + " MiB/s")

# Clean up the PID file to allow other runs
Pid.destroy_pid_file()

