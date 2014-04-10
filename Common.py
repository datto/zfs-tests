def bytes_to_mebibyte(size_in_bytes):
    """Since the output of zfs get -p is in bytes, and disk read/write is often
    measures in mb/s, this function will allow easy translation"""
    size_in_mib = ((float)(size_in_bytes))/(1024*1024)
    return size_in_mib
