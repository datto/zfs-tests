import sys
import subprocess
import Configs
import Pid
import TestConfig

TestConfig.permissions_check()

# While zfs destroy is not as taxing as zfs receive, I think that while this
# (potentially large) number of destorys is occuring, we should not allow the
# user to run any other perf tests.
# If we want to test the effect of multiple destroys on receive speed, we can
# work that into the multithread test.

Pid.create_pid_file()

runs_directory = Configs.test_filesystem_path + '/runs'

subprocess.check_call(['zfs', 'destroy', '-r', runs_directory])

subprocess.check_call(['zfs', 'create', 
    Configs.test_filesystem_path + '/runs'])

Pid.destroy_pid_file()

