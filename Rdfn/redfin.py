import csv
import os
import shutil
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import selenium
from selenium import webdriver


def DownloadByZipcode(zipcode=None):
  driver = webdriver.Chrome('chromedriver.exe')
  driver.get('https://www.redfin.com/zipcode/' + zipcode)
  try:
    elem = driver.find_element_by_class_name('downloadLink')
    elem.click()
    time.sleep(5)
  except selenium.common.exceptions.NoSuchElementException:
    print('Cannot find download link for zipcode {}'.format(zipcode))
  driver.close()


def GetKnownZipcodes():
  known_zipcodes = set()
  for f in os.listdir('redfin_data'):
    reader = csv.DictReader(open(os.path.join('redfin_data', f), 'r'))
    for row in reader:
      zip = row['ZIP']
      known_zipcodes.add(zip)
      break
  return known_zipcodes


def DownloadRedFinAllZipCode():
  known_zipcodes = GetKnownZipcodes()

  reader = csv.DictReader(open('data/zipcodes.csv', 'r'))
  for row in reader:
    zipcode = row['zipcode']
    if zipcode in known_zipcodes:
      continue
    DownloadByZipcode(zipcode=zipcode)


def GetZipToCity():
  zip_to_city = {}
  reader = csv.DictReader(open('data/zipcodes.csv', 'r'))
  for row in reader:
    zip_to_city[row['zipcode']] = row['city']
  return zip_to_city


def MoveDownloadFiles():
  zip_to_city = GetZipToCity()

  download_dir = 'C:/Users/xisis/Downloads'
  for f in os.listdir(download_dir):
    if not f.startswith('redfin_2017-'):
      continue
    reader = csv.DictReader(open(os.path.join(download_dir, f), 'r'))
    for row in reader:
      zip = row['ZIP']
      city = zip_to_city[zip]
      break
    shutil.copy(os.path.join(download_dir, f), os.path.join('redfin_data', city + '_' + zip + '.csv'))


def GetAllData():
  list_ = []
  for f in os.listdir('redfin_data'):
    if not f.endswith('.csv'):
      continue
    temp = pd.read_csv(filepath_or_buffer=os.path.join('redfin_data', f), index_col=['MLS#'], dtype={'ZIP': np.str})
    list_.append(temp)
  df = pd.concat(list_)
  return df


def GetPreparedData():
  df = GetAllData()
  zip_to_city = GetZipToCity()
  # drop unwanted rows
  df.drop(['SOLD DATE', 'STATE', 'STATUS', 'NEXT OPEN HOUSE START TIME', 'NEXT OPEN HOUSE END TIME',
           'URL (SEE http://www.redfin.com/buy-a-home/comparative-market-analysis FOR INFO ON PRICING)',
           'SOURCE', 'FAVORITE', 'INTERESTED', 'ADDRESS', 'LOCATION', 'CITY'], axis=1, inplace=True)
  # drop unwated zipcodes
  drop_index = []
  for index, zip in df['ZIP'].iteritems():
    if zip not in zip_to_city:
      drop_index.append(index)
  df.drop(drop_index, inplace=True)

  df['PRICE'] = df['PRICE'] / 1000.0
  df['CITY'] = df['ZIP'].map(zip_to_city)  # add back city to be consistent
  df['TAG'] = df['CITY'] + '_' + df['ZIP']  # add tag column
  return df


def PlotInvenotry(df=None):
  fig = df['TAG'].value_counts().plot.barh(figsize=(20, 10))
  fig.set_xlabel('Inventory')
  fig.set_ylabel('City')
  fig.set_title('Inventory by Zip Code')
  fig.grid()
  plt.savefig('redfin_pic/inventory.png')
  plt.close('all')


def PlotDistribution(df=None, col=None, xlim=None):
  df2 = pd.DataFrame({c: vals[col] for c, vals in df.groupby('TAG')})
  median = df2.median().sort_values()
  fig = df2[median.index].boxplot(figsize=(20, 10), vert=False)
  fig.set_title('Distribution by ' + col)
  fig.set_xlabel(col)
  fig.set_ylabel('City')
  if xlim != None:
    plt.xlim(xlim)
  filename = col.replace(' ', '_').replace('$/', 'dollar_per_').lower()
  plt.savefig('redfin_pic/distribution_' + filename + '.png')
  plt.close('all')


def PlotInventoryByPropertyType(df=None, col=None):
  tags = df['TAG'].unique()
  property_type = df[col].unique()
  df_property_type = pd.DataFrame(index=tags)
  for p in property_type:
    df_property_type[p] = 0
  for tag in tags:
    tmp = df[df['TAG'] == tag]
    for k, v in tmp[col].value_counts().iteritems():
      df_property_type.loc[tag, k] = v
  fig = df_property_type.plot.barh(stacked=True, figsize=(20, 10))
  fig.set_xlabel('Inventory')
  fig.set_ylabel('City')
  fig.set_title('Inventory by ' + col)
  fig.grid()
  filename = col.replace(' ', '_').replace('$/', '').lower()
  plt.savefig('redfin_pic/inventory_' + filename + '.png')
  plt.close('all')


def GenerateAnalysisPlot():
  df = GetPreparedData()

  PlotDistribution(df=df, col='PRICE', xlim=[0, 1500])
  PlotDistribution(df=df, col='$/SQUARE FEET', xlim=[0, 1000])
  PlotDistribution(df=df, col='SQUARE FEET', xlim=[0, 3000])
  PlotDistribution(df=df, col='DAYS ON MARKET', xlim=[0, 180])
  PlotDistribution(df=df, col='YEAR BUILT', xlim=[1800, 2020])

  PlotInvenotry(df)
  PlotInventoryByPropertyType(df, col='PROPERTY TYPE')
  PlotInventoryByPropertyType(df, col='SALE TYPE')

  df2 = df.copy()
  col = 'BEDS'
  df2.dropna(subset=[col], inplace=True)
  df2[col] = df2[col].apply(lambda x: '<=2' if int(x) <= 2 else x)
  df2[col] = df2[col].apply(lambda x: '>=7' if isinstance(x, float) and int(x) >= 7 else x)
  PlotInventoryByPropertyType(df2, col=col)

  df2 = df.copy()
  col = 'BATHS'
  df2.dropna(subset=[col], inplace=True)
  df2[col] = df2[col].apply(lambda x: '>=3' if int(x) >= 3 else x)
  PlotInventoryByPropertyType(df2, col=col)

  df2 = df.copy()
  col = 'YEAR BUILT'
  df2.dropna(subset=[col], inplace=True)
  df2[col] = df2[col].apply(lambda x: '<= 1800' if int(x) <= 1800 else x)
  df2[col] = df2[col].apply(lambda x: '(1800,1900]' if isinstance(x, float) and int(x) <= 1900 else x)
  df2[col] = df2[col].apply(lambda x: '(1900,1950]' if isinstance(x, float) and int(x) <= 1950 else x)
  df2[col] = df2[col].apply(lambda x: '(1950,1975]' if isinstance(x, float) and int(x) <= 1975 else x)
  df2[col] = df2[col].apply(lambda x: '(1975,2000]' if isinstance(x, float) and int(x) <= 2000 else x)
  df2[col] = df2[col].apply(lambda x: '(2000,now]' if isinstance(x, float) and int(x) <= 3000 else x)
  PlotInventoryByPropertyType(df2, col=col)

  df2 = df.copy()
  col = 'SQUARE FEET'
  df2.dropna(subset=[col], inplace=True)
  df2[col] = df2[col].apply(lambda x: '<= 800' if int(x) <= 800 else x)
  df2[col] = df2[col].apply(lambda x: '(800,1500]' if isinstance(x, float) and int(x) <= 1500 else x)
  df2[col] = df2[col].apply(lambda x: '(1500,2000]' if isinstance(x, float) and int(x) <= 2000 else x)
  df2[col] = df2[col].apply(lambda x: '(2000,2500]' if isinstance(x, float) and int(x) <= 2500 else x)
  df2[col] = df2[col].apply(lambda x: '(2500,more]' if isinstance(x, float) else x)
  PlotInventoryByPropertyType(df2, col=col)

  df2 = df.copy()
  col = 'LOT SIZE'
  df2.dropna(subset=[col], inplace=True)
  df2[col] = df2[col].apply(lambda x: '<= 800' if int(x) <= 800 else x)
  df2[col] = df2[col].apply(lambda x: '(800,1500]' if isinstance(x, float) and int(x) <= 1500 else x)
  df2[col] = df2[col].apply(lambda x: '(1500,2000]' if isinstance(x, float) and int(x) <= 2000 else x)
  df2[col] = df2[col].apply(lambda x: '(2000,2500]' if isinstance(x, float) and int(x) <= 2500 else x)
  df2[col] = df2[col].apply(lambda x: '(2500,more]' if isinstance(x, float) else x)
  PlotInventoryByPropertyType(df2, col=col)

  df2 = df.copy()
  col = 'DAYS ON MARKET'
  df2.dropna(subset=[col], inplace=True)
  df2[col] = df2[col].apply(lambda x: '<= 7' if int(x) <= 7 else x)
  df2[col] = df2[col].apply(lambda x: '(5,14]' if isinstance(x, float) and int(x) <= 14 else x)
  df2[col] = df2[col].apply(lambda x: '(14,30]' if isinstance(x, float) and int(x) <= 30 else x)
  df2[col] = df2[col].apply(lambda x: '(30,60]' if isinstance(x, float) and int(x) <= 60 else x)
  df2[col] = df2[col].apply(lambda x: '(60,more]' if isinstance(x, float) else x)
  PlotInventoryByPropertyType(df2, col=col)

  df2 = df.copy()
  col = '$/SQUARE FEET'
  df2.dropna(subset=[col], inplace=True)
  df2[col] = df2[col].apply(lambda x: '<= 200' if int(x) <= 200 else x)
  df2[col] = df2[col].apply(lambda x: '(200,300]' if isinstance(x, float) and int(x) <= 300 else x)
  df2[col] = df2[col].apply(lambda x: '(300,400]' if isinstance(x, float) and int(x) <= 400 else x)
  df2[col] = df2[col].apply(lambda x: '(400,500]' if isinstance(x, float) and int(x) <= 500 else x)
  df2[col] = df2[col].apply(lambda x: '(500,more]' if isinstance(x, float) else x)
  PlotInventoryByPropertyType(df2, col=col)


def test():
  df = pd.DataFrame(np.random.rand(10, 4), columns=['a', 'b', 'c', 'd'])
  df.plot.bar(stacked=True)
  print(df)
  plt.show()


if __name__ == '__main__':
  # test()
  # DownloadRedFinAllZipCode()
  # MoveDownloadFiles()
  GenerateAnalysisPlot()
