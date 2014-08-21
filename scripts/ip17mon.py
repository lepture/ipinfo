# -*- coding: utf-8 -*-
# read 17mon ip

import sys

PY2 = sys.version_info[0] == 2

import socket
import struct

_unpack_V = lambda b: struct.unpack("<L", b)
_unpack_N = lambda b: struct.unpack(">L", b)
_unpack_C = lambda b: struct.unpack("B", b)

ip2int = lambda ipstr: struct.unpack('!I', socket.inet_aton(ipstr))[0]
int2ip = lambda n: socket.inet_ntoa(struct.pack('!I', n))
nip2int = lambda nipstr: struct.unpack('!I', nipstr)[0]
int2nip = lambda n: struct.pack('!I', n)


def read(filename):
    with open(filename, "rb") as f:
        dat = f.read()

    lines = []
    offset, = _unpack_N(dat[:4])
    max_comp_len = offset - 1028
    index = dat[4:offset]

    index_offset = index_length = 0
    start = 1024
    old_nip = socket.inet_aton('1.0.0.0')
    while start < max_comp_len:
        new_nip = index[start:start + 4]

        index_offset, = _unpack_V(
            index[start + 4:start + 7] + b'\0')
        if PY2:
            index_length, = _unpack_C(index[start + 7])
        else:
            index_length = index[start + 7]

        start += 8

        if index_offset == 0:
            old_nip = int2nip(nip2int(new_nip) + 1)
            continue

        res_offset = offset + index_offset - 1024
        desc = dat[res_offset:res_offset + index_length]
        line = '%s %s %s' % (
            socket.inet_ntoa(old_nip),
            socket.inet_ntoa(new_nip),
            desc.decode("utf-8").strip().encode("utf-8")
        )
        lines.append(','.join(line.split()))
        if (start < max_comp_len):
            old_nip = int2nip(nip2int(new_nip) + 1)

    return lines


lines = read('data/17monipdb.dat')
with open('data/17monip.txt', 'w') as f:
    f.write('\n'.join(lines))
