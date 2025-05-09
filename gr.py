import random
import queue
import time
import os

rawResultQueue = queue.Queue(0)
prefer = []
grNameList = ["靈巧","敏捷","力量","生命","智力","精神"]
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def initialize():
    rawResultQueue = queue.Queue(0)
    prefer = []




def normal():
    result = []
    for i in range(2):

        result.append(random.randint(1,6))
    return result

def oned():
    result= random.randint(1,6)
    return int(result)

def prH(sp,prefer,dataQueue):
    list(prefer)
    resultList = []
    #print(dataQueue.empty())
    #print(prefer)
    while dataQueue.empty() == False:
        
        tar = dataQueue.get()
        #print(tar)
        for num in prefer:
            if num in tar:             
                resultList.append(num)
                break
            else:
                continue
    #print(resultList)
    for i in resultList:
        if sp == "a":
            if i not in [1,2]:
                #print(i)
                i = oned()
                #print(i)
                #print("/")
        if sp == "b":
            if i not in [3,4]:
                #print(i)
                i = oned()
                #print(i)
                #print("/")
        if sp == "c":
            if i not in [5,6]:
                #print(i)
                i = oned()
                #print(i)
                #print("/")

    readyToReturn = ""
    
    for j in range(6):
        quan = resultList.count(j+1)
        readyToReturn += f"{grNameList[j]}:{quan}\n"

    return readyToReturn

def main(prefer,dataQueue):
    
    list(prefer)
    resultList = []
    while dataQueue.empty() == False:
        
        tar = dataQueue.get()
        for num in prefer:
            if num in tar:             
                resultList.append(num)
                break
            else:
                continue
    
    readyToReturn = ""

    for j in range(6):
        quan = resultList.count(j+1)
        readyToReturn += f"{grNameList[j]}:{quan}\n"

    return readyToReturn


    




