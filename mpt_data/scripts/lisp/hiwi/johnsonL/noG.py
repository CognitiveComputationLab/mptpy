## created by Daniel Lux 
import subprocess, sys, csv
import numpy as npy

##default parmeterset
x1 = 0.4622856581
x2 = 0.4189480789
x3 = 0.580371264

#paths for evaluation data
path = "/home/noef/lisp/smac/4patern/"
dataSets = ["4abstract.csv", "4deontic.csv", "4generalization.csv", "4cluster1.csv", "4cluster2.csv", "4cluster3.csv", "4allAbstDeonGenc1c2c3.csv", "4test.csv"]
dataArgument = 0

#read arguments
for i in range(len(sys.argv)-1):  
	if (sys.argv[i] == '-x1'):
		x1 = float(sys.argv[i+1])
	elif(sys.argv[i] == '-x2'):
		x2 = float(sys.argv[i+1])
	elif(sys.argv[i] == '-x3'):
		x3 = float(sys.argv[i+1])
	elif(sys.argv[i] == '-data'):
		dataArgument = int(sys.argv[i+1])
#set dataPath and print datatype
dataPath = path + dataSets[dataArgument]
print("Data used: " + dataSets[dataArgument])

"""-----------------------------------------------------------------------------"""
##generate numberOfRunns
numberOfRunns = 100
## create command line input with parameter and call lisp function call-selection from sk.lisp (formerly selection-task.lisp)
callselection = '(call-selection ' +str(x1) +' '+ str(x2) +' '+str(x3)+' '+str(numberOfRunns)+')'
print(callselection)
cmd = ['sbcl', '--noinform', '--load', '/home/noef/lisp/sk.fasl', '--eval', callselection, '--eval', '(exit)']
output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
## decode console output to pathon string
output = output.decode('utf-8')
#print(output)
output = output.split('\n')

##Create results from Lisp
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
for x in range (0,len(countSelections)):
	countSelections[x] = countSelections[x] / numberOfRunns
print(countSelections)
"""-----------------------------------------------------------------------------"""

#initialice error calculation
error = 0
inputData =npy.genfromtxt(dataPath, delimiter=',')
#print(inputData)

csvArray = []
csvNames = '#participants, error0, error1, error2, error3, error4, error5, error6, error7, error8, error9, error10, error11, error12, error13, error14, error15, SumAbsErr, SumRelativeError'
for x in range (0, len(inputData)):
	csvTemp = []
	participants = npy.sum(inputData[x])
	csvTemp.append(participants)
	tempErr = 0
	temp = 0
	for y in range (0,len(inputData[x])):
		temp = (abs((inputData[x][y]) - (countSelections[y] * participants)))
		csvTemp.append(temp)
		tempErr = tempErr + temp
		pass
	csvTemp.append(tempErr)
	tempErr = tempErr / participants
	csvTemp.append(tempErr)
	error = error + tempErr
	csvArray.append(csvTemp)
##uncoment the following part to print solutions into csv
printer = npy.array(csvArray)
npy.savetxt('noG' + dataSets[dataArgument], printer, delimiter=',', header=csvNames)
print("Result of algorithm run: SUCCESS, 0, 0, %f, 0" % error)
