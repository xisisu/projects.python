# http://www.tendcode.com/article/jiandan-meizi-spider/

import base64
import os
from functools import partial
from multiprocessing.pool import Pool

import requests
from bs4 import BeautifulSoup


def base64_decode(data):
  missing_padding = 4 - len(data) % 4
  if missing_padding:
    data += '=' * missing_padding
  return base64.b64decode(data)


def get_img_url(img_hash):
  img_hash = img_hash[4:]
  k = base64_decode(img_hash)
  url = k.decode('utf-8', errors='ignore')
  return 'http://w' + url


def parse_page_get_url(url):
  headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Host': 'jandan.net'
  }
  html = requests.get(url, headers=headers).text
  soup = BeautifulSoup(html, 'lxml')
  tags = soup.select('.img-hash')
  result = []
  for tag in tags:
    img_hash = tag.text
    result.append(get_img_url(img_hash))
  return result


def download_img(imgurl, dir):
  name = imgurl.split('/')[-1]
  file = "{}{}".format(dir, name)
  if os.path.exists(file):
    return
  try:
    item = requests.get(imgurl).content
    with open(file, 'wb') as f:
      f.write(item)
  except requests.exceptions.ConnectionError:
    print("Error downloading ", imgurl)


def process_page(page_url, dir):
  print('processing page: ', page_url)
  for img in parse_page_get_url(page_url):
    download_img(img, dir)


def run_parallel(start=1, end=212):
  pages = []
  for i in range(start, end):
    pages.append("http://jandan.net/pic/page-{}".format(i))
  p = Pool(processes=4)
  p.map(partial(process_page, dir='D:/Data/wuliao/'), pages)


def run_sequential(start=1, end=212):
  for i in range(start, end):
    page = "http://jandan.net/pic/page-{}".format(i)
    process_page(page_url=page, dir='D:/Data/wuliao/')


if __name__ == '__main__':
  # run_sequential(start=1, end=212)
  run_parallel(start=139, end=212)
