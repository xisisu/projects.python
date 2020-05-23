import json
import csv
import pprint
import pandas as pd 
import matplotlib as plt
import datetime
import numpy as np

CSV_FILE_NAME = 'output.csv'

def get_csv():
  with open('watch-history.json') as f:
    data = json.load(f)

  with open(CSV_FILE_NAME, 'w') as f:
    fieldnames = ['time', 'channel', 'title']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for item in data:
      res = dict()
      if 'subtitles' in item:
        for v in item['subtitles']:
          res['channel'] = v['name']
          break
      res['title'] = item['title']
      res['time'] = item['time'][:10]
      writer.writerow(res)

def parse_csv():
  df = pd.read_csv(CSV_FILE_NAME, index_col='time', parse_dates=True, infer_datetime_format=True)
  df = df.sort_values('time')
  print('time range:', df.index[0], ' to ', df.index[-1], 'total of ', len(df.index.unique()), ' days')
  print('total video:', df.shape[0], ', unique video:', len(df.title.unique()))
  print('unique channel:', len(df.channel.unique()))
  print('top videos:', df['title'].value_counts().head())
  print('top channels:', df['channel'].value_counts().head())

  fig = df.groupby('time').count()['title'].plot()
  fig.get_figure().savefig('by_date.png')

  df['year_month'] = df.index.strftime('%Y-%m')
  fig = df.groupby('year_month').count()['title'].plot()
  fig.get_figure().savefig('by_month.png')

if __name__ == '__main__':
  get_csv()
  parse_csv()
