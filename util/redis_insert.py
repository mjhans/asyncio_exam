#!/usr/bin/env python

from util.myRedis import SimpleRedis

MAX = 100
CNT = 5

def do_insert():
	sr = SimpleRedis()
	index_list = list()
	for i in range(MAX):
		idx = i + 1
		index_list.append(idx)
		if idx % CNT == 0:
			sr.redisQ_push("page", index_list)
			index_list = list()
			
if __name__ == "__main__":
	do_insert()