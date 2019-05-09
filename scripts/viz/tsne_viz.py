import json
import numpy as np
from collections import defaultdict
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import matplotlib.cm as cm


#keys = ['City-large','City-small','Country-1','Country-2','Person-pol','Person-sport','Persion-gen','Company-tech','Company-gen','Org-pol','Animal','Deity','Profession']
keys = ['genre','film','film-editor','producer','director-photography','edu-institute','director','screenwriter','castmember','country','main-subject','superclasses']
def tsne_plot_similar_words(title, labels, embedding_clusters, word_clusters, a, filename=None):
    plt.figure(figsize=(16, 9))
    colors = cm.rainbow(np.linspace(0, 1, len(labels)))
    for label, embeddings, words, color in zip(labels, embedding_clusters, word_clusters, colors):
        x = embeddings[:, 0]
        y = embeddings[:, 1]
        plt.scatter(x, y, c=color, alpha=a, label=label)
        for i, word in enumerate(words):
            plt.annotate(word, alpha=0.5, xy=(x[i], y[i]), xytext=(5, 2),
                         textcoords='offset points', ha='right', va='bottom', size=8)
    plt.legend(loc=4)
    plt.title(title)
    plt.grid(True)
    if filename:
        plt.savefig(filename, format='png', dpi=400, bbox_inches='tight')
    plt.show()

#class_breaks = [11, 21, 31, 41, 51, 61, 71, 81, 91, 101, 111, 121]
#class_breaks = [10,19,28,39,49,57,66,75,81,91,100,110]
class_breaks = [20,40,60,80,100,120,140,160,180,200,220]
data = defaultdict(dict)
clusters = [[]]
# embeddings = open('embeddings.txt','w')
# meta = open('meta.txt','w')

with open('tsne_input_biggraph','r') as fin:
    for i,l in enumerate(fin):
        if i in set(class_breaks):
            clusters.append([])
        line_data = l.split('::')
        qnode,label,em = line_data
        # d = json.loads(em)
        # d = [str(x) for x in d]
        # embeddings.write("\t".join(d) + '\n')
        # meta.write(label+'\n')
        embed = np.array(json.loads(em), dtype=float)
        data[qnode]['lb'] = label
        data[qnode]['em'] = embed
        clusters[-1].append(qnode)

embedding_clusters = []
word_clusters = []
for cluster in clusters:
    embeddings = []
    labels = []
    i = 0
    for ele in cluster:
        i+=1
        labels.append(data[ele]['lb'])
        embeddings.append(data[ele]['em'])
        if i> 9:
           break
    embedding_clusters.append(embeddings)
    print(len(embeddings))
    word_clusters.append(labels)
embedding_clusters = np.array(embedding_clusters)
n, m, k = 12,10,200
tsne_model_en_2d = TSNE(perplexity=15, n_components=2, init='pca', n_iter=5000, random_state=32)
embeddings_en_2d = np.array(tsne_model_en_2d.fit_transform(embedding_clusters.reshape(n*m, k))).reshape(n,m,2)

tsne_plot_similar_words('Embeddings Biggraph-Pytorch(FB) for film graph nodes', keys, embeddings_en_2d, word_clusters, 0.7,
                        'similar_words.png')