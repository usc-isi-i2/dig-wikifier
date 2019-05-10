# -*- coding: utf-8 -*-
"""
Created on Wed May  8 16:37:48 2019

@author: harish
"""
import networkx as nx
import sys

filename=sys.argv[1]
opfile=sys.argv[2]

G=nx.DiGraph()
open_datafiles=open(filename,"r")
open_datafiles=open_datafiles.readlines()
edges=[]
#Counting edge weights
mapper={}
for element in open_datafiles:
    edge=element.strip().split()
    a,b=edge[0],edge[1]
    if (a,b) in mapper:
        mapper[(a,b)]+=1
    else:
        mapper[(a,b)]=1
    
for a,b in mapper:
    edges.append((a,b,mapper[(a,b)]))

G.add_weighted_edges_from(edges)


pr=nx.pagerank(G)
print(pr)
outputfile=open(opfile,"w")

for element in pr:
    prelm=pr[element]
    outputfile.write(element+" "+str(prelm)+"\n")
