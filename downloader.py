#!/usr/bin/python3

import requests, os, sys
from time import sleep

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
def download(url):
    try:
        filename = url.split('/')[-1]
        if filename in os.listdir():
            s = os.stat(filename)
            if s.st_size:
                pass
            else:
                # print(f'resuming {filename} at {s.st_size} bytes')
                file = open(filename, 'ab')
                resume_header = {'Range': f'bytes={os.stat(filename).st_size}-'}
                data = requests.get(url, stream=True, headers=resume_header)
                file.write(data.content)
                file.close()
        else:
            file = open(filename, 'wb')
            data = requests.get(url)
            file.write(data.content)
            file.close()
    except KeyboardInterrupt:
        sleep(1)
        sys.exit()
