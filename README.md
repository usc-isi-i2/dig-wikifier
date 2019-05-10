# dig-wikifier


## Resolving dependencies


#### Initialize:
First initialize the virtual environment required to run wikifier.

```
conda env create .
source activate wikifier
```

This module needs etk module to run. 
Install etk using
```
pip install etk
```

there are some additional dependencies, spacy downloads do them as follows : 
Load the spacy modules
```
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_lg (optional)
```
Note: If the above commands fail with s SSL error, run this:
```
python -m spacy download en_core_web_sm-2.0.0 --direct
```

This repo contains the scripts used to preprocess wikidata, and also run the wikifier as a service.


Git-lfs (Important) -
This repository contains some files that are stored via git-lfs. These are some of the files generated during the intermediary steps in preprocessing wikifier data. If you require to use these files, fetch them using git-lfs. Refer https://github.com/git-lfs/git-lfs/wiki/Tutorial on how to fetch files stored via git-lfs.


There are additional documentation for the different parts of the demo -
1. Server setup and server instructions can be found here - [server instructions](https://github.com/usc-isi-i2/dig-wikifier/blob/master/server_instructions.md)
2. Redis server setup instructions can be found here - [Redis Setup](https://github.com/usc-isi-i2/dig-wikifier/blob/master/scripts/REDIS.md)
3. Instructions about using the wikidata pre-processing scripts can be found here - [Wikidata pre-processor](https://github.com/usc-isi-i2/dig-wikifier/blob/master/scripts/wikidata_processing/README.md)
4. Information about using T-SNE diagram script is here - [Visualizations](https://github.com/usc-isi-i2/dig-wikifier/blob/master/scripts/viz/README.md)
5. Information about loading/unloading data structures into redis - [Redis interaction scripts](https://github.com/usc-isi-i2/dig-wikifier/blob/master/scripts/redis_scripts/README.md)
6. Information about generating input files for some common embedding training algorithms that we have experimented with can be found here - [Embedding Training](https://github.com/usc-isi-i2/dig-wikifier/blob/master/scripts/embedding_input_generators/README.md)
7. To look at some of the experiments results, find the T-SNE diagrams here - [T-SNE diagrams](https://github.com/usc-isi-i2/dig-wikifier/tree/master/scripts/generated_viz)

