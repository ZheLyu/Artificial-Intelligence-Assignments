# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 09:16:21 2016

@author: dell
"""
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import scale
import matplotlib.pyplot as plt
 
def readArff(fileName):
    arffFile = open(fileName,'r')
    data = []
    for line in arffFile.readlines():
        if not (line.startswith('@')):
            if not (line.startswith('%')):
                if line !='\n':
                    L=line.strip('\n')
                    k=L.split(',')
                    data.append(k)
    return data

def logic(docs_train,y_train,docs_test):
    clf= LogisticRegression(C=1)
    clf.fit(docs_train, y_train)
    pred = clf.predict(docs_test)
    plt.clf()
    plt.scatter(docs_train.ravel(), y_train, color='black', zorder=20)
  
    return pred
    
def calculatefm(pred,y_test):
    tp, fp, fn = 1, 0, 0
    for i in range(len(pred)):
        if (pred[i] == y_test[i] and pred[i]== 1):
            tp += 1
        elif (pred[i] != y_test[i] and y_test[i] == 1):
            fn += 1
        elif (pred[i] != y_test[i] and y_test[i] == 0):
            fp += 1
        pre = tp / (tp + fp)
        rec = tp / (tp + fn)
        f_measure = (2 * pre * rec) / (pre + rec)
    return f_measure

def GetResult():
    data = readArff('chronic_kidney_disease_full.arff')
    label=[]
    for temp in data:
        if (len(temp) != 25):
            temp.remove('')
        if(temp[24]=='ckd'):
            temp[24]=1
        else:
            temp[24]=0
        label.append(temp[24])
        del temp[24]
    for temp in data:
        for i in range(24):
            if (temp[i] == '?' or temp[i] == '\t?'):
                temp[i] = float(0)
            elif(temp[i]=='normal' or temp[i]=='present' or temp[i]=='yes'or temp[i]=='good' or temp[i]==' yes' or temp[i]=='\tyes'):
                temp[i]=float(2)
            elif(temp[i]=='abnormal' or temp[i]=='notpresent' or temp[i]=='no' or temp[i]=='poor' or temp[i]=='\tno'):
                temp[i]=float(1)
            else:
                temp[i]=float(temp[i])

        docs_train, docs_test, y_train, y_test = train_test_split(
        data, label, test_size=0.2, random_state=None)
    
    
    
    datatrain = scale(docs_train)
    testdatatrain=scale(docs_test)
    
    pred=logic(datatrain ,y_train,testdatatrain)
    logic_result=calculatefm(pred,np.array(y_test))
    print("result of standardization:")
    print(logic_result)

    pred=logic(docs_train,y_train,docs_test)
    logic_result=calculatefm(pred,np.array(y_test))
    print("result of logic:")
    print(logic_result)
    
    
    

if __name__ == '__main__':
    GetResult()    
    