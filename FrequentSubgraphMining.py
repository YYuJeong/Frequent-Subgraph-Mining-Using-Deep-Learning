# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 17:15:23 2020

@author: YuJeong
"""

import numpy as np
import glob, os
import string


dir = '.\\datasets\\fsm\\*'

alpha = list(string.ascii_uppercase)
chr2index = {alpha[i]:i for i in range(len(alpha))}

def chr2OH(alphabet):
    index = chr2index[alphabet]
    return index

all_names = []
all_data = []
sequence_length = []
data_length = len(glob.glob(dir))

files = glob.glob(dir)
print(files)
for file in files:
    datasets = []
    all_names.append(file.split('\\')[-1].replace('.txt', ''))
    for rf in open(file, 'r'):
        (u, v, w) = rf[1:-2].split(', ')
        datasets.append([chr2OH(u[1]), chr2OH(v[1]) , float(w)])
    sequence_length.append(len(datasets))
    all_data.append(datasets)