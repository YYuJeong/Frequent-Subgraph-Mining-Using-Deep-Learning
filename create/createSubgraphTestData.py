# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 15:43:32 2020

@author: YuJeong
"""
from pathlib import Path
import networkx as nx
import collections
from networkx.algorithms import isomorphism
import glob, os
import numpy as np
import itertools 

# k-test.txt : k-edges subgraph



def readRepresentGraph():
    path = str(Path(__file__).parent.parent) 
    files = path + '\\datasets\\estimate_size\\rep0.txt'

    adMatrix = []
    with open(files, 'r') as f:
        for line in f: 
            l = []
            for num in line.split(' '):
                if num.isdigit(): 
                    l.append(int(num))
                else:
                    if num != '\n':
                        l.append(float(num))
            adMatrix.append(l)
    
        del adMatrix[0]
        
        for index, line in enumerate(adMatrix):
            for ind, val in enumerate(line):
                if ind == 0:
                    del line[ind]
    return adMatrix

def writeFile(index, sub2seq):
    filename = "\\datasets\\estimate_size\\test\\"+str(len(sub2seq))+"test" +  str(index) + '.txt'
    path = str(Path(__file__).parent.parent) + filename
    print(path)
    f = open(path, 'w')

    for row in sub2seq:
        print(str(row))
        f.write(str(row) + '\n')
    f.close()

def generateAllSubgraphNX(graph):
    G = gtoNx
    all_connected_subgraphs = []
    
    for nb_nodes in range(2, G.number_of_nodes()):
        for SG in (G.subgraph(selected_nodes) for selected_nodes in itertools.combinations(G, nb_nodes)):
            if nx.is_connected(SG):
                #print(SG.nodes)
                all_connected_subgraphs.append(SG.nodes)
    return all_connected_subgraphs

if __name__ == '__main__':    
    graph = readRepresentGraph()  
    gtoNparray = np.array(graph)
    gtoNx = nx.from_numpy_matrix(gtoNparray)
    all_connected_subgraphs = generateAllSubgraphNX(gtoNx)
                
    subgraph  = []
    for ind, connected_subgraph in enumerate(all_connected_subgraphs):
        edgepairs = list(itertools.combinations(connected_subgraph,2))
        print(edgepairs)
        sub2seq = []
        for edgepair in edgepairs:
            u, v = edgepair
            if graph[u][v] != 0:
                sub2seq.append([u, v, graph[u][v]])
        writeFile(ind, sub2seq)        
  