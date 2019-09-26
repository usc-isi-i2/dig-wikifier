This is an experiment to analyse if the word embeddings can capture some underlying relationship between Qnodes. 
This experiment involves choosing a set of Qnode of castmembers who have won /not won golden globe awards.
Then we have a Logistic regression classifier to which the word embeddings of these qnodes are given to predict if the qnode has won/not won the golden globe award.

***Word embeddings used are:***  transE embeddings, Word2Vec embeddings, Facebook embeddings, VERSE embeddings

The embeddings and labels for transE, VERSE and word2vec are stored in the datafiles folder.

For running the classifiers for transE, VERSE and word2vec embeddings run the following command:

```python embeddings_classifier.py embeddings_input_file labels_input_file output_file_path```

The Facebook embeddings classifier will make use of the ***datafiles/castmembers_with_and_without_golden_globe_awards.txt*** file.
The facebook embedding vectors are obtained directly from Elastic search during runtime.
To run the Facebook embeddings classifier, run the command

```python fb_implicit_classifer.py```
