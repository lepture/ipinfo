# coding: utf-8
"""
    ipinfo
    ~~~~~~
"""

import mmap
import socket
from struct import Struct
from collections import namedtuple

__all__ = ['Info', 'IPv4Database']
__version__ = '0.1'

Info = namedtuple('Info', [
    'country', 'region', 'city', 'latitude', 'longitude'
])

unpack_long = lambda n: Struct('>L').unpack(n)[0]
unpack_char = lambda n: Struct('B').unpack(n)[0]


class IPv4Database(object):
    """Database for search IPv4 address.

    Bytes in the dat file::

        ----------
        |  4bit  |        <- [count] (n)
        --------------
        | 256 * 4bit |    <- [first ip index]
        --------------
        |  n * 8bit  |    <- [ip index]
        --------------
        | data block |    <- [data]
        --------------
    """
    def __init__(self, filename):
        with open(filename, 'rb') as f:
            buf = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

        self._buf = buf

        index_count = unpack_long(buf[:4])
        # index offset: index length + 4 + 1024(1-256) - 1
        self._offset = index_count * 8 + 1027

    def close(self):
        self._buf.close()

    def _lookup_ipv4(self, ip):
        nip = socket.inet_aton(ip)

        # first IP number
        fip = bytearray(nip)[0]
        # 4 + (fip - 1) * 4
        fip_offset = fip * 4

        # position in the index block
        count = unpack_long(self._buf[fip_offset:fip_offset + 4])
        pos = count * 8

        offset = pos + 1028
        data_pos = None
        while offset < self._offset:
            endip = self._buf[offset:offset + 4]
            if nip <= endip:
                data_pos = unpack_long(self._buf[offset + 4:offset + 8])
                break
            offset += 8

        if not data_pos:
            # None or 0
            return None

        ident = self._offset + data_pos + 1
        length = unpack_char(self._buf[ident])
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
        return Info(*values)
