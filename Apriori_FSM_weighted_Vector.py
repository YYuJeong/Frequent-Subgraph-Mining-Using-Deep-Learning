# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 18:36:38 2020

@author: sookmyung
"""

import numpy as np
import glob, os
import string
from collections import defaultdict 
from itertools import combinations, chain
import numpy as np
import networkx as nx
from networkx.algorithms import isomorphism
dir = '.\\datasets\\structure_fsm\\rep*'


def checkGraphIsomorphism(g1, g2):
    g1toNparray = np.array(g1)
    g2toNparray = np.array(g2)
    g1toNx = nx.from_numpy_matrix(g1toNparray)
    g2toNx = nx.from_numpy_matrix(g2toNparray)
    
    isIsomorphic = isomorphism.GraphMatcher(g1toNx, g2toNx)
    return isIsomorphic.is_isomorphic()

def readRepresentGraph():
    files = glob.glob(dir)
    all_graph = []
    for file in files:
        adMatrix = []
        with open(file, 'r') as f:
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
                    
        all_graph.append(adMatrix)     
        
    
    return all_graph


# converts from adjacency matrix to adjacency list 
def convertAdjMatToAdjList(adjMats):
    all_adjList = []
    for adjMat in adjMats:       
        adjList = defaultdict(list) 
        for i in range(len(adjMat)): 
            for j in range(len(adjMat[i])): 
               if adjMat[i][j] != 0: 
                   adjList[i].append(j)
        all_adjList.append(adjList)
    return all_adjList 

def convertAdjMatToAdjList_weight(adjMats):
    all_adjList_weight = []
    for adjMat in adjMats:       
        adjList = defaultdict(list) 
        for i in range(len(adjMat)): 
            for j in range(len(adjMat[i])): 
               if adjMat[i][j] != 0: 
                   adjList[i].append((j,adjMat[i][j]))
        all_adjList_weight.append(adjList)
    return all_adjList_weight

def printAdjList(AdjList):
    print("Adjacency List:") 
    # print the adjacency list 
    for i in AdjList: 
        print(i, end ="") 
        for j in AdjList[i]: 
            print(" -> {}".format(j), end ="") 
        print() 
        


all_graphs = readRepresentGraph()    
all_adjList = convertAdjMatToAdjList(all_graphs) 
all_adjList_weight = convertAdjMatToAdjList_weight(all_graphs)         


if __name__ == "__main__":
    
    minsup = 2
    T = 1

    ## find all frequent 1-subgraphs
    # all nodes in graph data set
    nodesList = []
    for adjList_weight in all_adjList_weight:
        nodesList.append(list(adjList_weight.keys()))
    nodesSet = list(set(chain.from_iterable(nodesList)))
    # scan each node in graph data set
    F1 = []
    for node in nodesSet:
        count = 0
        for adjList in all_adjList_weight:
            if node in adjList:
                count = count + 1
        if count >= minsup:
            F1.append(node)
    
    # edge based encoding
    edge2dic = {}
    edgepairs =list(combinations(nodesSet, 2))      
    keys = range(len(edgepairs))
    for i in keys:
        edge2dic['e' + str(i)] = edgepairs[i]      
    
    graphs2edge = []
    for adjMat in all_graphs:       
        graph = []
        for i in range(len(adjMat)): 
            for j in range(len(adjMat[i])): 
               if adjMat[i][j] != 0: 
                   e = (i, j)
                   for var, edge in edge2dic.items():
                        if edge == e:
                            graph.append(var)                            
        graphs2edge.append(graph)
    
    ## generate C2 using F1
    C2 = list(combinations(F1, 2))
    # C2 to edge2dic
    C2todic = []
    for c2 in C2:
        for var, edge in edge2dic.items():
            if edge == c2:
                C2todic.append(var) 

    
    ## find Fn using Cn-1
    for c2 in C2todic:
        count = 0        
        for ind, graph in enumerate(graphs2edge):
            if c2 in graph:
                print()
                    
    '''
    2 3 10 2
    '''                
                    