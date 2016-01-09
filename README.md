# python_tools

This is an auxiliary package containing python command line tools, which can be used with [StonyBrookNLP/stingysentiment](https://github.com/StonyBrookNLP/stingysentiment)


### Package Dependency

Package Dependency Infomation is included in `requirements.txt` file under the root directory. To install all the pacakages required for this program, run:

``` python
pip install -r requirements.txt
```

### Tools Available

**All the command line tools are in the `python_tools/Commands/` folder.

- `simplify.py`  —Use 'key words upward cross points' method to simplify a sentence of PTB format.
- `rawSentence.py`  —Convert sentences of PTB format to their raw form only consisting of words and punctuations.
- `injectNoise.py`  —Inject random number of scores(0,1,2,3,4) to the specific level of parsing trees.
- `phraseDistn.py`  —Output the statistics info for phrases of different length.
- `scoreDistn.py`  —Output the statistics info for nodes of different scores in parsing trees.
- `phraseF1.py`  —Evaluate the performence of models using F1 score. Results can be shown on different length of phrases.
- `toGraphInput.py`  —Convert sentences of PTB format to the standard input format in [Graph Discription Language](https://en.wikipedia.org/wiki/DOT_(graph_description_language)). The result of this command can be used as the input to some graph visualization tools, such as [Graphviz](http://www.graphviz.org).


### Usage by Examples

**To see help info of certain a command, run `python Commands/foo.py -h`. 

**For example, `python Commands/simplify.py -h` will out put the help info of `simplify.py`

<br />
---
**— simplify.py**

Take a sentence and simplify it, run:

``` python
python Commands/simplify.py sentence "(3 (3 (2 If) (3 (2 you) (3 (4 love) (2 (2 reading) (2 (2 and\/or) (3 poetry)))))) (3 (2 ,) (3 (2 (2 then) (2 (2 by) (2 all))) (3 (2 (2 means) (4 (2 (3 check) (2 it)) (1 out))) (2 .)))))"
```

The output would be:

``` 
This is a type-4 sentence.
The simplified sentence is:
(3 (3 (4 love) (3 poetry)) (4 (3 check) (1 out)))
```



Take a file as the source of input and write outputs to a destination file, run:

``` 
python Commands/simplify.py file input/train.txt output/train_simplified.txt
```

This command will take the **train.txt** file in `python_tools/input/` folder as the input. Then it creates a file named **train_simplified.txt** in `python_tools/output/` folder to hold the results.

<br />
To see help info for the command:

``` 
python Commands/simplify.py -h
```

To see help info for the command regarding sentence input:

``` 
python Commands/simplify.py sentence -h
```

To see help info for the command regarding file input:

``` 
python Commands/simplify.py file -h
```

<br />
---
**— rawSentence.py**

This command is highly analogous to `simplify.py`. Parameters in this command have the same meaning as their complementary part in `simplify.py`.


<br />
---
**— injectNoise.py**

Take a sentence and inject noise to nodes whose phrase length is 3:

``` python
python Commands/injectNoise.py -l 3 sentence "(4 (2 You) (4 (3 (2 (2 'll) (2 probably)) (4 (4 love) (2 it))) (2 .)))"
```

The output would be:

(4 (2 You) (4 (**0** (2 (2 'll) (2 probably)) (4 (4 love) (2 it))) (2 .)))

The bold **0** is the score changed, because this node in the parsing tree has a phrase length of 3.(*Note that you may get a different value as the value is chosen randomly from {0, 1, 2, 3, 4})


<br />
To inject noise to nodes whose phrase length is less or equal to 3:

``` python
python Commands/injectNoise.py -c -l 3 sentence "(4 (2 You) (4 (3 (2 (2 'll) (2 probably)) (4 (4 love) (2 it))) (2 .)))"
```

(4 (2 You) (4 (**0** (**1** (2 'll) (2 probably)) (**3** (4 love) (2 it))) (2 .)))

The bold **0**, **1**, **3** is the score changed, because this node in the parsing tree has a phrase length of 3, 2 or 1.


<br />
To take a file as an input:

``` 
python Commands/injectNoise.py -c -l 3 file input/train.txt output/noised_train.txt
```

This will do noise injection job to every senence in **train.txt** file. The results go to **noised_train.txt** under `python_tools/output/` directory.


<br />
To see help info, use the similar commands as in `simplify.py`:

``` 
python Commands/injectNoise.py -h
```

``` 
python Commands/injectNoise.py sentence -h
```

``` 
python Commands/injectNoise.py file -h
```

<br />
---
**— phraseDistn.py**

To take a file and calculate the distribution of phrase of different length:

``` 
python Commands/phraseDistn.py input/train.txt
``` 

The output would be:

```
-------------------------------------------
phrase_length   number          percentage
-------------------------------------------
         1           38371         0.12044
         2           23081         0.07245
         3           14616         0.04588
              ...
              ...
        29             387         0.00121
        30             363         0.00114
-------------------------------------------
words               163563         0.51341
total               318582         1.00000
-------------------------------------------
``` 

- This method give results upto length 30. 


- The first column is the length of phrase.


- The seconde column shows how many phrases of a specific length are in the **train.txt** file.


- The theird column showing figures in percentage.


- The second row to the bottom shows the total number of words in the file.


- The last row shows the total number of nodes in the parsing trees.



<br />
---
**— scoreDistn.py**

To see the score distribution in a file:

```
python Commands/scoreDistn.py input/train.txt
```
 

The output would be:

```
---------------------------------------------------------
length  score0  score1  score2  score3  score4
---------------------------------------------------------
total     8245   34362  219788   44194   11993
words     1130    7795  140415   11524    2699
---------------------------------------------------------
``` 

- The first row shows the number of nodes of every score.
- The second row shows the info for word nodes only.


<br />
To see results on phrases of different length:

```
python Commands/scoreDistn.py -l 5 input/train.txt
``` 

This command will give results upto length 5:

```
---------------------------------------------------------
length  score0  score1  score2  score3  score4
---------------------------------------------------------
total     8245   34362  219788   44194   11993
words     1130    7795  140415   11524    2699
     1     494    3791   27610    5502     974
     2     522    2752   14506    4374     927
     3     474    2206    8071    3127     738
     4     438    1832    5686    2503     650
     5     381    1649    4233    2150     579
---------------------------------------------------------
``` 

<br />
You can also combine the result by specifying the `-c` parameter:

```
python Commands/scoreDistn.py -c -l 5 input/train.txt

``` 

You will get:

```
---------------------------------------------------------
length          neg             neutral         pos     
---------------------------------------------------------
total              42607          219788           56187
words               8925          140415           14223
       1            4285           27610            6476
       2            3274           14506            5301
       3            2680            8071            3865
       4            2270            5686            3153
       5            2030            4233            2729
---------------------------------------------------------
``` 

where `neg` is the sum of `score0` and `score1`,  and `pos` is the sum of `score3` and `score4`. 



<br />
---
**— phraseF1.py**

To evaluate the performance of a model, input the original PTB format file **test.txt** and the predicted file **predicted_test.txt** containing sentences in the same format and order as that of **test.txt**. The only possible difference should be the scores. I emphasis again that everything else should be the same.

Assume that we have the files satisfying the previous requirements, and run:

```
python Commands/phraseF1.py input/test.txt input/predicted_test.py
``` 

you may get:

```
---------------------------------------------------------
length  score0  score1  score2  score3  score4
---------------------------------------------------------
total   0.00000 0.00086 0.88079 0.40108 0.28737
words   0.00000 0.00100 0.97728 0.57565 0.80846
---------------------------------------------------------
``` 

Note that the numbers in the output are F1 scores.


<br />
Similar as the command `scoreDistn.py`, you can use `-c` and `-l` parameters to get the combined F1 scores and to specify the length of phrases respectively.

For example:

```
python Commands/phraseF1.py -c -l 5 input/test.txt input/predicted_test.txt
``` 

will give F1 scores on different phrase level upto length 5, and the F1 score is calsulated combining type 0 and type 1 nodes(also combining type 3 and type 5 nodes). Results are shown below:

```
---------------------------------------------------------
length          neg             neutral         pos
---------------------------------------------------------
total            0.00071         0.88079         0.52064
words            0.00086         0.97728         0.62385
       1         0.00528         0.85089         0.45621
       2         0.00000         0.76927         0.45383
       3         0.00000         0.71935         0.45313
       4         0.00000         0.66412         0.49560
       5         0.00000         0.60773         0.46764
---------------------------------------------------------
``` 



<br />
---
**— toGraphInput.py**

To convert every sentence in **PTB_sentences.txt** to Graph [Description Language](https://en.wikipedia.org/wiki/DOT_(graph_description_language)) format, run:

```
python Commands/toGraphInput.py input/PTB_sentences.txt output/graphFiles/
``` 

You'll create `.dot` files in `output/graphFiles/` folder. Assume that there are 10 sentences in **PTB_sentences.txt**, the results would be named as 

- **graphInput_0.dot**


- **graphInput_2.dot**

​            ...

- **graphInput_9.dot** 

This kind of file can be open by [Graphviz](http://www.graphviz.org). Here is an example:

Sentensce:
```
(4 (2 (2 a) (2 (2 screenplay) (2 more))) (3 (4 ingeniously) (2 (2 constructed) (2 (2 (2 (2 than) (2 ``)) (2 Memento)) (2 '')))))
```

Graphviz Output:
![Graphviz Example]
(https://raw.githubusercontent.com/Nacturne/python_tools/master/graphviz_example.png)






<br />
<br />
<br />
<br />
#### Note:

Data structures are in the `python_tools/Core/TreeClass.py` file. 

