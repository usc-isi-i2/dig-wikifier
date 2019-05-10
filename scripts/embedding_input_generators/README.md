# Embedding input generators


This folder contains 2 files will go through how to use each one of them.

## generate TransX input files (generate_transx_gpu_input.py)
The file takes a graph of the form as described below -
```
{
    "Q123" : {
            "P12" : ["Q124", "Q125", "Q126"] ,
            "P25" : ["Q100", "Q10201"]
            .
            .
            .
            .
    }
    .
    .
    .
    .

}
```
The above json is a json representation of the wikidata graph connected via properties. We take an input of such format and generate
the entity2id.txt, train2id.txt, relation2id.txt files required for transX GPU training. The files generated will be served as input to the
following repository -

`https://github.com/thunlp/OpenKE`

### Usage
```
python generate_transx_gpu_input.py --d inputfile.json
```

## generate a set of random walks

This file now takes a graph as described above and performs random walks as per the parameters set. Read the comments in the file
for more info on the random walks algorithm and parameters.

The generated walks file can be used as input for training a gensim model as follows -

```
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

inp_name=sys.argv[1]

sentences = LineSentence(inp_name)

w2v = Word2Vec(sentences, size=300, window=2, min_count=20, workers=32, iter=25)
w2v.save(outputfile)
```


