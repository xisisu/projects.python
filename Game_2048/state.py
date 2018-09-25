from enum import Enum, auto


class STATE(Enum):
  INIT = auto()
  IN_GAME = auto()
  OVER = auto()
  WIN = auto()
  EXIT = auto()
