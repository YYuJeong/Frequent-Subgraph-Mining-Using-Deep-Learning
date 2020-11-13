# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 15:43:32 2020

@author: YuJeong
"""
from pathlib import Path

def writeFile(index, sub2seq):
    filename = "\\datasets\\estimate_size\\test\\test" +  str(index) + '.txt'
    path = str(Path(__file__).parent.parent) + filename
    print(path)
    f = open(path, 'w')

    for row in sub2seq:
        print(str(row))
        f.write(str(row) + '\n')
    f.close()


if __name__ == '__main__':
    subNum = int(input('Subgraph number for Testing: '))
    for i in range(subNum):
        sub2seq = []
        while True:
            inp = input('u v weight: ')
            if inp != 'z':
                seq = list(map(int, inp.split(' ')))
                sub2seq.append(seq)
                print(seq)
            else:
                writeFile(i, sub2seq)
                break
            