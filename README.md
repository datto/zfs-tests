zfs-tests
=========

An attempt at making a broadly applicable zfs test suite

##Requires:
* zfs
* python2.7

The main script to run is [MultiReceive.py](./MultiReceive.py). 
The first time you run this on a machine it should walk you through configuring
these tests to fit your environment.
PROTIP: you will probably have to change main_pool in [config.cfg](./config.cfg)

MultiReceive takes two arguments: verbosity and threadcount. When run with no
arguments it defaults to silent and 4 threads. Verbosity is a boolean flag, when
present the receiving filesystem is continuously monitored for speed. The thread
count parameter requires an integer between 1 and 32. This upper limit is
arbitrary, and can be increased if someone sees a need. The lower limit is there
as a sanity check.

##Consistency

One of the first things we were concerned about with ZFS performance testing was
consistency. These tests  produce consistent results, here are 7 runs of the
default settings with a 200GB sendfile
```bash
for i in {1..8}; do python2.7 MultiReceive.py; done
Speed: 129.370693668 MiB/s
Speed: 127.831824486 MiB/s
Speed: 126.817502308 MiB/s
Speed: 126.879119935 MiB/s
Speed: 126.032755742 MiB/s
Speed: 124.877744597 MiB/s
Speed: 123.970860591 MiB/s
```
We get consistent results by ignoring the ARC, setting primarycache=none. If you
want to test changes related to the ARC, you can unset this, but you need to be
aware of how it will affect performance.

Discussed further in the threads section, note that for the default settings
with a 200GB sendfile, 800GB of data is read from the disks, and 800GB of data
is written to the disks.

##Sendfiles

###Location

These tests measure the receiving of zfs sendfiles. You will need to
provide a source zfs sendfile for this program to work with. Its location is
determined by the test_file configurable. I most often keep it in
/opt/zfs_perf_tests/corpus/ as a symlink, then back that symlink with multiple
sendfiles of varying size
```bash
ls -1 /opt/zfs_perf_tests/corpus/
152G.zfs
16G.zfs
5GB.zfs
800M.zfs
sendfile.zfs -> 800M.zfs
```
###Storage
For my use case, I host the sendfiles on the zfs filesystem being tested. This
means the same zfs filesystem is serving reads and receiving the writes.

Using the symlink method you could easily link to a file hosted on another
filesystem, an entirely different medium (ramdisk for example), or an entirely
separate computer. Using a ramdisk would test the pure speed of the ZFS receive.
If you just want to measure write performance, I recommend
[fio](http://manpages.ubuntu.com/manpages/natty/man1/fio.1.html).

###Creation of sendfiles

The best sendfile you can have is one that represents the workload of your
particular use case. Will your server be receiving sendfiles representing users
home directories? Virtual machine images? Databases? Make a filesystem and load
it up with what you think your production workload will look like, and create a
sendfile out of that.

However sometimes you want a large sendfile without transferring it over the
network. In cases like this you will need to create a sendfile locally and
receive from that. For a generally interesting sendfile, I run fio creating and
recreating a 10GB random file and continually snapshot the file system they are
writing into.


##Threads and speed

The number of threads you choose to run does change the overall speed of the
tests. Here are some samples from a machine we used for testing:

threads| speed in MiB/s | TXGs/s
-------|----------------:|---------
1 |43.53  |.57
2 |77.75 |.74
3 |105.82 |.74
4 |127.06 |.77
5 |~130.00 |.85
6 |~105.00 |.90
7 |~~100.00  |.90
8 |~~105.00  |.90

As noted above, in my setup the zpool is both serving the reads for the
sendfiles, as well as writing them to disk. This means that for every thread you
can imagine two separate streams, one read and one write. Thie server I ran these
tests on starts slowing down and begins becomes very
inconsistent with 7 threads (so 14 disk streams). This metric can be helpful in
two ways: first it shows that you probably cannot sustain 14 read/write streams
on this machine in its current config, which may be a helpful metric to know.
Secondly you could remake the pool with a different VDEV configuration and see
how that changes the optimal thread count.

