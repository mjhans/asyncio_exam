#!/usr/bin/env python

# builtin module
import asyncio
from collections import Counter
from datetime import datetime

# pip install module
import aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup

# user defined module
from util.myRedis import SimpleRedis
from util.redis_insert import *

URL_TPL = "http://comic.naver.com/webtoon/list.nhn?titleId=20853&\
weekday=tue&page={}"
CONCUR_req = 5

@asyncio.coroutine
def get_html(url):
	html = None
	response = None
	with ClientSession() as session:
		with aiohttp.Timeout(60):
			try:
				response = yield from session.get(url)
				
				if response.status == 200:
					return (yield from response.text('utf8'))
			except Exception as e:
				if response is not None:
					response.close()
				raise e
			finally:
				if response is not None:
					yield from response.release()


def parse_html(html):
	"""
	입력받은 마음의 소리 웹툰 페이지 html에서 마음의소리의 회차, 제목 url을 추출하여
	tuple로 만들고, 리스트에 갯수대로 저장하여 반환한다
	:param html: string
	:return: 마음의 소리 정보가 담긴 리스트
	"""
	webtoon_list = list()
	soup = BeautifulSoup(html, 'html.parser')
	webtoon_area = soup.find("table",
	                         {"class": "viewList"}
	                         ).find_all("td", {"class": "title"})
	for webtoon_index in webtoon_area:
		info_soup = webtoon_index.find("a")
		_url = info_soup["href"]
		_text = info_soup.text.split(".")
		_title = ""
		_num = _text[0]
		if len(_text) > 1:
			_title = _text[1]
		
		webtoon_list.append((_num, _title, _url,))
	return webtoon_list



@asyncio.coroutine
def collect_one_page(page_index, sema):
	result_dict = dict()
	try:
		with(yield from sema):
			url = URL_TPL.format(page_index)
		
			res_html = yield from get_html(url)
			result_dict = parse_html(res_html)
	except Exception as err:
		print(err)
	return result_dict
		
		

@asyncio.coroutine
def collect_many_page(indexes,concur_req, simple_redis, loop):
	counter = Counter()
	semaphore = asyncio.Semaphore(concur_req)
	to_do = [collect_one_page(index, semaphore) for index in indexes]
	to_do_iter = asyncio.as_completed(to_do)
	
	for future in to_do_iter:
		try:
			res = yield from future
			for info in res:
				save = yield from loop.run_in_executor(
					None,
					simple_redis.redis_hash_set,
					"maso",
					res[0], # key(page index)
					res # value (page info)
				)
			#counter["success"] += 1
		except Exception as err:
			print("test:", err)
			#counter["failure"] += 1
	
	return counter

@asyncio.coroutine
def collect_page_coro(simple_redis, loop=None):
	while True:
		count = None
		
		pop_result = yield from loop.run_in_executor(
			None,
			simple_redis.redisQ_pop,
			"page"
		)
		if pop_result is None:
			break
			
		count = yield from collect_many_page(pop_result, CONCUR_req,
											simple_redis, loop)
		#print("Counter:{}".format(count))
		

def collect_page_start(simple_redis):
	loop = asyncio.get_event_loop()
	coro = asyncio.async(collect_page_coro(simple_redis, loop))
	ret = loop.run_until_complete(coro)
	#print("result: {}".format(ret))
	
	
def do_main():
	sr = SimpleRedis()
	collect_page_start(sr)
	
if __name__ == "__main__":
	do_insert()
	sts = datetime.now()
	do_main()
	ets = datetime.now()
	print("elapse : {}".format(ets - sts))