import os
import sys
import Configs

# This class will quickly test if your machine is properly configured for
# these perf tests.

# TODO check that zfs is installed, perhaps get version

# Check that the user running this script has permissions to run zfs commands
# this is established by having read permissions on the /dev/zfs device 
if not os.access('/dev/zfs' ,os.R_OK):
    print("You do not have read permissions to /dev/zfs, can you run zfs"
        + " commands?")
    sys.exit(1)

# Check that the specified test file exists
if not os.path.isfile(Configs.test_file_full_path):
    print("The test file does not exits. It is set to " + 
        Configs.test_file_full_path + " please check config.cfg")
    sys.exit(1)

# Check that the specified test file is readable
if not os.access(Configs.test_file_full_path, os.R_OK):
    print("Cannot read the test file. It is set to " + 
         Configs.test_file_full_path + " please check config.cfg")
    sys.exit(1)

