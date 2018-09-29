# https://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do

def lines(file):
  for line in file: yield line
  yield '\n'


def blocks(file):
  block = []
  for line in lines(file):
    if line.strip():
      block.append(line)
    elif block:
      yield ''.join(block).strip()
      block = []
