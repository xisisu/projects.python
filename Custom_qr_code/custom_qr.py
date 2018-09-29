# https://www.shiyanlou.com/courses/370/labs/1191/document

import argparse

from MyQR import myqr


def run():
  parser = argparse.ArgumentParser(description='Custom QR code.')
  parser.add_argument('-i', '--input', type=str, default='elva.gif')
  parser.add_argument('-o', '--output', type=str, default='output.gif')
  args = parser.parse_args()

  myqr.run(
    words='https://sites.google.com/site/xisisu',
    picture=args.input,
    colorized=True,
    save_name=args.output,
  )


if __name__ == '__main__':
  run()
