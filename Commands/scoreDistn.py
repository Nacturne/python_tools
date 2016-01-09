import config
import argparse
from Core import TreeClass
import pandas as pd


def distnOfScore(dataFrame, combined, index): # Length parameter is handled outside this function so that it can be used to the  situation of 'total'
    score0 = dataFrame[dataFrame['score'] == 0].shape[0]
    score1 = dataFrame[dataFrame['score'] == 1].shape[0]
    score2 = dataFrame[dataFrame['score'] == 2].shape[0]
    score3 = dataFrame[dataFrame['score'] == 3].shape[0]
    score4 = dataFrame[dataFrame['score'] == 4].shape[0]
    if combined:
        print('{0:8}\t{1:8}\t{2:8}\t{3:8}'.format(index, score0 + score1, score2, score3 + score4))
    else:
        print('{0:6}\t{1:6}\t{2:6}\t{3:6}\t{4:6}\t{5:6}'.format(index,score0, score1, score2, score3, score4))


parser = argparse.ArgumentParser()
parser.add_argument('I', metavar='input_path', type=str, help="The path of the input file")
parser.add_argument('-c', '--combined',dest='combined', action='store_true', help='If specified, 0+1=neg, 2=neutral, 3+4=pos')
parser.add_argument('-l', '--length',dest='length', type=int, help='Report score distn on different length of phrase, up to the number you specifed')


args = parser.parse_args()

if args.length and args.length <= 0:
    raise ValueError("the value of length should be an integer greater than 0")

file_in = open(config.ROOT_DIR + '/' + args.I, 'r')
temp = []
for s in file_in:
    tree = TreeClass.ScoreTree(s)
    for node in tree.allNodes():
        temp.append([int(node.label), node.num_phrases()])
file_in.close()
stats = pd.DataFrame(temp, columns=['score', 'num_phrases'])

print("---------------------------------------------------------")
if args.combined:
    print("{0:8}\t{1:8}\t{2:8}\t{3:8}".format('length','neg','neutral', 'pos'))
else:
    print('{0:6}\t{1:6}\t{2:6}\t{3:6}\t{4:6}\t{5:6}'.format('length','score0', 'score1', 'score2', 'score3', 'score4'))
print("---------------------------------------------------------")

distnOfScore(stats,args.combined,'total')

phraseOfI = stats[stats['num_phrases'] == 0]
distnOfScore(phraseOfI,args.combined,'words')

if args.length:
    for i in range(1,args.length+1):
        phraseOfI = stats[stats['num_phrases'] == i]
        distnOfScore(phraseOfI,args.combined,i)

print("---------------------------------------------------------")
