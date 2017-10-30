"""
Find PI to the Nth Digit - Enter a number and have the program generate PI up to that many decimal places. Keep a limit
to how far the program will go.
"""

from mpmath import mp


def GeneratePi(n):
  mp.dps = n  # set number of digits
  print(mp.pi)  # print pi to a thousand places


def run():
  while True:
    n = input('Enter the number of digits to generate for pi: ')
    if n in ('quit', 'exit'):
      return 0
    elif not n.isdigit():
      print('{} is not a digit'.format(n))
    elif int(n) <= 0:
      print('{} must be greater than 0.'.format(n))
    else:
      GeneratePi(int(n))


if __name__ == '__main__':
  run()
