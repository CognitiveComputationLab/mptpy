## created by Daniel Lux 
import subprocess, sys


x1 = .5
x2 = .2
x3 = .1
x4 = 0
numberOfRunns = 20

for i in range(len(sys.argv)-1):  
	if (sys.argv[i] == '-x1'):
		x1 = float(sys.argv[i+1])
	elif(sys.argv[i] == '-x2'):
		x2 = float(sys.argv[i+1])
	elif(sys.argv[i] == '-x3'):
		x3 = float(sys.argv[i+1])
	elif(sys.argv[i] == '-x4'):
		x4 = float(sys.argv[i+1])


### TODO: read in input from file
inputFile = [0] * 4
inputFile[0] = 0.875
inputFile[1] = 0.083
inputFile[2] = 0.5
inputFile[3] = 0.333
##generate numberOfRunns



r = [0] * 4
r[0] = x1 + (1-x1) * x2
r[1] = (1-x1) * x3
r[2] = (1-x4) * x2
r[3] = x4 + (1-x4) * x3 
error = 0
for x in range (0,4):
	error = error + abs(inputFile[x] - r[x])

# SMAC has a few different output fields; here, we only need the 4th output:
print("Result of algorithm run: SUCCESS, 0, 0, %f, 0" % error)


