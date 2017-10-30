"""
Next Prime Number - Have the program find prime numbers until the user chooses to stop asking for the next one.
"""

Factors = lambda n: [x for x in range(1, int(n) + 1) if not n % x]
IsPrime = lambda n: len(Factors(n)) == 2


def NextPrime(n):
  n = n + 1
  while not IsPrime(n):
    n = n + 1
  return n


def run():
  cur = 1
  while True:
    n = input('next prime? (y/n): ')
    if n == 'n':
      return 0
    elif n != 'y':
      print('{} is not a valid.'.format(n))
    else:
      print(cur)
      cur = NextPrime(cur)


if __name__ == '__main__':
  run()
