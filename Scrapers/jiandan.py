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
  item = requests.get(imgurl).content
  with open(file, 'wb') as f:
    f.write(item)


def process_page(page_url, dir):
  print('processing page: ', page_url)
  for img in parse_page_get_url(page_url):
    download_img(img, dir)


if __name__ == '__main__':
  pages = []
  for i in range(1, 44):
    pages.append("http://jandan.net/ooxx/page-{}".format(i))
  p = Pool(processes=4)
  p.map(partial(process_page, dir='D:/Data/jiandan/'), pages)
