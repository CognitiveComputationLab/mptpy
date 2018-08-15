## created by Daniel Lux 
import subprocess, sys, csv
import numpy as npy

x1 = 0.5775756914
x2 = 0.1600268164
x3 = 0.952920719
r = 0.2783749729
p = 0.4026238717
np = 0.2168196325
q = 0.6697347092
nq = 0.2120422532

numberOfRunns = 20

for i in range(len(sys.argv)-1):  
	if (sys.argv[i] == '-x1'):
		x1 = float(sys.argv[i+1])
	elif(sys.argv[i] == '-x2'):
		x2 = float(sys.argv[i+1])
	elif(sys.argv[i] == '-x3'):
		x3 = float(sys.argv[i+1])
	elif(sys.argv[i] == '-r'):
		r = float(sys.argv[i+1])
	elif(sys.argv[i] == '-p'):
		p = float(sys.argv[i+1])
	elif(sys.argv[i] == '-np'):
		np = float(sys.argv[i+1])
	elif(sys.argv[i] == '-q'):
		q = float(sys.argv[i+1])
	elif(sys.argv[i] == '-nq'):
		nq = float(sys.argv[i+1])

##generate numberOfRunns
r = r * 100
r = int(r)
print(r)
tempNum = 100 - r
##Dont change this -> ruins all calculation
factor = 1
numberOfRunns = tempNum * factor

## create command line input with parameter and call lisp function call-selection from sk.lisp (formerly selection-task.lisp)
callselection = '(call-selection ' +str(x1) +' '+ str(x2) +' '+str(x3)+' '+str(numberOfRunns)+')'
print(callselection)
cmd = ['sbcl', '--noinform', '--load', '/home/noef/lisp/sk.fasl', '--eval', callselection, '--eval', '(exit)']
output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]

## decode console output to pathon string
output = output.decode('utf-8')
#print(output)
output = output.split('\n')

countSelections = [0] * 16

#change this number if the output from sbcl changes, check this on every system
numberOfPreprintedLines = 6
## check outputs per line and generate binary number from it to calculate difference
for x in range (numberOfPreprintedLines,len(output)):
	temp = 0
	if '(P)' in output[x]:
		temp = temp + 8
	if '(- P)' in output[x]:
		temp = temp + 4
	if '(Q)' in output[x]:
		temp = temp + 2
	if '(- Q)' in output[x]:
		temp = temp + 1
	countSelections[temp] = countSelections[temp] + 1

##Guessingtree:
r = r / 100
rFactor = [0] * 16
rFactor[0] = (r) * (1-p) * (1-np) * (1-q) * (1-nq)
rFactor[1] = (r) * (1-p) * (1-np) * (1-q) * nq
rFactor[2] = (r) * (1-p) * (1-np) * q * (1-nq) 
rFactor[3] = (r) * (1-p) * (1-np) * q * nq 
rFactor[4] = (r) * (1-p) * np * (1-q) * (1-nq) 
rFactor[5] = (r) * (1-p) * np * (1-q) * nq 
rFactor[6] = (r) * (1-p) * np * q * (1-nq)
rFactor[7] = (r) * (1-p) * np * q * nq
rFactor[8] = (r) * p * (1-np) * (1-q) * (1-nq)
rFactor[9] = (r) * p * (1-np) * (1-q) * nq
rFactor[10] = (r) * p * (1-np) * q * (1-nq)
rFactor[11] = (r) * p * (1-np) * q * nq
rFactor[12] = (r) * p * np * (1-q) * (1-nq)
rFactor[13] = (r) * p * np * (1-q) * nq
rFactor[14] = (r) * p * np * q * (1-nq)
rFactor[15] = (r) * p * np * q * nq

for x in range (0,len(countSelections)):
	countSelections[x] = countSelections[x] / 100
	countSelections[x] = countSelections[x] + rFactor[x]


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
#npy.savetxt('jolaParG16.csv', a, delimiter=',')
print("Result of algorithm run: SUCCESS, 0, 0, %f, 0" % error)
