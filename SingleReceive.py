import time
import datetime
import subprocess
import TestConfig
import Configs
import ZfsApi
import Pid
import Common

Pid.create_pid_file()

# Establish where this test will be writing its output
current_min = time.strftime("%Y%m%d%H%M%S")
zfs_receive_path = Configs.test_filesystem_path + '/runs/' + current_min

start_time = time.time()
try:
    ZfsApi.zfs_recv(Configs.test_file_full_path, zfs_receive_path)
except KeyboardInterrupt:
    pass

end_time = time.time()

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

