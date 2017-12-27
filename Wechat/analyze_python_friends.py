import itchat
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import pandas as pd
import re
from wordcloud import WordCloud, ImageColorGenerator
import PIL.Image as Image
import jieba
from matplotlib.font_manager import FontProperties

def __GetOutputDir():
  return 'data'


def GetFriends():
  itchat.auto_login()
  return itchat.get_friends(update=True)

def GetSex(sex):
  if sex == 1:
    return "Male"
  elif sex == 2:
    return 'Female'
  else:
    return 'Other'

def GetDataFrame(friends=None):
  output = os.path.join(__GetOutputDir(), 'friends.csv')
  if os.path.exists(output):
    return pd.read_csv(output, parse_dates=False, index_col=['Num'])

  features = []
  for f in friends:
    feature = {
      'UserName' : f['UserName'],
      'NickName' : f['NickName'],
      'Sex' : GetSex(f['Sex']),
      'City' : f['City'],
      'Province' : f['Province'],
      'Signature' : f['Signature']
    }
    features.append(feature)
  df = pd.DataFrame(features)
  df.index.names = ['Num']
  df.to_csv(os.path.join(__GetOutputDir(), 'friends.csv'))
  return df


def PlotSignature(df=None):
  sig_list = []
  for signature in df['Signature']:
    signature = str(signature).strip()
    for w in ['span', 'class', 'emoji', 'nan', '\"', '!', '~', ',', '！', '。', '，', '#', '～', '“', '”']:
      signature = signature.replace(w, '')
    signature = re.compile('1f\d+\w*|[<>/=]').sub('', signature)
    if (len(signature) > 0):
      sig_list.append(signature)
  text = ' '.join(sig_list)

  word_list = jieba.cut(text, cut_all=True)
  words = ' '.join(word_list)

  coloring = np.array(Image.open('data/color.jpg'))
  wc = WordCloud(background_color='white', max_words=2000, mask=coloring, max_font_size=60, random_state=42,
                 font_path='data/DroidSansFallbackFull.ttf', scale=2).generate(words)
  image_color = ImageColorGenerator(coloring)
  plt.figure(figsize=(32, 16))
  plt.imshow(wc.recolor(color_func=image_color))
  plt.imshow(wc)
  plt.axis('off')
  plt.show()

def run():
  # friends = GetFriends()
  # df = GetDataFrame(friends)
  df = GetDataFrame()
  PlotSignature(df)

if __name__ == '__main__':
  run()
