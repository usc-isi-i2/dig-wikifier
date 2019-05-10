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


