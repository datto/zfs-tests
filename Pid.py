import os

# Functions to help with PID managmnet, we will use PID files to ensure only
# one instance of the tests are running at a time.

pid_file_path = '/var/run/zfs_perf_test.pid'

def create_pid_file():
    pid = os.getpid()
    pid_file_object = open(pid_file_path, 'w')
    pid_file_object.write(str(pid))
    pid_file_object.close()

def destroy_pid_file():
    os.unlink(pid_file_path)

def pid_file_exists():
    return os.path.exists(pid_file_path)

