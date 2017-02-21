#-*-coding:utf8-*-
#! /usr/bin/python
#encoding=utf-8
import random
from random import choice

class BalanceSample(object):
	def __init__(self):
		pass

	def random_choice(self,num,index_list,datas):
		count = 0
		data = []
		while count <= num:
			rand = choice(index_list)
			data.append(datas[rand])
			count = count+1	
		return data 				

	def over_sample(self,positive,negative,datas):

		if len(positive) > len(negative):
			sample_num = len(positive) - len(negative)
			over_data = self.random_choice(sample_num,positive,datas)

		else:
			sample_num = len(negative) - len(positive)	
			over_data = self.random_choice(sample_num,negative,datas)

		return over_data	
		