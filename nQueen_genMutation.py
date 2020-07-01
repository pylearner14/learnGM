# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 11:47:47 2020

@author: 123171
"""

import random
import numpy as np
from numpy.random import choice
import pandas as pd

#Declarations
mutationRate = 0.03
allowedPopulation = 100
crossOver = 0.5
N=8

def randGen(n):
    return [random.randint(1,n) for _ in range (n)]


def checkFitness(parent):
    horizontal_collisions = sum([parent.count(queen)-1 for queen in parent])/2
    n=len(parent);
    leftDiagonal=[0]*2*n
    rightDiagonal=[0]*2*n
    
    for i in range(n):
        leftDiagonal[i+parent[i]-1] += 1
        rightDiagonal[len(parent)-i + parent[i]-2] += 1
    #print("parent",parent)
    #print("leftDiag",leftDiagonal)
    #print("rightDiag",rightDiagonal)
    #print("horizontalcoll",horizontal_collisions)
    diagonal_collisions=0
    for i in range(2*n-1):
        cntr=0
        if leftDiagonal[i]>1:
            cntr += leftDiagonal[i]-1
        if rightDiagonal[i]>1:
            cntr += rightDiagonal[i]-1
        diagonal_collisions += cntr/(n-abs(i-n+1))
    
    #print("Horizontal Collission",horizontal_collisions)
    #print("Diagonal Collisions",diagonal_collisions)
    #print("mFit score",mFit)
    #print("Fitness score")
    #print(int(mFit - (horizontal_collisions+diagonal_collisions)))
    return int(mFit - (horizontal_collisions+diagonal_collisions))


def crossOver(parent1, parent2):
    lnth=len(parent1)
    midPoint=random.randint(0,lnth-1)
    return parent1[0:midPoint]+parent2[midPoint:lnth]    

def mutate(parent):
    lnth=len(parent)
    randPoint=random.randint(0,lnth-1)
    randVal=random.randint(1,lnth)
    parent[randPoint]=randVal  
    return parent

def probability(parent,checkFitness):
    return checkFitness(parent)/mFit

def randomPick(population,probability):
    popProbability = zip(population,probability)
    total = sum(w for c,w in popProbability)
    r=random.uniform(0,total)
    upto=0
    for c,w in zip(population,probability):
        if upto + w >= r:
            return c
        upto +=w
    assert False, "Shouldnt be here"

def printFunc(chrom):
    print("Chromosome = {},  Fitness = {}"
        .format(str(chrom), checkFitness(chrom)))

def genQueen(population,checkFitness):
    mutatepercentage=.03
    newPopulation=[]
    probabilities = [probability(n,checkFitness) for n in population]
    for i in range(len(population)):
        parent1=randomPick(population,probabilities)
        parent2=randomPick(population,probabilities)
        child = crossOver(parent1,parent2)
        #print ("generated child")
        if random.random()<mutatepercentage:
            child=mutate(child)
        printFunc(child)
        newPopulation.append(child)
        #print("child addted;total population=",len(newPopulation))
        if checkFitness(child) == mFit:break
    return newPopulation
   
    
    
if __name__ == "__main__":
    mFit=(N*(N-1))/2  #### maxFitness
    totalPopulation = [randGen(N) for _ in range(allowedPopulation)] 


#print ('=======Population Generated{}=========="{}!"'.format(totalPopulation,"End"))

    generation=1
    cnt=1
    while not mFit in [checkFitness(parent) for parent in totalPopulation]:
        print("=== Generation {} ===".format(generation))
        totalPopulation = genQueen(totalPopulation,checkFitness)
        print("")
        print("Maximum Fitness = {}".format(max([checkFitness(n) for n in totalPopulation])))
        generation+=1
        cnt+=1
     #if cnt >4:
     #    break

    drawBoard = []
    print("Solved in Generation {}!".format(generation-1))
    for chrom in totalPopulation:
        if checkFitness(chrom)==mFit:
            print("")
            print("One of the Solutions")
            drawBoard=chrom
            printFunc(chrom)
       
    board=[]
    for x in range(N):
        board.append(["x"]*N)
            
    for i in range(N):
        board[N-drawBoard[i]][i]="Q"

    for row in board:
        print("".join(row))