import threading
import ZfsApi
"""This thread should receive a zfs sendfile into a zfs file system"""

class ReceiveThread(threading.Thread):
    def __init__(self, filesystem, sendfile):
        threading.Thread.__init__(self)
        self.filesystem = filesystem
        self.sendfile = sendfile

    def run(self):
        ZfsApi.zfs_recv(self.sendfile, self.filesystem)
