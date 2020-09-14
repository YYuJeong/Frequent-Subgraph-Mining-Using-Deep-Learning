# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 17:15:23 2020

@author: YuJeong
"""

import numpy as np
import glob, os
import string
from collections import defaultdict 

dir = '.\\datasets\\fsm\\graph*'

def readRepresentGraph():
    files = glob.glob( dir)
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

def printAdjList(AdjList):
    print("Adjacency List:") 
    # print the adjacency list 
    for i in AdjList: 
        print(i, end ="") 
        for j in AdjList[i]: 
            print(" -> {}".format(j), end ="") 
        print() 
  
if __name__ == "__main__":
    all_graphs = readRepresentGraph()    
    all_adjList = convertAdjMatToAdjList(all_graphs) 
    
    minsup = 2
    
    # all frequent 1-subgraphs
    F1 = []
    edges_1 = []
    for i in all_adjList[0]:
        for j in all_adjList[0][i]:
            if j > i:
                edges_1.append([j,i])
            else:
                edges_1.append([i,j])
        
    l2s = list(set(map(tuple,edges_1)))
    for s in l2s:
        if edges_1.count(list(s)) >= minsup:
            F1.append(list(s))
    
    #FSM
    k = 2
     
    
    