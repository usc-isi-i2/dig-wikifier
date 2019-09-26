# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 10:59:32 2019

@author: harish
"""

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
import numpy as np
import requests

input_file = "datafiles/castmembers_with_and_without_golden_globe_awards.txt"

def get_embeddings(qnode):
    query = { "query": { "term": { "key.keyword": { "value": "<http://www.wikidata.org/entity/"+qnode+">" } } } }
    names_es_search_url = "http://kg2018a.isi.edu:9200/wiki_fb_embeddings_1/_search"
    response = requests.post(names_es_search_url, json=query)
    if response.status_code == 200:
        hits = response.json()['hits']['hits']
        return hits[0]['_source']['value']
#        results = [x['_source']['value'] for x in hits]
    else:
        return []
#        print(response.text)
        
def classifier(X,y,filename):
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,stratify=y,random_state=66)
    model=LogisticRegression(verbose=10)
    model.fit(X_train,y_train)
    X_predict=model.predict(X_test)
    accuracy=str(np.mean(X_predict==y_test))
    content_write=filename+"\nAccuracy = "+accuracy+"\n"
    content_write+=classification_report(y_test,X_predict)
    fileopen=open(filename,"w")
    print(content_write)
    fileopen.write(content_write)
    fileopen.close()

file_handle=open(input_file,"r")
file_handle=file_handle.readlines()

X=[]
y=[]

for data in file_handle:
    temp=data.strip().split('-')
    X.append([float(j) for j in get_embeddings(temp[0])])   
    y.append(int(temp[1]))
    
classifier(X,y,"FB_implicit_classifier")
