# coding: utf-8
"""
    ipcity.parser
    ~~~~~~~~~~~~~

    |4bit|255*4bit|index block|data block|
    --------------------------------------
"""

import mmap
import socket
from struct import Struct

unpack_long = Struct('>L').unpack
unpack_char = Struct('B').unpack


class Database(object):
    def __init__(self, filename):
        with open(filename, 'rb') as f:
            buf = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

        self._buf = buf
        # index offset: index length + 4 + 1020
        self._offset = unpack_long(buf[:4]) + 1024

    def close(self):
        self._buf.close()

    def _lookup_ipv4(self, ip):
        nip = socket.inet_aton(ip)

        # first IP number * 4
        # position in first index
        fip = bytearray(nip)[0] * 4

        # position in the index block
        pos = unpack_long(self._buf[fip:fip + 4])
        offset = pos + 1028
        # TODO
        return offset
