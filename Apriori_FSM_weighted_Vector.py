# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 18:36:38 2020

@author: sookmyung
"""

import numpy as np
import glob, os
import string
from collections import defaultdict 
from itertools import combinations, chain, groupby
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
        
def findAllNodes(all_adjList_weight):
    ## find all frequent 1-subgraphs
    # all nodes in graph data set
    nodesList = []
    for adjList_weight in all_adjList_weight:
        nodesList.append(list(adjList_weight.keys()))
    nodesSet = list(set(chain.from_iterable(nodesList)))
    return nodesSet

def edgeTodic(nodesSet):
    # edge based encoding
    edge2dic = {}
    edgepairs =list(combinations(nodesSet, 2))      
    keys = range(len(edgepairs))
    for i in keys:
        edge2dic['e' + str(i)] = edgepairs[i]  
    return edge2dic
        
def EncodingGraphbyEdge(adjMat):      
    graph = []
    for i in range(len(adjMat)): 
        for j in range(len(adjMat[i])): 
           if adjMat[i][j] != 0: 
               e = (i, j)
               for var, edge in edge2dic.items():
                    if edge == e:
                        graph.append(var)  
    return graph

def findF0graphs():
    # scan each node in graph data set
    F0 = []
    for node in nodesSet:
        count = 0
        for adjList in all_adjList_weight:
            if node in adjList:
                count = count + 1
        if count >= minsup:
            F0.append(node)
    return F0

def generateC1(F0):
    ## generate C1 using F0
    
    C1 = list(combinations(F0, 2))
    
    candidE = []
    for c1 in C1:
        (u, v) = c1
        edge0 = all_graphs[0][u][v]
        if edge0 != 0: 
            for ind, graph in enumerate(all_graphs[1:]):
                if graph[u][v] != 0 and distance.euclidean(edge0, graph[u][v]) <= T:
                    edge0 = (edge0 + graph[u][v])/ 2
                else:
                    if graph[u][v] != 0:
                        candidE.append([u, v, graph[u][v]])
            candidE.append([u, v, edge0])
    C1 = candidE
    C1todic = []
    for c1 in C1:
        (u, v, w) = c1
        for var, edge in edge2dic.items():
            if edge == (u, v):
                C1todic.append([var, w])
    return C1todic    

def findF1(C1):
    ## find F1 using C1 --> k = 1    
    F1 = [] 
    for c1 in C1:
        (u, v) = edge2dic[c1[0]]
        w = c1[1]
        count = 0 
        for graph in all_graphs:
            if graph[u][v] != 0 and distance.euclidean(graph[u][v], w) <= T:
                count = count + 1
        if count >= minsup:
            F1.append([c1[0], w])
    return F1

def generateCandidate(Fn, k):
    ## generate C2 using F1 --> k = 2
    Cn = []
    for ind, fn in enumerate(Fn):
        for f in Fn[ind+1:]:
            edgesG = fn[::2] # extract edges 
            edgesG.extend(f[::2][:])
            sameedges = [item for item, count in collections.Counter(edgesG).items() if count > 1]
            cn = []
            if len(sameedges) == k-2: # edge이므로
                originedges1 = []  
                originedges2 = []
                for sameedge in sameedges:
                    g1weight = fn[fn.index(sameedge)+1] 
                    g2weight = f[f.index(sameedge)+1]
                    originedges1.extend([sameedge, g1weight])
                    originedges2.extend([sameedge, g2weight])
                    mergeWeight = (g1weight + g2weight)/2
                    mergeEdge = [sameedge, mergeWeight]
                    del fn[fn.index(sameedge):fn.index(sameedge)+2]
                    del f[f.index(sameedge):f.index(sameedge)+2]
                    cn.extend(mergeEdge)
                cn.extend(fn)
                cn.extend(f)
                fn.extend(originedges1)
                f.extend(originedges2)
            Cn.append(cn)
                
    # remove duplicate candidates
    Cnset = [sorted(ti, key=str) for ti in Cn]           
    Cnset = list(set(map(tuple,Cnset)))
    for cnset in Cnset:
        sameind = []
        for ind, cn in enumerate(Cn):
            if sorted(cn, key=str) == list(cnset):
                sameind.append(ind)
        sameind = sameind[:-1]
        for i in reversed(sameind):
            del Cn[i]
    return Cn

def countCandidate(Cn, k):
    Fn = []
    for cn in Cn:
        edges = cn[::2]
        count = 0 
        for ind, graph in enumerate(all_graphs):
            if set(edges).issubset(graphs2edge[ind]):
                candidG = cn[1::2]
                DBGraph = []
                for edge in edges:
                    (u, v) = edge2dic[edge]
                    DBGraph.append(graph[u][v])
                if distance.euclidean(candidG, DBGraph) <= T:
                    count = count + 1
        if count >= minsup:
            Fn.append(cn)
    return Fn

all_graphs = readRepresentGraph()    
all_adjList = convertAdjMatToAdjList(all_graphs) 
all_adjList_weight = convertAdjMatToAdjList_weight(all_graphs)         

nodesSet = findAllNodes(all_adjList_weight)
edge2dic = edgeTodic(nodesSet)

minsup = 3
T = 0.5
    
if __name__ == "__main__":
    
    
    graphs2edge = []
    for adjMat in all_graphs:   
        graphs2edge.append(EncodingGraphbyEdge(adjMat))
         
    F0 = findF0graphs()
    ## generate C1 using F0
    C1 = generateC1(F0)
    ## find F1 using C1 --> k = 1    
    F1 = findF1(C1)
    
    # FSM
    k = 2
    while globals()['F%s' % (k-1)] != []:
        globals()['C%s' % k] = generateCandidate(globals()['F%s' % (k-1)], k)    
        globals()['F%s' % k] = countCandidate(globals()['C%s' % k], k)
        k = k + 1
    print(globals()['F%s' % (k-2)])
    
