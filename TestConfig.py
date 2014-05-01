import os
import sys
import subprocess
import Configs
import ZfsApi

# This class will quickly test if your machine is properly configured for
# these perf tests.

# TODO check that zfs is installed, perhaps get version
def check_all():
    permissions_check()
    check_filesystems()

def permissions_check():
    # Check that the calling user has permissions to run zfs commands this is
    # established by having read permissions on the /dev/zfs device
    if not os.access('/dev/zfs' ,os.R_OK):
        print("You do not have read permissions to /dev/zfs, can you run zfs"
            + " commands?")
        sys.exit(1)

def check_filesystems():
    # Check that the area we are going to be working in exists. If it does not
    # offer to set it up for the user.
    if not os.path.isdir(Configs.mount_point):
        print("Could not find the pref_tests directory " +
                Configs.mount_point)
        result = raw_input("Create it? [Y/n] ")
        if result == "Y":
            setup_system()
        else:
            print("Exiting tests")
            sys.exit(1)

def setup_system():
    # This function will setup the zfs filesystems, it does not perform
    # any checks, call it when you know this machine needs to be set up
    subprocess.check_call(['zfs', 'create', '-p',
        Configs.test_filesystem_path,
        '-o', "mountpoint=" + Configs.mount_point])
    # Create the corpus directory, currently setting primarycahce=none
    # since not doing so results in abnormalities in test timing. I
    # think this will become especially useful when this process
    # becomes multithreaded.
    subprocess.check_call(['zfs', 'create',
        Configs.test_filesystem_path + '/corpus',
        '-o', 'primarycache=none'])
    # Create the area for test runs to go. I keep this in a separate
    # area to ensure that cleanup is easy
    ZfsApi.create_filesystem(Configs.test_filesystem_path + '/runs')

def check_testfile():
    '''Perfomr tests to ensure the test file will be usable'''
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

