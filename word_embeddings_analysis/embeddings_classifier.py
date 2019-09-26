# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 12:39:05 2019

@author: harish
"""

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
import numpy as np
import ast
import sys

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
    
embeddings_file = open(sys.argv[1],"r")
labels_file = open(sys.argv[2],"r")

embeddings = embeddings_file.readlines()
labels = labels_file.readlines()
labels = [int(val) for val in labels]

embeddings = [ast.literal_eval(val) for val in embeddings]

classifier(embeddings,labels,sys.argv[3])