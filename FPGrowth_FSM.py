# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 00:56:51 2020

@author: YuJeong
"""
import itertools
import numpy as np
import glob, os
import string
from collections import defaultdict 
from itertools import combinations, chain, groupby
import networkx as nx
import collections
from networkx.algorithms import isomorphism
from scipy.spatial import distance

dir = '.\\datasets\\structure_fsm\\rep*'

class FPNode(object):
    """
    A node in the FP tree.
    """

    def __init__(self, value, count, parent):
        """
        Create the node.
        """
        self.value = value
        self.count = count
        self.parent = parent
        self.link = None
        self.children = []

    def has_child(self, value):
        """
        Check if node has a particular child node.
        """
        for node in self.children:
            if node.value == value:
                return True

        return False

    def get_child(self, value):
        """
        Return a child node with a particular value.
        """
        for node in self.children:
            if node.value == value:
                return node

        return None

    def add_child(self, value):
        """
        Add a node as a child node.
        """
        child = FPNode(value, 1, self)
        self.children.append(child)
        return child


class FPTree(object):
    """
    A frequent pattern tree.
    """

    def __init__(self, transactions, threshold, root_value, root_count):
        """
        Initialize the tree.
        """
        self.frequent = self.find_frequent_items(transactions, threshold)
        self.headers = self.build_header_table(self.frequent)
        self.root = self.build_fptree(
            transactions, root_value,
            root_count, self.frequent, self.headers)

    @staticmethod
    def find_frequent_items(transactions, threshold):
        """
        Create a dictionary of items with occurrences above the threshold.
        """
        items = {}

        for transaction in transactions:
            for item in transaction:
                if item in items:
                    items[item] += 1
                else:
                    items[item] = 1

        for key in list(items.keys()):
            if items[key] < threshold:
                del items[key]
        #print(items)
        return items

    @staticmethod
    def build_header_table(frequent):
        """
        Build the header table.
        """
        headers = {}
        for key in frequent.keys():
            headers[key] = None

        return headers

    def build_fptree(self, transactions, root_value,
                     root_count, frequent, headers):
        """
        Build the FP tree and return the root node.
        """
        root = FPNode(root_value, root_count, None)

        for transaction in transactions:
            sorted_items = [x for x in transaction if x in frequent]
            sorted_items.sort(key=lambda x: frequent[x], reverse=True)
            if len(sorted_items) > 0:
                self.insert_tree(sorted_items, root, headers)

        return root

    def insert_tree(self, items, node, headers):
        """
        Recursively grow FP tree.
        """
        first = items[0]
        child = node.get_child(first)
        if child is not None:
            child.count += 1
        else:
            # Add new child.
            child = node.add_child(first)

            # Link it to header structure.
            if headers[first] is None:
                headers[first] = child
            else:
                current = headers[first]
                while current.link is not None:
                    current = current.link
                current.link = child

        # Call function recursively.
        remaining_items = items[1:]
        if len(remaining_items) > 0:
            self.insert_tree(remaining_items, child, headers)

    def tree_has_single_path(self, node):
        """
        If there is a single path in the tree,
        return True, else return False.
        """
        num_children = len(node.children)
        if num_children > 1:
            return False
        elif num_children == 0:
            return True
        else:
            return True and self.tree_has_single_path(node.children[0])

    def mine_patterns(self, threshold):
        """
        Mine the constructed FP tree for frequent patterns.
        """
        if self.tree_has_single_path(self.root):
            return self.generate_pattern_list()
        else:
            return self.zip_patterns(self.mine_sub_trees(threshold))

    def zip_patterns(self, patterns):
        """
        Append suffix to patterns in dictionary if
        we are in a conditional FP tree.
        """
        suffix = self.root.value

        if suffix is not None:
            # We are in a conditional tree.
            new_patterns = {}
            for key in patterns.keys():
                new_patterns[tuple(sorted(list(key) + [suffix]))] = patterns[key]

            return new_patterns

        return patterns

    def generate_pattern_list(self):
        """
        Generate a list of patterns with support counts.
        """
        patterns = {}
        items = self.frequent.keys()

        # If we are in a conditional tree,
        # the suffix is a pattern on its own.
        if self.root.value is None:
            suffix_value = []
        else:
            suffix_value = [self.root.value]
            patterns[tuple(suffix_value)] = self.root.count

        for i in range(1, len(items) + 1):
            for subset in itertools.combinations(items, i):
                pattern = tuple(sorted(list(subset) + suffix_value))
                patterns[pattern] = \
                    min([self.frequent[x] for x in subset])

        return patterns

    def mine_sub_trees(self, threshold):
        """
        Generate subtrees and mine them for patterns.
        """
        patterns = {}
        mining_order = sorted(self.frequent.keys(),
                              key=lambda x: self.frequent[x])

        # Get items in tree in reverse order of occurrences.
        for item in mining_order:
            suffixes = []
            conditional_tree_input = []
            node = self.headers[item]

            # Follow node links to get a list of
            # all occurrences of a certain item.
            while node is not None:
                suffixes.append(node)
                node = node.link

            # For each occurrence of the item, 
            # trace the path back to the root node.
            for suffix in suffixes:
                frequency = suffix.count
                path = []
                parent = suffix.parent

                while parent.parent is not None:
                    path.append(parent.value)
                    parent = parent.parent

                for i in range(frequency):
                    conditional_tree_input.append(path)

            # Now we have the input for a subtree,
            # so construct it and grab the patterns.
            subtree = FPTree(conditional_tree_input, threshold,
                             item, self.frequent[item])
            subtree_patterns = subtree.mine_patterns(threshold)

            # Insert subtree patterns into main patterns dictionary.
            for pattern in subtree_patterns.keys():
                if pattern in patterns:
                    patterns[pattern] += subtree_patterns[pattern]
                else:
                    patterns[pattern] = subtree_patterns[pattern]

        return patterns


def find_frequent_patterns(transactions, support_threshold):
    """
    Given a set of transactions, find the patterns in it
    over the specified support threshold.
    """
    tree = FPTree(transactions, support_threshold, None, None)
    return tree.mine_patterns(support_threshold)


def generate_association_rules(patterns, confidence_threshold):
    """
    Given a set of frequent itemsets, return a dict
    of association rules in the form
    {(left): ((right), confidence)}
    """
    rules = {}
    for itemset in patterns.keys():
        upper_support = patterns[itemset]

        for i in range(1, len(itemset)):
            for antecedent in itertools.combinations(itemset, i):
                antecedent = tuple(sorted(antecedent))
                consequent = tuple(sorted(set(itemset) - set(antecedent)))

                if antecedent in patterns:
                    lower_support = patterns[antecedent]
                    confidence = float(upper_support) / lower_support

                    if confidence >= confidence_threshold:
                        rules[antecedent] = (consequent, confidence)

    return rules


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
        deledges = []
        for ind, graph in enumerate(all_graphs):
            if graph[u][v] != 0 and distance.euclidean(graph[u][v], w) <= T:
                count = count + 1
            elif graph[u][v] != 0 and distance.euclidean(graph[u][v], w) > T:
                deledges.append([ind, c1[0]])
        if count >= minsup:
            F1.append([c1[0], w])
    return F1, deledges


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
    C1 = generateC1(F0)
    F1, deledges = findF1(C1)

    freqgraphs = []
    for edge in deledges:
        (ind, e) = edge
        graphs2edge[ind].remove(e)
    
    graphs = []
    for graph in graphs2edge:
        g = []
        for e in graph:
            g.append(int(e[1:]))
        graphs.append(g)
    transactions = graphs
    
    patterns = find_frequent_patterns(transactions, minsup)
    freq = list(patterns.keys())
    
    freq2edge = []
    for fsg in freq:
        edge = []
        for f in list(fsg):
            edgename = 'e'+str(f)
            for f1 in F1:
                if f1[0] == edgename:
                    edge.extend(f1)
        freq2edge.append(edge)
    
