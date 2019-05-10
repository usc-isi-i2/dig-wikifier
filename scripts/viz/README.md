# How to use the files to visualize different embeddings?

You require a sample csv file as present in this directory as `embed_film.txt` which needs to be present as input for all the below programs.

## bigGraph T-SNE
Extract Embeddings for the ids that you want to visualize by using the following command out of [this file](https://dl.fbaipublicfiles.com/torchbiggraph/wikidata_translation_v1.tsv.gz)
using the following command
```
zgrep -iw "Q14547231\|Q3604747\|Q181283\|otherids" downloaded_file.gz > results.txt

```

That will give you all the embeddings as an array.


Convert that file to look like the following format, one Qnode per line with its label and embeddings as a serialized array.
```
http://wikidata.org/wiki/Q14547231,[12.41,-121.2,-2.5,6.5, . . . . ]
.
.
.
.
.
```

Then use the following command to run the biggraph tsne_script -
```

python generate_biggraph_tsne.py -b generated_file
```

## transE T-SNE

To extract transX embeddings, we need to use the following [link here](https://github.com/thunlp/OpenKE#getting-the-embedding-matrix) to extract
the embedding matrix. Once that is done succesfully, we should be able to use the script to generate the appropriate file for T-SNE visualization

The embedding matrix must be stored as a space separated file of vectors
```

1.22 -1.252 66.26 ....
.
.
.
.
.
```

Passing this as input to the program along with the entit2id.txt file (which would describe mapping of row number to Qnode)

```
python generate_transe_tsne.py -b embeddingmatrixfile -n entity2id.txt
```

## VERSE embeddings

To load the VERSE embeddings and to generate the correct file for t-sne viz, we use the following command below

```
python generate_tsne_input.py -b embedding.bin -n nodemap.json
```

In order to obtain the nodemap.json required for the above program, while generating inputs to train [VERSE](https://github.com/xgfs/verse) update the file
[convert.py](https://github.com/xgfs/verse/blob/master/python/convert.py) with the following code at [line](https://github.com/xgfs/verse/blob/0adfde139e817c13d84a29c167a4153ba2ce61af/python/convert.py#L71)
with the following -

```
with open('nodemap.json','w') as out:
        out.write(json.dumps(node2id))
```

The above lines will save the nodemap into a file, which will tell us the mapping for a given Qnode, which row in the matrix corresponds to the qnode's embedding vector

## word2vec embedding
To load the word2vec embedding trained after the random walks are generated, use the following command

```
python generate_word2vec_tsne.py -b theword2vecmodel
```

**Note: All of the above programs require a file like the embed_film.txt, and will not run without it. Feel free to modify to suit different formats, embeddings etc**

## Using T-SNE viz file
Once you have generated an input in the expected format, use the tsne_viz.py to plot the T-SNE diagram
**Note: Requires sklearn, scipy and matplotlib as dependencies**

```
python tsne_viz.py
```

The output will be stored in a file called output.png. It will also open a live plot window which you can interact with and explore the visualization
