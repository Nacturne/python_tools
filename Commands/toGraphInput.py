import config
from Core import TreeClass
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('I', metavar='input_path', type=str, help="The path of the input file")
parser.add_argument('O', metavar='output_path', type=str, help="The path of the output folder, ending with a /")

args = parser.parse_args()

file_in = open(config.ROOT_DIR + '/' + args.I, 'r')

for count,s in enumerate(file_in):
    tree = TreeClass.ScoreTree(s)
    graph_input = tree.toGraphInput()
    file_out = open('{}/{}graphInput_{}.dot'.format(config.ROOT_DIR,args.O,count), 'w')
    file_out.write(graph_input)
    file_out.close()

file_in.close()