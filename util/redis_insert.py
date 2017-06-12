#!/usr/bin/env python

from util.myRedis import SimpleRedis

MAX = 50
CNT = 5
if __name__ == "__main__":
	sr = SimpleRedis()
	index_list = list()
	for i in range(MAX):
		idx = i + 1
		index_list.append(idx)
		if idx % CNT == 0:
			sr.redisQ_push("page", index_list)
			index_list = list()