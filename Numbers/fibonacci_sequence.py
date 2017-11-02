"""
Fibonacci Sequence - Enter a number and have the program generate the Fibonacci sequence to that number or to the Nth
number.
"""


def GenerateNthFibonacci(fib_map, n):
  if n in fib_map:
    return fib_map[n]

  for i in range(1, n + 1):
    if i in fib_map:
      continue
    fib_map[i] = fib_map[i - 2] + fib_map[i - 1]
  return fib_map[n]


def GetUntilFibonacci(fib_map, n):
  for i in range(1, n + 1):
    if fib_map[i] > n:
      return fib_map[i - 1]
  return fib_map[n]


def run():
  fib_map = {1: 1, 2: 1}
  while True:
    n = input('Enter the number to generate for nth fibonacci sequence: ')
    if n in ('quit', 'exit'):
      print(fib_map)
      return
    elif not n.isdigit():
      print('{} is not a digit'.format(n))
    elif int(n) <= 0:
      print('{} must be greater than 0.'.format(n))
    else:
      nth = GenerateNthFibonacci(fib_map, int(n))
      n_fib = GetUntilFibonacci(fib_map, int(n))
      print('{}th fib number is {}, closest fib number to n is {}.'.format(n, nth, n_fib))


if __name__ == '__main__':
  run()
