import config
from Core import TreeClass
import argparse
import argparse
from Core import TreeClass

def sentence_simplifier(args):
    tree = TreeClass.ScoreTree(args.S)
    print('This is a type-{} sentence.'.format(tree.treeType()))
    print('The simplified sentence is:')
    print(tree.simplify())

def file_simplifier(args):
    file_in = open(config.ROOT_DIR + args.I, 'r')
    file_out = open(config.ROOT_DIR + args.O, 'w')
    for s in file_in:
        tree = TreeClass.ScoreTree(s)
        file_out.write(tree.simplify() + '\n')
    file_in.close()
    file_out.close()

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='specify the type of input')

parser_sentence = subparsers.add_parser('sentence', help='Specified if the input is a sentence')
parser_sentence.add_argument('S', metavar='Sentence', type=str, help='A sentence in PTB format wrapped with double quotation marks')
parser_sentence.set_defaults(func=sentence_simplifier)

parser_file = subparsers.add_parser('file', help='Specified if the input is a file')
parser_file.add_argument('I', metavar='input_path', type=str, help="Please start it with '/', which means root dir")
parser_file.add_argument('O', metavar='output_path', type=str, help="Please start it with '/', which means root dir")
parser_file.set_defaults(func=file_simplifier)

args = parser.parse_args()
args.func(args)