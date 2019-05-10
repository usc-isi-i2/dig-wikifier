# T-SNE plots for several visualizations

This folder primarily contains all the T-SNE diagrams for different embeddings that were generated with parts of Wikidata ontology.


We ran experiments generating several embeddings, listing them below -
1. Python-bigGraph - Extracted embeddings from chosen subset of wikidata entities from the [Python-BigGraph](https://github.com/facebookresearch/PyTorch-BigGraph)
and plotted them.
2. VERSE - Trained embeddings on the wikidata ontology using [VERSE](https://github.com/xgfs/verse) and visualized the embeddings.
3. TransX - Trained embeddings on the wikidata ontology using [TransE, TransH, TransR](https://github.com/thunlp/OpenKE)
4. Word2vec on Random walk - Trained embeddings on a large file of random walks using [this algorithm](https://github.com/usc-isi-i2/dig-wikifier/blob/master/scripts/embedding_input_generators/random_walk.py)

Find the T-SNE plots for them here.