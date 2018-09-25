import argparse
import pprint

import codecs
import jieba
import jieba.posseg as pseg


def get_lines(input_filename, input_dict):
  line_names = []
  jieba.load_userdict(input_dict)
  with codecs.open(input_filename, 'r', 'utf8') as f:
    for line in f.readlines():
      poss = pseg.cut(line)
      line_names.append([])
      for w in poss:
        if w.flag != 'nr' or len(w.word) < 2:
          continue
        line_names[-1].append(w.word)
  return line_names


def get_node_count(line_names):
  names_to_count = {}
  for line in line_names:
    for name in line:
      names_to_count[name] = names_to_count.get(name, 0) + 1
  return names_to_count


def get_edge_value(line_names):
  names_to_edge = {}
  for line in line_names:
    for k in line:
      for v in line:
        if names_to_edge.get(k) == None:
          names_to_edge[k] = {}
        if names_to_edge[k].get(v) == None:
          names_to_edge[k][v] = 0
        names_to_edge[k][v] += 1
  return names_to_edge


def run(input_filename, input_dict, output_filename):
  line_names = get_lines(input_filename=input_filename, input_dict=input_dict)
  names_to_count = get_node_count(line_names=line_names)
  names_to_edge = get_edge_value(line_names=line_names)
  pprint.pprint(names_to_count)
  pprint.pprint(names_to_edge)


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Analyze movie scripts.')
  parser.add_argument('-i', '--input', type=str, default='resources/busan.txt')
  parser.add_argument('-d', '--input_dict', type=str, default='resources/dict.txt')
  parser.add_argument('-o', '--output', type=str, default='relations.txt')
  args = parser.parse_args()

  run(input_filename=args.input, input_dict=args.input_dict, output_filename=args.output)
