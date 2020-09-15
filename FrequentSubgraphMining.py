# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 17:15:23 2020

@author: YuJeong
"""

import numpy as np
import glob, os
import string
from collections import defaultdict 
from itertools import combinations
import numpy as np
   
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
        
def convertFntoDict(Fn, k):
    Fn_flat = np.array(Fn).flatten()
    dup_Fn = list(set(map(tuple,Fn_flat)))
    edge2dict = {k: v for v, k in enumerate(dup_Fn)}
    FntoDict = []
    for fn in Fn:
        dic = []
        for kk in range(k):
            dic.append(edge2dict[tuple(fn[kk])])
        FntoDict.append(tuple(dic))
    return edge2dict, FntoDict

def reconstructCn(Cn, edge2dict):
    recons_Cn = []
    dup_Cn = []
    for i in Cn:
        dup_Cn.append(i[0].union(i[1]))
    dup_Cn = list(set(map(tuple,dup_Cn)))
    for j in dup_Cn:
        l = list(j)
        tmp = []
        for i in l:
            for key, val in edge2dict.items():
                if val == i:
                    #print(i)
                    #print(val)
                    tmp.append(set(key))
        recons_Cn.append(tmp)  
    return recons_Cn

def generateCandidate(Fn, k):
    '''
    1. Fn flatten
    2. remove duplicate
    3. to dict
    4. Fn convert to dict
    5. candidate generate
    '''
    if k > 2:
        edge2dict, Fn = convertFntoDict(Fn, k-1)
        
    candid = []   
    Cn = []
    for i in range(len(Fn)):
        fn_base = set(Fn[i])
        for j in range(i+1, len(Fn)):
            comp = set(Fn[j])
            if fn_base.intersection(comp) != set():
                Cn.append([fn_base, comp])
                candid.append(list(fn_base.union(comp)))
    
    if k > 2:
        Cn = reconstructCn(Cn, edge2dict)
    #Cn = list(set(map(tuple,candid)))      
    return Cn

def countCandidate(Cn, k):
    Fn = []
    for c in Cn:
        freq_count = 0 
        for ind, g in enumerate(all_adjList):
            edge_count = 0
            for i in range(k): #k 만큼 안에 리스트 존재
                (u, v) = list(c[i])
                if v in g[u]:
                    edge_count = edge_count + 1
            if edge_count == k: #Cn의 c가 g에 존재
                freq_count = freq_count + 1 #이 그래프 g에는 c가 있음
        if freq_count >= minsup:
            Fn.append(c)
    return Fn

def countAllF1Subgraph(all_adjList, minsup):
    F1 = []
    vertex_len = []
    
    for g in all_adjList:
        vertex_len.append(len(g))
    max_vertex_len = max(vertex_len)
    ver_comb = [i for i in range(max_vertex_len)]
    ver_comb = list(combinations(ver_comb, 2))

    for comb in ver_comb:
        (u, v) = comb
        freq_count = 0
        for g in all_adjList:
            if v in g[u]:
                freq_count = freq_count + 1
        if freq_count >= minsup:
            F1.append(comb)
    return F1
    
if __name__ == "__main__":
    all_graphs = readRepresentGraph()    
    all_adjList = convertAdjMatToAdjList(all_graphs) 
    
    minsup = 2
    
    # all frequent 1-subgraphs
    F1 = countAllF1Subgraph(all_adjList , minsup)
    k = 2
    F = []
    
    while globals()['F%s' % (k-1)] != []:
        globals()['C%s' % k] = generateCandidate(globals()['F%s' % (k-1)], k)    
        globals()['F%s' % k] = countCandidate(globals()['C%s' % k], k)
        k = k + 1
    print(globals()['F%s' % (k-2)])
    

    