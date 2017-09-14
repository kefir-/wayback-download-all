#!/usr/bin/env python3
import requests
import sys

baseurl="http://web.archive.org/cdx/search/xd?url="

def help():
    print("Usage: {0} url".format(sys.argv[0]))
    sys.exit(1)

def main():
    try:
        url=sys.argv[1]
    except IndexError:
        help()

    r = requests.get(baseurl + url + "*")
    if r.status_code != 200:
        print("Error: archive.org returned status code:", r.status_code)
        sys.exit(1)

    for line in r.text.splitlines():
        print("Got line:", line)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Program interrupted by user.")
        sys.exit(1)

        
