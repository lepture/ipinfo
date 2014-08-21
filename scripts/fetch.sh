#!/usr/bin/env bash

ip17mon="http://s.qdcdn.com/17mon/17monipdb.zip"
geoip="http://geolite.maxmind.com/download/geoip/database/GeoLiteCity_CSV/GeoLiteCity-latest.zip"
region="http://www.maxmind.com/download/geoip/misc/region_codes.csv"

mkdir -p data
cd data

case "$1" in
    download)
        #curl $ip17mon -o ip17mon.zip
        #curl $geoip -o geoip.zip
        curl $region -o regions.csv
        ;;
    unzip)
        unzip ip17mon.zip
        unzip geoip.zip
        mv Geo*/*.csv ./
        ;;
    encode)
        iconv -f LATIN1 -t UTF8 GeoLiteCity-Location.csv > Location.csv
        iconv -f LATIN1 -t UTF8 GeoLiteCity-Blocks.csv > Blocks.csv
        ;;
    *)
        ;;
esac
