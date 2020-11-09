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
import collections
from networkx.algorithms import isomorphism
from scipy.spatial import distance
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
    T = 0.5

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
    
    candidE = []
    for c2 in C2:
        (u, v) = c2
        edge0 = all_graphs[0][u][v]
        if edge0 != 0: 
            for ind, graph in enumerate(all_graphs[1:]):
                if graph[u][v] != 0 and distance.euclidean(edge0, graph[u][v]) <= T:
                    edge0 = (edge0 + graph[u][v])/ 2
                else:
                    if graph[u][v] != 0:
                        candidE.append([u, v, graph[u][v]])
            candidE.append([u, v, edge0])
    C2 = candidE
    C2todic = []
    for c2 in C2:
        (u, v, w) = c2
        for var, edge in edge2dic.items():
            if edge == (u, v):
                C2todic.append([var, w])
    C2 = C2todic
        
    
    ## find F2 using C2    
    F2 = [] 
    for c2 in C2:
        (u, v) = edge2dic[c2[0]]
        w = c2[1]
        count = 0 
        for graph in all_graphs:
            if graph[u][v] != 0 and distance.euclidean(graph[u][v], w) <= T:
                count = count + 1
        if count >= minsup:
            F2.append([c2[0], w])

    ## generate C3 using F2 --> k = 3
    C3 = []
    for ind, f2 in enumerate(F2):
        for f in F2[ind+1:]:
            (u1, v1) = edge2dic[f2[0]]
            w1 = f2[1]
            (u2, v2) = edge2dic[f[0]]
            w2 = f[1]
            nodes = [u1, v1, u2, v2]
            samenode = [item for item, count in collections.Counter(nodes).items() if count > 1]
            c3 = []
            if len(samenode) >= 1:
                c3 = [f2[0], w1, f[0], w2]
            C3.append(c3)
    
    ## find F3 using C3 --> 재사용 가능
    k = 3
    F3 = []
    for c3 in C3:
        edges = c3[::2]
        count = 0 
        for ind, graph in enumerate(all_graphs):
            if set(edges).issubset(graphs2edge[ind]):
                candidG = c3[1::2]
                DBGraph = []
                for edge in edges:
                    (u, v) = edge2dic[edge]
                    DBGraph.append(graph[u][v])
                if distance.euclidean(candidG, DBGraph) <= T:
                    count = count + 1
        if count >= minsup:
            F3.append(c3)
    
    ## generate C4 usin F3 --> 재사용 가능 
    k = 4
    C4 = []
    for ind, f3 in enumerate(F3):
        for f in F3[ind+1:]:
            edgesG = f3[::2] # extract edges 
            edgesG.extend(f[::2][:])
            sameedges = [item for item, count in collections.Counter(edgesG).items() if count > 1]
            c4 = []
            if len(sameedges) == k-3: # edge이므로
                originedges1 = []  
                originedges2 = []
                for sameedge in sameedges:
                    g1weight = f3[f3.index(sameedge)+1] 
                    g2weight = f[f.index(sameedge)+1]
                    originedges1.extend([sameedge, g1weight])
                    originedges2.extend([sameedge, g2weight])
                    mergeWeight = (g1weight + g2weight)/2
                    mergeEdge = [sameedge, mergeWeight]
                    del f3[f3.index(sameedge):f3.index(sameedge)+2]
                    del f[f.index(sameedge):f.index(sameedge)+2]
                    c4.extend(mergeEdge)
                c4.extend(f3)
                c4.extend(f)
                f3.extend(originedges1)
                f.extend(originedges2)
            C4.append(c4)
                
      
    
    
    
    
    
    
    