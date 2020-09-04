# graph - adjacency version
import copy as cp
import glob
import os

def bfs(start, data):
	adj = cp.deepcopy(data)
	vertex = len(adj)
	queue = [start]
	visited[start] = True
	sequence = []
	while queue:
		now = queue.pop(0)
		for i in range(1, vertex):	
			if adj[now][i] == 0 or visited[i]:
				if not (visited[i] and adj[now][i] != 0):
					continue
			#print(now, adj[now][i], i)
			sequence.append([now, i, adj[now][i]])
			adj[now][i] = 0
			adj[i][now] = 0
			queue += [i]
			visited[i] = True
	return sequence


# sort with maked time
#files = sorted(glob.glob('graph/datasets/*'), key=os.path.getmtime)
    
folders = glob.glob(os.getcwd()+'\\datasets\\group*')
seqfolders = glob.glob(os.getcwd() + '\\datasets\\seq*')
#files = glob.glob(folders[0]+'\\graph*.txt')
for idx, folder in enumerate(folders):
    files = glob.glob(folder+'\\graph*.txt')
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
            newF = open(os.getcwd() + '\\datasets\\seq' + str(idx+1) + '\\'+ basefile+"-"+str(i)+'.txt', 'w+')
            for seq in bfs(i, data):
                newF.write(str(seq) + '\n')
            newF.close()
        f.close()
        
