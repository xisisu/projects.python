"""
Change Return Program - The user enters a cost and then the amount of money given. The program will figure out the
change and the number of quarters, dimes, nickels, pennies needed for the change.
"""

import pprint


def GetChanges(n):
  dp = {}
  coins = (1, 5, 10, 25)
  for amount in range(1, n + 1):
    if amount in coins:
      dp[amount] = {amount: 1}
    else:
      cur = None
      for coin in coins:
        val = amount - coin
        if val <= 0:
          break
        if cur == None or sum(cur.values()) > sum(dp[val].values()) + 1:
          cur = dp[val].copy()
          cur[coin] = cur.get(coin, 0) + 1
      dp[amount] = cur

  return dp


def run():
  while True:
    cost = float(input('Enter the cost: '))
    total = float(input('Enter money given: '))
    if cost <= 0.0 or total <= 0.0 or cost >= total:
      print('Invalid input.')
      return

    print('total: {}, cost: {}'.format(total, cost))
    changes = GetChanges(int((total - cost) * 100))
    pprint.pprint('changes are: {}'.format(changes))


if __name__ == '__main__':
  run()
