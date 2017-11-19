"""
Calculator - A simple calculator to do basic operators. Make it a scientific calculator for added complexity.
"""


def Calculate(formula):
  stack = []
  for val in formula.split(' '):
    if val.isdigit():
      stack.append(int(val))
    else:
      if len(stack) < 2:
        raise Exception('Invalid formula: {}'.format(formula))
      num1 = stack.pop()
      num2 = stack.pop()
      if val == '+':
        num = num2 + num1
      elif val == '-':
        num = num2 - num1
      elif val == '*' or val == 'x':
        num = num2 * num1
      elif val == '/' or val == '÷':
        num = num2 / num1
      else:
        raise Exception('unknown operator: {}'.format(val))
      stack.append(num)

  if len(stack) != 1:
    raise Exception('Stack contains more than one number, stack: {}'.format(stack))
  return stack.pop()


def run():
  while True:
    n = input('Enter the formula: ')
    if n in ('quit', 'exit'):
      return
    else:
      result = Calculate(n)
      print('{} = {}'.format(n, result))


if __name__ == '__main__':
  run()
