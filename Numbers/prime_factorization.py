"""
Prime Factorization - Have the user enter a number and find all Prime Factors (if there are any) and display them.
"""

Factors = lambda n: [x for x in range(1, int(n) + 1) if not n % x]
IsPrime = lambda n: len(Factors(n)) == 2
PrimeFactors = lambda n: list(filter(IsPrime, Factors(n)))


def GeneratePrimeFactor(n):
  if IsPrime(n):
    return str(int(n))
  f = PrimeFactors(n)
  return str(f[0]) + "*" + GeneratePrimeFactor(n / f[0])


def GeneratePrimeFactor2(prime_map, n):
  if n in prime_map:
    return prime_map[n]
  for i in range(2, n):
    if n % i != 0:
      continue
    temp = GeneratePrimeFactor2(prime_map, int(n / i))
    prime_map[n] = [i]
    for x in temp:
      prime_map[n].append(x)
    return prime_map[n]
  prime_map[n] = [n]
  return prime_map[n]


def run():
  prime_map = {1: [1]}
  while True:
    n = input('Enter the number: ')
    if n in ('quit', 'exit'):
      print(prime_map)
      return
    elif not n.isdigit():
      print('{} is not a digit'.format(n))
    elif int(n) <= 1:
      print('{} must be greater than 1.'.format(n))
    else:
      result = GeneratePrimeFactor(int(n))
      print('prime factors for {} are {}'.format(n, result))
      result = GeneratePrimeFactor2(prime_map, int(n))
      print('prime factors for {} are {}'.format(n, result))


if __name__ == '__main__':
  run()
