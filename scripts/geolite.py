# coding: utf-8

import csv
import ipaddress


def read_region(filename):
    regions = {}
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            country = row[0]
            if country not in regions:
                regions[country] = {}
            regions[country][str(row[1])] = row[2]
    return regions


def read_location(filename, regions):
    locs = {}
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                country = row[1]
                region = row[2]
                if region:
                    region = regions[country][region]
                locs[int(row[0])] = ','.join([
                    country, region, row[3], row[5], row[6]
                ])
            except:
                pass
    return locs


def read_blocks(filename, locs):
    ips = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                loc = locs[int(row[2])]
                start = ipaddress.IPv4Address(int(row[0]))
                end = ipaddress.IPv4Address(int(row[1]))
                ips.append('%s,%s,%s' % (str(start), str(end), loc))
            except:
                pass
    return ips


regions = read_region('data/regions.csv')
locs = read_location('data/Location.csv', regions)
ips = read_blocks('data/Blocks.csv', locs)
with open('data/geoip.txt', 'w') as f:
    f.write('\n'.join(ips))
