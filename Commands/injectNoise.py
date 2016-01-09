import config
import argparse
from Core import TreeClass
import random
import sys

def simp_tool(sentence, phrase_length, cumulative):
    tree = TreeClass.ScoreTree(sentence)
    node_list = tree.allNodes()
    if cumulative:
        for node in node_list:
            if node.num_phrases() <= phrase_length and node.num_phrases() > 0:
                node.label = str(random.randint(0,4))
    else:
        for node in node_list:
            if node.num_phrases() == phrase_length:
                node.label = str(random.randint(0,4))
    return tree.toPTB()

def sentence_noise(args):
    print('The sentence with injected noise is:')
    print(simp_tool(args.S, args.length, args.cumulative))


def file_noise(args):
    file_in = open(config.ROOT_DIR + '/' + args.I, 'r')
    file_out = open(config.ROOT_DIR + '/' + args.O, 'w')
    for s in file_in:
        noised_sentence = simp_tool(s, args.length, args.cumulative)
        file_out.write(noised_sentence + '\n')
    file_in.close()
    file_out.close()

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--cumulative',dest='cumulative', action='store_true', help='If specified, noises will be injected to all phrases <= Length parameter')
parser.add_argument('-l', '--length', metavar='Length', type=int, help="Inject noise to phrase of this length")
subparsers = parser.add_subparsers(help='specify the type of input')

parser_sentence = subparsers.add_parser('sentence', help='Specified if the input is a sentence')
parser_sentence.add_argument('S', metavar='Sentence', type=str, help='A sentence in PTB format wrapped with double quotation marks')
parser_sentence.set_defaults(func=sentence_noise)

parser_file = subparsers.add_parser('file', help='Specified if the input is a file')
parser_file.add_argument('I', metavar='input_path', type=str, help="The path of the input file")
parser_file.add_argument('O', metavar='output_path', type=str, help="The path of the output file")
parser_file.set_defaults(func=file_noise)

args = parser.parse_args()


if not args.length:
    print("Please provide the length parameter by -l")
    sys.exit(1)
elif args.length <= 0:
    print("the value of Length should be an integer greater than 0")
    sys.exit(1)

args.func(args)
