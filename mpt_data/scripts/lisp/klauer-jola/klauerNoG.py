## created by Daniel Lux 
import subprocess, sys, csv
import numpy as npy

c = 0.07716730352293283
d = 0.6126706561511327
s = 0.8522686597984686
i = 0.44903587533706635
x = 0.8427955625424043

numberOfRunns = 20

for i in range(len(sys.argv)-1):  
	if(sys.argv[i] == '-s'):
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
tree[0] = 0
tree[1] = c * (1-d) * (1-s) * i
tree[2] = c * (1-d) * s * i
tree[3] = (1-c) * (1-x) * (1-d) * i
tree[4] = c * d * (1-s) * i
tree[5] = (1-c) * x * (1-s) * i
tree[6] = c * d * (1-s) * (1-i) + c * (1-d) * s * (1-i)
tree[7] = 0
tree[8] = c * d * s * i
tree[9] = c * d * s * (1-i) +  c * (1-d) * (1-s) * (1-i)
tree[10] = (1-c) * x * s * i
tree[11] = 0
tree[12] = (1-c) * (1-x) * d * i
tree[13] = 0
tree[14] = 0
tree[15] = (1-c) * x * s * (1-i) +  (1-c) * x * (1-s) * (1-i) +  (1-c) * (1-x) * d * (1-i) +   (1-c) * (1-x) * (1-d) * (1-i) 


countSelections = tree
print(countSelections)
print(npy.sum(countSelections))

### ERROR CALCULATION ###
error = 0
##TODO:
inputData =npy.genfromtxt('/home/noef/lisp/klauer-jola/16points.csv', delimiter=',')
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
npy.savetxt('klNoG16.csv', a, delimiter=',')
print("Result of algorithm run: SUCCESS, 0, 0, %f, 0" % error)

