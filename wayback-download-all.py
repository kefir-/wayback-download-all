#!/usr/bin/env python3
import requests
import sys
import os
import urllib
import time
from collections import namedtuple

baseurl="http://web.archive.org/cdx/search/xd?url="
basedir = os.path.join(".","archive")

def help():
    print("Usage: {0} url".format(sys.argv[0]))
    sys.exit(1)


def setup():
    if not os.path.exists(basedir):
        os.makedirs(basedir)


def to_fs(s):
    return s.replace('/','_').replace(':','_')

def download(entry):

    url = urllib.parse.unquote(entry.url)
    ts = entry.ts
    if entry.http_status != "200":
        print("Skipping url with http status {0}: {1}".format(entry.http_status, url))
        return

    output = os.path.join(basedir, ts, to_fs(url))
    if os.path.exists(output):
        print("Skipping url, already downloaded:", url)
        return

    print("Fetching url {0}@{1} => {2}".format(url, ts, output))
    counter = 10
    while True:
        counter = counter - 1
        r = requests.get("http://web.archive.org/web/{0}id_/{1}".format(ts,entry.url))
        if r.status_code == 200:
            break
        else:
            if counter > 0:
                print("Warning: Got http error from archive.org, sleeping a bit:", r.status_code)
                time.sleep((10-counter) * 10)
                continue
            else:
                print("Error: archive.org returned error when downloading:", r.status_code)
                sys.exit(1)

    if not os.path.exists(os.path.dirname(output)):
        os.makedirs(os.path.dirname(output))
    with open(output, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)


def list_archive(url):
    r = requests.get(baseurl + url + "*")
    if r.status_code != 200:
        print("Error: archive.org returned status code:", r.status_code)
        sys.exit(1)

    Entry = namedtuple('Entry', 'id ts url mime http_status aid size')

    entries = []
    log = os.path.join(basedir, "all-entries.log")
    with open(log, "w") as f:
        for line in r.text.splitlines():
            # print("Got line:", line)
            print(line, file=f)
            entry=Entry._make(line.split())
            # print(repr(entry))
            entries.append(entry)

    return entries


def main():
    try:
        url=sys.argv[1]
    except IndexError:
        help()

    setup() 

    entries = list_archive(url)

    for entry in entries:
        download(entry)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Program interrupted by user.")
        sys.exit(1)

        
