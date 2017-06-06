#!/usr/bin/env python

from util.myRedis import SimpleRedis

if __name__ == "__main__":
	sr = SimpleRedis()
	for i in range(50):
		sr.redisQ_push("page",i)