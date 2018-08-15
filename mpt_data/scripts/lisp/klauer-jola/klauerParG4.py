## created by Daniel Lux 
import subprocess, sys, csv
import numpy as npy

r = 0.00020941004059442337
p = 0.9994269324258951
np = 0.003373600525019546
q = 0.5583356799213123
nq = 0.2151103494962462
c = 0.9446618774040285
d = 0.9624767647385005
s = 0.9763440863593029
i = 0.20272543540993582
x = 0.9846854693979286

numberOfRunns = 20

for i in range(len(sys.argv)-1):  
	if(sys.argv[i] == '-r'):
		r = float(sys.argv[i+1])
	elif(sys.argv[i] == '-p'):
		p = float(sys.argv[i+1])
	elif(sys.argv[i] == '-np'):
		np = float(sys.argv[i+1])
	elif(sys.argv[i] == '-q'):
		q = float(sys.argv[i+1])
	elif(sys.argv[i] == '-nq'):
		nq = float(sys.argv[i+1])
	elif(sys.argv[i] == '-s'):
		s = float(sys.argv[i+1])
	elif(sys.argv[i] == '-d'):
		d = float(sys.argv[i+1])
	elif(sys.argv[i] == '-i'):
		i = float(sys.argv[i+1])
	elif(sys.argv[i] == '-i'):
		c = float(sys.argv[i+1])
	elif(sys.argv[i] == '-x'):
		x = float(sys.argv[i+1])

##Guessingtree:
tree = [0] * 16
tree[0] = (1-r) * (1-p) * (1-np) * (1-q) * (1-nq)
tree[1] = (1-r) * (1-p) * (1-np) * (1-q) * nq + r * c * (1-d) * (1-s) * i
tree[2] = (1-r) * (1-p) * (1-np) * q * (1-nq) + r * c * (1-d) * s * i
tree[3] = (1-r) * (1-p) * (1-np) * q * nq + r * (1-c) * (1-x) * (1-d) * i
tree[4] = (1-r) * (1-p) * np * (1-q) * (1-nq) + r * c * d * (1-s) * i
tree[5] = (1-r) * (1-p) * np * (1-q) * nq + r * (1-c) * x * (1-s) * i
tree[6] = (1-r) * (1-p) * np * q * (1-nq) + r * c * d * (1-s) * (1-i) + r * c * (1-d) * s * (1-i)
tree[7] = (1-r) * (1-p) * np * q * nq
tree[8] = (1-r) * p * (1-np) * (1-q) * (1-nq) + r * c * d * s * i
tree[9] = (1-r) * p * (1-np) * (1-q) * nq + r * c * d * s * (1-i) + r * c * (1-d) * (1-s) * (1-i)
tree[10] = (1-r) * p * (1-np) * q * (1-nq) + r * (1-c) * x * s * i
tree[11] = (1-r) * p * (1-np) * q * nq
tree[12] = (1-r) * p * np * (1-q) * (1-nq) + r * (1-c) * (1-x) * d * i
tree[13] = (1-r) * p * np * (1-q) * nq
tree[14] = (1-r) * p * np * q * (1-nq)
tree[15] = (1-r) * p * np * q * nq + r * (1-c) * x * s * (1-i) + r * (1-c) * x * (1-s) * (1-i) + r * (1-c) * (1-x) * d * (1-i) +  r * (1-c) * (1-x) * (1-d) * (1-i) 


countSelections = tree
print(countSelections)
print(npy.sum(countSelections))

### ERROR CALCULATION ###
error = 0
##TODO:
inputData =npy.genfromtxt('/home/noef/lisp/klauer-jola/4points.csv', delimiter=',')
#print(inputData)
temp = 0
count = 0
averageError = 0
averageErrordivPar = 0
csvArray = []
for x in range (0, len(inputData)):
	temp = error
	tempArray = []
	participants = npy.sum(inputData[x])
	tempArray.append(participants)
	#print('next:')	
	#print(participants)
	tempErr = 0
	for y in range (0,len(inputData[x])):
		##TODO: find error function for fit which is not ramdom giberish 
		tempErr = tempErr + (abs((inputData[x][y]/participants) - countSelections[y]))
	temp = tempErr
	averageError =  averageError + tempErr
	averageErrordivPar = averageErrordivPar + temp
	tempArray.append(tempErr)
	tempArray.append(temp)
	#print(temp)
	error = error + temp
	csvArray.append(tempArray)
# SMAC has a few different output fields; here, we only need the 4th output:
print(averageError / len(inputData))
print(averageErrordivPar / len(inputData))
#print(csvArray)
foo = 0
bar = 0
for x in range (0, len(csvArray)):
	foo = foo + csvArray[x][1]
	bar = bar + csvArray[x][2]
foo = foo / len(csvArray)
bar = bar / len(csvArray)
tempArray = [0, foo, bar]
csvArray.append(tempArray)
a = npy.asarray(csvArray)
#print(a)
#TODO
npy.savetxt('klParG4.csv', a, delimiter=',')
print("Result of algorithm run: SUCCESS, 0, 0, %f, 0" % error)

