#-*-coding:utf8-*-
#! /usr/bin/python
#encoding=utf-8
from __future__ import division
from math import log
import json
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')
from random import choice
from redis import Redis
import pickle
import time
import os
import os.path 
import glob

class decisionnode:

    def __init__(self,col = -1,value = None, results = None, tb = None,fb = None):
        self.col = col   
        self.value = value 
        self.results = results
        self.tb = tb 
        self.fb = fb   


class DecisionTree(object):

    def __init__(self):
        pass

    def uniquecounts(self,rows):
        results = {}
        for row in rows:
            r = row[len(row)-1]
            if r not in results:results[r] = 0
            results[r]+=1
        return results

    def giniimpurity_2(self,rows):
        total = len(rows)
        counts = self.uniquecounts(rows)
        imp = 0
        for k1 in counts.keys():
            p1 = float(counts[k1])/total
            imp+= p1*(1-p1)
        return imp    


    def entropy(self,rows):
     
        log2 = lambda x:log(x)/log(2)
        results = self.uniquecounts(rows)
        ent = 0.0
        for r in results.keys():
            p = float(results[r])/len(rows)
            ent = ent - p*log2(p)
        return ent  
    

    def divideset(self,rows,column,value):
    
        split_function = None
        if isinstance(value,int) or isinstance(value,float):
            split_function = lambda row:row[column] >= value
        else:
            split_function = lambda row:row[column]==value
    
        set1 = [row for row in rows if split_function(row)]
        set2 = [row for row in rows if not split_function(row)]
        return(set1,set2)
    
    
    def buildtree(self,rows,scoref = entropy):
        if len(rows)==0 : return decisionnode()

        current_score = scoref(rows)
        best_gain = 0.0
        best_criteria = None
        best_sets = None
        
        column_count = len(rows[0]) - 1
        for col in range(0,column_count):
            column_values = {}
            for row in rows:
                column_values[row[col]] = 1 
            for value in column_values.keys():
                (set1,set2) = self.divideset(rows,col,value)
                p = float(len(set1))/len(rows)
                print (p)
                gain = current_score - p*scoref(set1) - (1-p)*scoref(set2)
               
                if gain>best_gain and len(set1)>0 and len(set2)>0:
                    best_gain = gain
                    best_criteria = (col,value)
                    best_sets = (set1,set2)
        if best_gain>0:
            trueBranch = self.buildtree(best_sets[0],self.entropy) 
            falseBranch = self.buildtree(best_sets[1],self.entropy)
            return decisionnode(col = best_criteria[0],value = best_criteria[1],
                                tb = trueBranch,fb = falseBranch)
        else:
            return decisionnode(results = self.uniquecounts(rows))
    
    
    
    def printtree(self,tree,indent = ''):
    
        if tree.results!=None:
            print (json.dumps(tree.results,encoding='utf-8',ensure_ascii=False))
        else:
            print str(tree.col)+":"+str(tree.value)+"? "
            print indent+"T->",
            self.printtree(tree.tb,indent+" ")
            print indent+"F->",
            self.printtree(tree.fb,indent+" ")
    
    
    def classify(self,observation,tree):
      
        if tree.results!= None:
            return tree.results
        else:
            v = observation[tree.col]
            branch = None
            if isinstance(v,int) or isinstance(v,float):
                if v>= tree.value: branch = tree.tb
                else: branch = tree.fb
            else:
                if v==tree.value : branch = tree.tb
                else: branch = tree.fb
       
            return self.classify(observation,branch)
    
    
    
    def prune(self,tree,mingain):
        if tree.tb.results == None:
            prune(tree.tb,mingain)
        if tree.fb.results == None:
            prune(tree.fb,mingain)
        if tree.tb.results !=None and tree.fb.results !=None:
            tb,fb = [],[]
            for v,c in tree.tb.results.items():
                tb+=[[v]]*c
            for v,c in tree.fb.results.items():
                fb+=[[v]]*c
            delta = entropy(tb+fb)-(entropy(tb)+entropy(fb)/2)
            if delta < mingain:
                tree.tb,tree.fb = None,None
                tree.results = uniquecounts(tb+fb)
        return tree   
