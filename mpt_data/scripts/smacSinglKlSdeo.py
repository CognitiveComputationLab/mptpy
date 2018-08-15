import pysmac
import numpy as npy
import time
indice = 0

def error (x1, x2, x3, x4):
	params = [0] *4
	params[0] = x1
	params[1] = x2
	params[2] = x3
	params[3] = x4
	tree = [0] *4
	tree[0] = params[2] * params[0] * params[1] * params[3] 
	tree[1] = params[2] * params[0] * params[1] * (1-params[3]) + params[2] * params[0] * (1-params[1])
	tree[2] = params[2] * (1-params[0])
	tree[3] = (1-params[2])
	tree = npy.array(tree)
	d = fullData[indice][8:12]
	distance = d - (tree * npy.sum(d))
	temp = npy.sqrt((npy.sum(distance * distance) / 4))
	return(temp)

def prints (x1, x2, x3, x4):
	results = [0] * 5
	params = [0] *4
	params[0] = x1
	params[1] = x2
	params[2] = x3
	params[3] = x4
	tree = [0] *4
	tree[0] = params[2] * params[0] * params[1] * params[3] 
	tree[1] = params[2] * params[0] * params[1] * (1-params[3]) + params[2] * params[0] * (1-params[1])
	tree[2] = params[2] * (1-params[0])
	tree[3] = (1-params[2])
	tree = npy.array(tree)
	d = fullData[indice][8:12]
	distr = tree * npy.sum(d)
	distance = d - (tree * npy.sum(d))
	results[4] = npy.sqrt((npy.sum(distance * distance) / 4))
	for x in range (0,4):
		if d[x] < distr[x]:
			results[x] = d[x]
		else:
			results[x] = distr[x]
	return(results)


parameters=dict(\
                x1=('real',[0, 1], 0.5),
                x2=('real',[0, 1], 0.5),
                x3=('real',[0, 1], 0.5),
                x4=('real',[0, 1], 0.5),
                )

path = "/home/noef/smac-v2.10.03-master-778/hiwi/4patern/4deontic.csv"#allADG.csv"
dataFile = path
data = npy.genfromtxt(dataFile, delimiter=",")
dataAgg = data.sum(axis=0)
fullData = npy.append(data, dataAgg.reshape(1, -1), axis=0)

start = time.time()
resultsArr = []
paramsArr = []
for x in range (0,len(fullData)):
	opt = pysmac.SMAC_optimizer()
	indice = x
	vals, params = opt.minimize(error, 10000, parameters)
	paramsArr.append(params)
	print(x)
	x1 = params['x1']
	x2 = params['x2']
	x3 = params['x3']
	x4 = params['x4']
	restemp = prints(x1, x2, x3, x4)
	resultsArr.append(restemp)
printer = npy.array(resultsArr)
print(paramsArr)
end = time.time()
print(end - start)
npy.savetxt("results/deoKS.csv", printer, delimiter=',')