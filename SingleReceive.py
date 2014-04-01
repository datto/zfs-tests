import time
import datetime
import subprocess
import TestConfig
import Configs
import ZfsApi
import Pid

Pid.create_pid_file()

# Establish where this test will be writing its output
current_min = time.strftime("%Y%m%d%H%M")
zfs_receive_path = Configs.test_filesystem_path + '/' + current_min

if ZfsApi.fs_exists(zfs_receive_path):
    print("Already exists!")

start_time = time.time()
ZfsApi.zfs_recv(Configs.test_file_full_path, zfs_receive_path)
end_time = time.time()

time_elapsed = end_time - start_time

print("that took " + str(datetime.timedelta(seconds=time_elapsed)))

# CLean up the PID file to allow other runs
Pid.destroy_pid_file()

