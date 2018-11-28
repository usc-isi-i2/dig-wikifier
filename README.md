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
