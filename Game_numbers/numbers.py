import pprint
import itertools

COLUMN_WIDTH = 9

def init_board():
  return [
    [1,2,3,4,5,6,7,8,9],
    [1,1,1,2,1,3,1,4,1],
    [5,1,6,1,7,1,8],
  ]

def print_board(board):
  for r in board:
    print(r)

def beat_game(board):
  return all(x == 1 for x in itertools.chain(*board))

def valid_pair(i, j):
  return i == j or i+j == 10

def get_left(board, i, j):
  cur = j-1
  while i >= 0:
    while cur >= 0:
      if board[i][cur] != 0:
        return (i, cur)
      cur-=1
    cur = COLUMN_WIDTH-1
    i-=1
  return None

def get_right(board, i, j):
  cur = j+1
  while i < len(board):
    while cur < len(board[i]):
      if board[i][cur] != 0:
        return (i, cur)
      cur+=1
    cur = 0
    i+=1
  return None

def get_next_move(board, i, j):
  if board[i][j] == 0:
    return None

  # try element on top
  cur = i-1
  while cur >= 0 and board[cur][j] == 0:
    cur -= 1
  if cur >= 0 and valid_pair(board[i][j], board[cur][j]):
    return (cur, j)

  # try element from left
  left = get_left(board, i, j)
  if left != None and valid_pair(board[i][j], board[left[0]][left[1]]):
    return left

  # try element from right
  right = get_right(board, i, j)
  if right != None and valid_pair(board[i][j], board[right[0]][right[1]]):
    return right

  # try element in bottom
  cur = i+1
  while cur < len(board) and j < len(board[cur]) and board[cur][j] == 0:
    cur += 1
  if cur < len(board) and j < len(board[cur]) and valid_pair(board[i][j], board[cur][j]):
    return (cur, j)
  

  return None

def move(board):
  for i in range(0, len(board)):
    for j in range(0, len(board[i])):
      next_move = get_next_move(board, i, j)
      if next_move == None:
        continue
      x, y = next_move
      print('pair {}({}, {}) with {}({}, {})'.format(board[i][j], i, j, board[x][y], x, y))
      return ((i, j), (x, y))
  return None

def get_list_of_valid_numbers(board):
  res = []
  for row in board:
    for i in row:
      if i != 0:
        res.append(i)
  return res

def filter_board(board):
  res = []
  for row in board:
    if all(x == 1 for x in row):
      continue
    res.append(row)
  return res

def extend_board(board):
  i = len(board)-1
  for n in get_list_of_valid_numbers(board):
    if len(board[i]) == COLUMN_WIDTH:
      board.append([])
      i += 1
    board[i].append(n)
  return filter_board(board)

if __name__ == '__main__':
  board = init_board()
  print_board(board)
  print('')
  
  count = 0
  while True:
    next_move = move(board)

    if next_move != None:
      ((i, j), (x, y)) = next_move
      board[i][j] = 0
      board[x][y] = 0
    else:
      board = extend_board(board)
      print_board(board)
      print('')
      count += 1
      if count > 5:
        break
    
    # print_board(board)
    # print('')
    


  
