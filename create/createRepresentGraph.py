# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 10:51:19 2020

@author: YuJeong
"""

# Adjacency Matrix representation in Python

import os 
import copy, random
import string

class Graph(object):

    # Initialize the matrix
    def __init__(self, size, index):
        self.adjMatrix = []
        self.index = index
        for i in range(size):
            self.adjMatrix.append([0 for i in range(size)])
        self.size = size

    # Add edges
    def add_edge(self, v1, v2, weight):
        if v1 == v2:
            print("Same vertex %d and %d" % (v1, v2))
        self.adjMatrix[v1][v2] = weight
        self.adjMatrix[v2][v1] = weight

    # Remove edges
    def remove_edge(self, v1, v2):
        if self.adjMatrix[v1][v2] == 0:
            print("No edge between %d and %d" % (v1, v2))
            return
        self.adjMatrix[v1][v2] = 0
        self.adjMatrix[v2][v1] = 0

    def __len__(self):
        return self.size

    # Print the matrix
    def print_matrix(self):
        for row in self.adjMatrix:
            for val in row:
                print('{:4}'.format(val), end = ' ')
            print()

    def writeFile(self):
        ind = '0 '
        ind0 = '0 '
        for i in range(self.size):
            ind = ind + chr(ord('A') + i) + ' '
            ind0 = ind0 + '0 '
        
        #filename = "\\datasets\\group" + str(self.index+1) + "\\represent" + str(self.index) + '.txt'
        filename = "\\datasets\\fsm\\graph" +  str(self.index) + '.txt'
        path = os.getcwd() + filename
    
        f = open(path, 'w')
        f.write(ind0+'\n')
        for row in self.adjMatrix:
            line = '0 '
            for val in row:
                line = line + str(val) + ' '
            print(line)
            f.write(line+'\n')
        f.close()
        #f.write()


def createGraph(ithGraph):
    vnum = int(input("vertex num: "))
    g = Graph(vnum, ithGraph)

    while True:
        inp =  input("u v weight: ")
        if inp != 'z':
            a, b, weight = list(map(int, inp.split(' ')))
            
            #a, b = list(map(int, inp.split(' ')))
            #weight = float(input('weight: '))
            g.add_edge(a, b, weight)
        else:
            break
    g.print_matrix()
    g.writeFile()



if __name__ == '__main__':
    repNum = int(input("Represent graph number: " ))
    for i in range(repNum):    
        print('='*60)
        createGraph(i)
        print('='*60)
   # writeFile()
   
    
    
    
    
    