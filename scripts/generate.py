# coding: utf-8

import sys
import socket
from struct import Struct

PY3 = sys.version_info[0] == 3
if PY3:
    bytes_type = bytes
else:
    bytes_type = str

pack_long = Struct('>L').pack
pack_char = Struct('B').pack


def first_ip(ip):
    nip = socket.inet_aton(ip)
    return bytearray(nip)[0]


def to_bytes(text, encoding='utf-8'):
    if not isinstance(text, bytes_type):
        text = text.encode(encoding)
    return text


def create_database(lines, filename):
    ip_index = {}
    data_index = []
    data_block = ''
    data_cache = {}

    latest_ip = 1
    for line in lines:
        start, end = line[0], line[1]

        text = '\t'.join(map(lambda b: b.strip(), line[2:]))
        text = to_bytes(text)
        if text not in data_cache:
            data_cache[text] = len(data_block)
            data_block += pack_char(len(text)) + text

        new_ip = max(first_ip(start), first_ip(end))
        if new_ip > latest_ip:
            ip_index[new_ip] = len(data_index)
            latest_ip = new_ip

        data_index.append((end, data_cache[text]))

    data = ''
    # data index length in bytes
    index_count = len(data_index)

    # track of data index length: 4bit
    data += pack_long(index_count)

    # track of ip index
    count = 1
    num = 0
    while count < 256:
        num = ip_index.get(count, num)
        data += pack_long(num)
        count += 1

    # track of data index
    for ip, offset in data_index:
        data += socket.inet_aton(ip) + pack_long(offset)

    data += data_block
    with open(filename, 'wb') as f:
        f.write(data)
    return data
