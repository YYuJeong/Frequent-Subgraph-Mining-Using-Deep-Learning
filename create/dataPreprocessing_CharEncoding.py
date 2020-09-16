# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 21:17:14 2020

@author: YuJeong
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 14:13:49 2020

@author: YuJeong
"""

import numpy as np
import glob, os
import string
dir = '.\\datasets\\seq\\*'

alpha = list(string.ascii_uppercase)
chr2index = {alpha[i]:i for i in range(len(alpha))}

def chr2OH(alphabet):
    oh = [0 for i in range(len(alpha))]
    index = chr2index[alphabet]
    return index


# file read
all_names = []
all_data = []
sequence_length = []
alpha = list(string.ascii_uppercase)
data_length = len(glob.glob(dir))
file_predix = '.\\datasets\\seq'
files = glob.glob(dir)
'''
for index in range(data_length):
    filename = file_predix + str(index) + "/*"
    print(filename)
    files = glob.glob(filename)
    print(files)
'''

files = glob.glob(dir)
for file in files[:2]:
    datasets = []
    all_names.append(file.split('\\')[-1].replace('.txt', ''))
    for rf in open(file, 'r'):
        (u, v, w) = rf[1:-2].split(', ')
        datasets.append([chr2OH(u[1]) , chr2OH(v[1]), float(w)])
    sequence_length.append(len(datasets))
    all_data.append(datasets)
 
all_data = np.array([np.array(arr) for arr in all_data])

max_sequence_length = max(sequence_length)
zeros = np.zeros(53)
     

for ind, data in enumerate(all_data):
    if len(data) != max_sequence_length:
        for i in range(len(data), max_sequence_length):
            all_data[ind] = np.vstack([all_data[ind], zeros])

for data in all_data:
    if len(data) != max_sequence_length:
        print("false")        





