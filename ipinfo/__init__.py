# coding: utf-8
"""
    ipinfo
    ~~~~~~

    |4bit|255*4bit|data index|data block|
"""

import mmap
import socket
from struct import Struct
from collections import namedtuple

__all__ = ['IpInfo', 'Database']
__version__ = '0.1'

IpInfo = namedtuple('IpInfo', [
    'country', 'region', 'city', 'latitude', 'longitude'
])

unpack_long = Struct('>L').unpack
unpack_char = Struct('B').unpack


class Database(object):
    def __init__(self, filename):
        with open(filename, 'rb') as f:
            buf = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

        self._buf = buf

        index_count, = unpack_long(buf[:4])
        # index offset: index length + 4 + 1020(1-255) - 1
        self._offset = index_count * 8 + 1023

    def close(self):
        self._buf.close()

    def _lookup_ipv4(self, ip):
        nip = socket.inet_aton(ip)

        # first IP number
        fip = bytearray(nip)[0]
        # 4 + (fip - 1) * 4
        fip_offset = fip * 4

        # position in the index block
        count, = unpack_long(self._buf[fip_offset:fip_offset + 4])
        pos = count * 8

        offset = pos + 1024
        data_pos = None
        while offset < self._offset:
            endip = self._buf[offset:offset + 4]
            if nip <= endip:
                data_pos, = unpack_long(self._buf[offset + 4:offset + 8])
                break
            offset += 8

        if data_pos is None:
            return None

        ident = self._offset + data_pos + 1
        length, = unpack_char(self._buf[ident])
        buf = self._buf[ident+1:ident+1+length]
        return buf.decode('utf-8')

    def lookup(self, ip):
        value = self._lookup_ipv4(ip)
        if not value:
            return None
        values = value.split()
        length = len(values)
        if length > 5:
            values = values[:5]
        elif length < 5:
            values.extend([''] * (5 - length))
        return IpInfo(*values)
