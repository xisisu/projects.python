# https://github.com/mepeichun/six_nine/blob/master/six_nine.py

import pygame


# array is a 2d boolean array
def text_to_pixel(string, width=140, height=30):
  pygame.init()
  font = pygame.font.SysFont('msyh.ttc', 50)
  rtext = font.render(string, True, (0, 0, 0), (255, 255, 255))
  array = pygame.surfarray.array2d(pygame.transform.scale(rtext, (width, height))) > 200
  return zip(*array)


def matrix_to_symbol(array):
  result = ''
  for row in array:
    cur = ''.join('6' if val else '9' for val in row)
    result += cur
    result += '<br />'
    result += '\n'
  return result


def generate_html(from_person, to_person, words, title):
  html = open('template.html', encoding='utf-8').read()
  array = matrix_to_symbol(text_to_pixel(words))

  html = html.replace('Your_name', from_person).replace('Somebody', to_person).replace(
    'Generate text and fill in here!', array).replace('Replace title here', title)

  with open('main.html', 'w', encoding='utf-8') as f:
    f.write(html)


def run():
  generate_html(from_person='Sisu', to_person='Elva', words='I Love You', title='Chou pi lu')


if __name__ == '__main__':
  run()
