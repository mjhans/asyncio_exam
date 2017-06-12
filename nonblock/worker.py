#!/usr/bin/env python

# builtin module
import asyncio

# pip install module
import aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup

# user defined module
from util.myRedis import SimpleRedis

URL_TPL = "http://comic.naver.com/webtoon/list.nhn?titleId=20853&\
weekday=tue&page={}"

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
def collect_one_page(page_index):
	url = URL_TPL.format(page_index)
	
	res_html = yield from get_html(url)
	res_parse = parse_html(res_html)
	return res_parse

@asyncio.coroutine
def collect_page_coro():
	pass
	