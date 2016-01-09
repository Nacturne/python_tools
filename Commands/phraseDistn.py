import config
import argparse
import pandas as pd
from Core import TreeClass

parser = argparse.ArgumentParser()
parser.add_argument('I', metavar='input_path', type=str, help="The path of the input file")
args = parser.parse_args()

file_in = open(config.ROOT_DIR + '/' + args.I, 'r')

temp = []
for s in file_in:
    tree = TreeClass.ScoreTree(s)
    for node in tree.allNodes():
        temp.append([int(node.label), node.num_phrases()])

file_in.close()

stats = pd.DataFrame(temp, columns=['score', 'num_phrases'])

print("-------------------------------------------")
print("{0:10}\t{1:10}\t{2:10}".format('phrase_length','number','percentage'))
print("-------------------------------------------")

total = stats.shape[0]
for i in range(1,31):
    count = stats[stats['num_phrases'] == i].shape[0]
    print("{0:10}\t{1:10}\t{2:10.5f}".format(i,count, count/float(total)))

word_count = stats[stats['num_phrases'] == 0].shape[0]
print("-------------------------------------------")
print("{0:10}\t{1:10}\t{2:10.5f}".format('words',word_count, word_count/float(total)))
print("{0:10}\t{1:10}\t{2:10.5f}".format('total',total, 1))
print("-------------------------------------------")