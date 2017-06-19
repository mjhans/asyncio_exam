#!/usr/bin/env python

# builtin module
from datetime import datetime

# pip install module
import requests
from bs4 import BeautifulSoup

# user defined module
from util.myRedis import SimpleRedis
from util.redis_insert import *

URL_TPL = "http://comic.naver.com/webtoon/list.nhn?titleId=20853&weekday=tue&page={}"

def get_html(url):
	_html = ""
	resp = requests.get(url)
	if resp.status_code == 200:
		_html = resp.text
	return _html


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
	        ).find_all("td", {"class":"title"})
	for webtoon_index in webtoon_area:
		info_soup = webtoon_index.find("a")
		_url = info_soup["href"]
		_text = info_soup.text.split(".")
		_title  = ""
		_num = _text[0]
		if len(_text) > 1:
			_title = _text[1]
			
		webtoon_list.append((_num, _title, _url, ))
	return webtoon_list

def collect_one_page(page_index):
	url = URL_TPL.format(page_index)
	
	res_html = get_html(url)
	res_parse = parse_html(res_html)
	return res_parse
	
def get_pageindex_from_redis(simple_redis):
	total = 0
	while True:
		indexes = simple_redis.redisQ_pop("page")
		if indexes is None:
			break
		for index in indexes:
			infos = collect_one_page(index)
			insert_webtoon_info(simple_redis, infos)
			total += 1
	
	print("{} 저장되었습니다".format(total))
		
def insert_webtoon_info(simple_redis, infos):
	for info in infos:
		res = simple_redis.redis_hash_set("maso", info[0], info)
			

def do_main():
	sr = SimpleRedis()
	get_pageindex_from_redis(sr)

if __name__ == "__main__":
	do_insert()
	sts = datetime.now()
	do_main()
	ets = datetime.now()
	
	print("elapse : {}".format(ets-sts))