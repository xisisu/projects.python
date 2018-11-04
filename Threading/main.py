import math
import os
import time
from multiprocessing import Process
from threading import Thread


def calc():
  for i in range(10000000):
    math.sqrt(i)


def run_thread():
  threads = []
  for i in range(os.cpu_count()):
    print('thread {}'.format(i))
    threads.append(Thread(target=calc))

  for t in threads:
    t.start()

  for t in threads:
    t.join()


def run_process():
  processes = []
  for i in range(os.cpu_count()):
    print('process {}'.format(i))
    processes.append(Process(target=calc))

  for p in processes:
    p.start()

  for p in processes:
    p.join()


if __name__ == '__main__':
  start = time.time()
  run_thread()
  # run_process()
  finish = time.time() - start
  print('total time: {}'.format(finish))
