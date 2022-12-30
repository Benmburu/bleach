#!/usr/bin/python

from lxml import html
import requests, os, argparse, sys
from downloader import download
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('chapters', type=str, nargs='+')
args = parser.parse_args()

def extract(chapter):
    url = 'https://ww3.readbleachmanga.com/chapter/bleach-digital-colored-comics-chapter-686/'
    page = requests.get(url)
    tree = html.fromstring(page.content)
    manga = tree.xpath('//select/option/@value')[-chapter]
    page = requests.get(manga)
    tree = html.fromstring(page.content)

    pics = tree.xpath('//div[@class="text-center"]/img/@src')
    manga = tree.xpath('//div[@class="container px-3 mx-auto"]/h1/text()')[0].replace("/", " ")
    try:
        os.mkdir(manga)
    except FileExistsError:
        pass

    print(manga)
    path = os.getcwd()
    os.chdir(manga)

    for url in tqdm(pics, ascii=True):
        download(url.strip('\r'))

    os.chdir(path)

for chapter in args.chapters:
    if '-' in chapter:
        ranges = [int(i) for i in chapter.split('-')]
        if len(ranges) > 2:
            sys.exit('Invalid Range')
        else:
            for i in range(ranges[0], ranges[1]+1):
                extract(i)
    else:
        extract(int(chapter))
