#-*-coding:utf8-*-
#! /usr/bin/python
#encoding=utf-8
from mysqlclient import MysqlClient
from unbalanceSample import BalanceSample
from decisiontree import DecisionTree
import time
import sys
import re
import os
reload(sys)
sys.setdefaultencoding('utf-8')
import json 
import time
import random



class PickleTree(object):

	def __init__(self):
		pass

	def readTree(self):
		files = glob.glob("/Users/homelink/dianping/decision/*")
		for f in files:
			reader = open(f,'rU')
			tree =  pickle.load(reader)
			self.forest_tree[f] = tree


	def writeTree(self):
		f = open("/Users/homelink/dianping/decision_3/"+area[0].replace("/","#")+"_"+area[1].replace("/","#")+".txt","a")
		pickle.dump(tree,f)
		f.flush()
		f.close()
      
class decisionnode:

    def __init__(self,col = -1,value = None, results = None, tb = None,fb = None):
        self.col = col   
        self.value = value 
        self.results = results
        self.tb = tb 
        self.fb = fb          

class Decision(object):

	def __init__(self):
		self.forest_tree = {}
		self.test_list = []
		self.tree = DecisionTree()
		self.sample = BalanceSample()
		self.file_name = open("/Users/homelink/storein/rent.txt","r")
		self.datas = []

	def generateSample(self):  	
		positive = []
		negative = []
		count = 0
		for data in self.file_name.readlines():
			rent_dic = json.loads(data)
			self.datas.append([rent_dic["business_area"],rent_dic["area"],rent_dic["width"],rent_dic["face"],rent_dic["structure"],rent_dic["height"],rent_dic["day_rent_per_centare"] ,rent_dic["tenancy"] ,rent_dic["transfer_fee"] ,rent_dic["licence"] ,rent_dic["water"] ,rent_dic["power"] ,rent_dic["fire"] ,rent_dic["wind"] ,rent_dic["gas"] ,rent_dic["industry"] ,rent_dic["is_rent"]])
			
			if rent_dic["is_rent"] == "True":
				positive.append(count)
			else :
				negative.append(count)	
			count = count+1		
 		data = self.sample.over_sample(positive,negative,self.datas)
 		self.datas = self.datas+data


	def run(self):
		self.generateSample()
		tree = self.tree.buildtree(self.datas,self.tree.giniimpurity_2)
		# prune(tree,0.1)
		self.tree.printtree(tree)
 

	def frequence(self,trade):
		trade_dic = {}
		trade_area = []
		for i in trade:
			if i in trade_dic.keys():
				trade_dic[i] = trade_dic[i]+1
			else:
				trade_dic[i] = 1
		max_index = max(list(trade_dic.values())) 
		for key,value in trade_dic.items():
			if value == max_index:
				trade_area.append(key) 
		return (trade_area)         

	def accuracy(self):       
		true_index = 0
		false_index = 0
		test_list = []
		test = open("/Users/homelink/dianping/test.txt","r")
		for line in test.readlines():
			test_list = test_list+list(eval(line))
		    
		for i in range(len(test_list)):
			test = test_list[i]
			result_true = test[5]
			trade_store = []
			
			for key,tree in self.forest_tree.items(): 
				result = classify([test[0],int(test[1]),float(test[2]),float(test[3]),float(test[4])],tree)
			   
				max_value = 0
				for key,value in result.items():
					if value>max_value:
						max_value = value
						trade = key
				trade_store.append(trade)
	   
			option_result = self.frequence(trade_store) 
	  
			if result_true in option_result:
				true_index = true_index+1
			else:
				false_index = false_index+1  
			    
		return  true_index/len(test_list) 


a = Decision()
a.run()
# thread = ThreadPool(runnable=run,num_of_threads = 4)
# thread.wait_for_complete()



 

