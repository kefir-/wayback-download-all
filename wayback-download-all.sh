#!/bin/bash

(
  ts=$(date +%Y%m%d%H%M%S)
  while read url; do
    echo url="$url";
    wayback_machine_downloader -e -l -t $ts "$url"
  done
)< <(echo http://www.friekaker.no/)
