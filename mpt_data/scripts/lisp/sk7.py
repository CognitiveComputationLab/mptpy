## created by Daniel Lux 
import subprocess, sys


x1 = .5
x2 = .2
x3 = .1
numberOfRunns = 20

for i in range(len(sys.argv)-1):  
	if (sys.argv[i] == '-x1'):
		x1 = float(sys.argv[i+1])
	elif(sys.argv[i] == '-x2'):
		x2 = float(sys.argv[i+1])
	elif(sys.argv[i] == '-x3'):
		x3 = float(sys.argv[i+1])


### TODO: read in input from file
inputFile = [0] * 16
inputFile[8] = 12
inputFile[9] = 2
inputFile[10] = 14
inputFile[11] = 0
##generate numberOfRunns
tempNum = 0
factor = 1
for x in range (0,len(inputFile)):
	tempNum = tempNum + inputFile[x]
if tempNum > 0:
	numberOfRunns = tempNum * factor
print(numberOfRunns)

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
print(countSelections)
error = 0
for x in range(0,len(inputFile)):
	error = error + abs(inputFile[x] - countSelections[x])
print(error)

# SMAC has a few different output fields; here, we only need the 4th output:
print("Result of algorithm run: SUCCESS, 0, 0, %f, 0" % error)


