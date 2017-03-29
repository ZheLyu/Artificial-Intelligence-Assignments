# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 11:14:15 2016

@author:zhe
"""

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

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


def linearsvc(docs_train,y_train,docs_test):
    linearsvc = SVC(kernel='linear')
    linearsvc.fit(docs_train, y_train)
    pred = linearsvc.predict(docs_test)
    return pred

def rbfsvc(docs_train,y_train,docs_test):
    rbfsvc = SVC(kernel='rbf')
    rbfsvc.fit(docs_train, y_train)
    pred = rbfsvc.predict(docs_test)
    return pred

def random_forest(docs_train,y_train,docs_test):
    randomforest= RandomForestClassifier()
    randomforest.fit(docs_train,y_train)
    pred=randomforest.predict(docs_test)
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
    
 

    pred=linearsvc(docs_train,y_train,docs_test)
    linearsvc_result=calculatefm(pred,np.array(y_test))
    print("Correctly Classified Instances of Linearsvc:")
    print(linearsvc_result)

    pred = rbfsvc(docs_train, y_train, docs_test)
    rbfsvc_result = calculatefm(pred,np.array(y_test))
    print("Correctly Classified Instances of Rbfsvc:")
    print(rbfsvc_result)

    pred=random_forest(docs_train, y_train, docs_test)
    randomforest_result=calculatefm(pred,np.array(y_test))
    print("Correctly Classified Instances of Randomforest:")
    print(randomforest_result)

if __name__ == '__main__':
    GetResult()