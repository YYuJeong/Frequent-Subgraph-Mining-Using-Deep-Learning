# graph - adjacency version
import copy as cp
import glob
import os, string


alpha = list(string.ascii_uppercase)
chr2index = {i:alpha[i] for i in range(len(alpha))}

def OH2chr(OH):
    index = chr2index[OH]
    return index


# sort with maked time
#files = sorted(glob.glob('graph/datasets/*'), key=os.path.getmtime)
    

#folders = glob.glob(os.getcwd()+'\\datasets\\group*')
#seqfolders = glob.glob(os.getcwd() + '\\datasets\\seq*')
folders = glob.glob(os.getcwd()+'\\datasets\\fsm\\random')

#files = glob.glob(folders[0]+'\\graph*.txt')
for idx, folder in enumerate(folders):
    files = glob.glob(folder+'\\2graph*.txt')
    for ind, file in enumerate(files):
        basefile = 'graph'+str(ind)
        f = open(file, 'r')
        data = []
        for r in f:
            data.append(list(map(float, r.split())))
        visited = [False for i in range(len(data))]
    	#print(f)
        for i in range(1, len(data)):
            #print('start', i, bfs(i, data))
            newF = open(os.getcwd() + '\\datasets\\fsm\\seq\\'+ str(2) + basefile+"-"+str(i)+'.txt', 'w+')
            for seq in bfs(i, data):
                newF.write(str(seq) + '\n')
            newF.close()
        f.close()
        
