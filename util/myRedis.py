#!/usr/bin/env python


import json
import pickle

import redis

REDISQ_PREFIX = "RedisQ"
REDISHASH_PREFIX = "RedisHash"

class SimpleRedis(object):
	
	def __init__(self, host='localhost', port=6379, db=0, *args, **kwargs):
		self.redis_conn = redis.StrictRedis(host=host, port=port, db=db)
	
	def redisQ_pop(self, qkey):
		rq_key = "{}:{}".format(REDISQ_PREFIX, qkey)
		msg = self.redis_conn.lpop(rq_key)
		result = None
		if msg is not None:
			result = pickle.loads(msg)
		return result
	
	def redisQ_push(self, qkey, value):
		rq_key = "{}:{}".format(REDISQ_PREFIX, qkey)
		msg = pickle.dumps(value)
		result = self.redis_conn.rpush(rq_key, msg)
		return result
	
	def redis_hash_set(self, field, hkey, value):
		h_field = "{}:{}".format(REDISHASH_PREFIX, field)
		msg = pickle.dumps(value)
		result = self.redis_conn.hset(h_field, hkey, msg)
		return result
	
	def redis_hash_get(self, field, hkey):
		h_field = "{}:{}".format(REDISHASH_PREFIX, field)
		msg  = self.redis_conn.hget(h_field, hkey)
		return pickle.loads(msg)
	

if __name__ == "__main__":
	sr = SimpleRedis()
	sr.redisQ_push("test", 1)
	sr.redisQ_push("test", 2)
	sr.redisQ_push("test", 3)
	
	while True:
		res = sr.redisQ_pop("test")
		if res is None:
			break
		print(res)