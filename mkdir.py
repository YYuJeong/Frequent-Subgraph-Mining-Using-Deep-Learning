import os
print(os.getcwd())


for i in range(1, 7):
	os.mkdir('./datasets/group' + str(i))

#for i in range(9, 17):
#	os.mkdir('group1/group' + str(i))