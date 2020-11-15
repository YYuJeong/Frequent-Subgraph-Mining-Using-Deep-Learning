# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 14:48:46 2020

@author: sookmyung
"""
import os 
import random
from pathlib import Path
import glob

path = str(Path(__file__).parent.parent) 
files = glob.glob(path +  '\\datasets\\estimate_size\\test\\*') 
all_names = []

for file in files:
    all_names.append(file.split('\\')[-1].replace('.txt', ''))

namesbysize = []
for _ in range(15):
    line = []
    namesbysize.append(line)
    

for names in all_names:
    namesbysize[int(names[:names.find('test')])].append(names)
    
predicts = []
for _ in range(15):
    line = []
    predicts.append(line)

precision = []    
for ind, name in enumerate(namesbysize):
    print(ind)
    precision.append(len(predicts[ind])/len(namesbysize))
    
    
'''    
for ind, predict in enumerate(1, predicts):
    print(ind+1)
'''