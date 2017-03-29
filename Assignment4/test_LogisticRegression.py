# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 13:48:26 2016

@author: dell
"""
import csv
import random
import numpy
import matplotlib.pyplot as plt
import LogisticRegression as LR
from sklearn.preprocessing import scale


#import data
data = numpy.genfromtxt('input.csv', delimiter=',')
# response is in the first column
Y = data[:, 0]
X = data[:, 1:]

# n-fold cross validation
# shuffle data
m = len(Y)

index = range(0, m)
random.shuffle(index)
X = X[index, :]
Y = Y[index]
X1=scale(X)
Y1=Y
# n-fold
nfold = 10
foldSize = int(m / nfold)

# arrage to store training and testing error

testErr = [0.0] * nfold


trainX=X[0:319]
trainY=Y[0:319]
testX=X[320:399]
testY=Y[320:399]
    # set parameter
alpha = 0.05
lam =[-2,-1,0,1,2,3,4]
for j in lam:

    model = LR.LogisticRegression(trainX, trainY, alpha, j)
    model.run(400, printIter=False)

    testPred = model.predict(testX)
    accuracy = 1-float(sum(testPred != testY)) / len(testY)
    TP,TN,FP,FN = 0.0,0.0,0.0,0.0
    for i in range(len(testY)):
        if(testPred[i] == 1 and testY[i]== 1):
            TP += 1
        if(testPred[i] == 0 and testY[i] == 0):
            TN += 1
        if(testPred[i] == 0 and testY[i] == 1):
            FP += 1
        if(testPred[i] == 1 and testY[i]== 0):
            FN += 1
    Pr = TP/(TP+FP)
    Re = TP/(TP+FN)
    f = (2*Pr*Re)/(Pr+Re)
    testPred = model.predict(testX)
    testErr= float(sum(testPred != testY)) / len(testY)
    print "feature", f 
    print "testaccuracy", accuracy
    print " "
    print 
    plt.scatter(j,f,s=50,c='b',marker='o', label='f_m')


plt.xlabel('lamda')
plt.ylabel('feature')


plt.show()

trainX1=X1[0:319]
trainY1=Y1[0:319]
testX1=X1[320:399]
testY1=Y1[320:399]
    # set parameter
alpha = 0.2
lam =[-2,-1,0,1,2,3,4]

for j in lam:

    model = LR.LogisticRegression(trainX1, trainY1, alpha, j)
    model.run(400, printIter=False)

    testPred = model.predict(testX1)
    accuracy = 1-float(sum(testPred != testY1)) / len(testY1)
    TP,TN,FP,FN = 0.0,0.0,0.0,0.0
    for i in range(len(testY1)):
        if(testPred[i] == 1 and testY1[i]== 1):
            TP += 1
        if(testPred[i] == 0 and testY1[i] == 0):
            TN += 1
        if(testPred[i] == 0 and testY1[i] == 1):
            FP += 1
        if(testPred[i] == 1 and testY1[i]== 0):
            FN += 1
    Pr = TP/(TP+FP)
    Re = TP/(TP+FN)
    f = (2*Pr*Re)/(Pr+Re)
    testPred = model.predict(testX1)
    testErr= float(sum(testPred != testY1)) / len(testY1)
    print "feature", f 
    print "testaccuracy", accuracy
    print " "
    print 
    plt.scatter(j,f,s=50,c='b',marker='o', label='f_m')


plt.xlabel('lamda')
plt.ylabel('feature-standarize')


plt.show()

