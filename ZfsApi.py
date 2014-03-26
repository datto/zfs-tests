import subprocess
import os
# A collection of zfs calls that can be stubed out

def fs_exists(zfs_receive_path):
    """Check if a zfs Filesytem already exists"""
    devnull = open(os.devnull, 'w')
    try:
        subprocess.check_call(['zfs', 'get', 'name', zfs_receive_path],
                stdout=devnull, stderr=devnull)
    except subprocess.CalledProcessError:
        return False
    return True

