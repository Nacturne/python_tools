__author__ = 'Nacturne'

from Core import TreeClass as tc

#line = "(ROOT (S (CC But) (NP (PRP he)) (ADVP (RB somehow)) (VP (VBZ pulls) (NP (PRP it)) (PRT (RP off))) (. .)))"
#line = "(ROOT (S (SBAR (NP (ADJP (JJ Effective) (CC but) (JJ too-tepid)) (NN biopic)) (IN If) (S (NP (PRP you)) (ADVP (RB sometimes)) (VP (VBP like) (S (VP (TO to) (VP (VB go) (PP (TO to) (NP (DT the) (NNS movies))) (S (VP (TO to) (VP (VB have) (NP (NN fun))))))))))) (, ,) (NP (NNP Wasabi)) (VP (VBZ is) (NP (DT a) (JJ good) (NN place) (S (VP (TO to) (VP (VB start)))))) (. .)))"
#line = "(ROOT (2 (3 (3 Effective) (2 but)) (1 (1 too-tepid) (2 biopic))))"
#line = "(3 (3 (3 Effective) (2 but)) (1 (1 too-tepid) (2 biopic)))"
#line = "(3 (1 -LRB-) (3 (2 Wendigo) (3 (3 (2 (2 is) (3 -RRB-)) (3 (2 why) (3 (2 we) (3 (2 go) (2 (2 to) (3 (2 (2 (2 the) (2 cinema)) (2 :)) (3 (2 to) (2 (2 be) (2 (2 fed) (3 (2 through) (2 (2 (2 (2 the) (2 eye)) (2 ,)) (3 (3 (2 (2 the) (2 heart)) (2 ,)) (2 (2 the) (2 mind)))))))))))))) (2 .))))"


#line = "(3 (3 (3 (2 Scores) (2 (2 a) (1 (2 few) (2 points)))) (4 (2 for) (3 (2 doing) (3 (2 what) (3 (2 it) (3 (2 does) (4 (2 with) (3 (2 a) (4 (3 (3 (3 dedicated) (2 and)) (3 good-hearted)) (3 professionalism)))))))))) (2 .))"

#line = "(ROOT (S (NP (DT The) (NNP Rock)) (@S:NP... (VP (VBZ is) (VP (VBN destined) (SBAR (@SBAR:...SBAR (SBAR (S (VP (TO to) (VP (VB be) (NP (NP (DT the) (@NP:DT... (NNP 21st) (@NP:DT-NNP... (NNP Century) (POS 's)))) (@NP:NP... (JJ new) (@NP:NPJJ... (`` ``) (@NP:NP-JJ-``... (NNP Conan) ('' ''))))))))) (CC and)) (SBAR (IN that) (S (NP (PRP he)) (VP (VBZ 's) (VP (VBG going) (S (VP (TO to) (VP (@VP:...-PP (VB make) (NP (NP (DT a) (NN splash)) (ADJP (RB even) (JJR greater)))) (PP (IN than) (NP (@NP:...NP (@NP:...CC-NP (@NP:...NP-CC-NP (NP (NNP Arnold) (NNP Schwarzenegger)) (, ,)) (NP (NNP Jean-Claud) (@NP:NNP... (NNP Van) (NNP Damme)))) (CC or)) (NP (NNP Steven) (NNP Segal)))))))))))))) (. .)))) "
#tree = tc.scoreTree(line)
#print(tree.simplify())

#print(tree.toGraphInput())
#print(len(tree.keyNodes()))


'''
file_in1 = open("output/new_simplified_type_4.txt", 'r')
file_in2 = open("output/new_simplified_type_4", 'r')

lines1 = file_in1.readlines()
lines2 = file_in2.readlines()

print(len(lines1))
print(len(lines2))

counter = 0

for i in range(len(lines1)):
    if lines1[i] == lines2[i]:
        counter += 1

print(counter)

file_in1.close()
file_in2.close()

'''




file_in = open("output/simplified/type_4.txt", 'r')
file_out = open("output/simplified/new_simplified_type_4.txt", 'w')

for line in file_in:
    tree = tc.ScoreTree(line)
    file_out.write(tree.simplify() + '\n')

file_in.close()
file_out.close()
'''

file_in = open("output/simplified/type_3.txt", 'r')

for line in file_in:
    tree = tc.scoreTree(line)
    print(tree.treeType())

file_in.close()
'''















