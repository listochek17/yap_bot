"""Минимальный парсер сайта yaponamama.uz.

Версия: минимальные изменения от оригинального закомментированного кода,
разделённые на функции: получение категорий, получение продуктов по категории
и сохранение в JSON. Лёгкие исправления: абсолютные ссылки и аккуратное
сохранение результатов.

Запуск: python pars_evos.py
"""

from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import json
import time
import os

HOST = 'https://yaponamama.uz/'
OUT_DIR = os.path.dirname(__file__)
CATEGORY_FILE = os.path.join(OUT_DIR, 'category.json')
PRODUCTS_FILE = os.path.join(OUT_DIR, 'products.json')


def make_session():
	"""Создать простую сессию requests с заголовком."""
	s = requests.Session()
	s.headers.update({
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
	})
	return s


def fetch_categories(session):
	"""Скачать главную страницу и собрать список категорий.

	Возвращает список словарей {'name': ..., 'link': ...}.
	"""
	resp = session.get(HOST, timeout=10)
	resp.raise_for_status()
	soup = BeautifulSoup(resp.text, 'html.parser')
	category_block = soup.find('div', class_='style_categories___eG8o')
	if not category_block:
		return []
	categories = []
	nodes = category_block.find_all('div', class_='cursor-pointer')
	for node in nodes:
		p = node.find('p')
		a = node.find('a')
		if not p or not a:
			continue
		name = p.get_text(strip=True)
		link = urljoin(HOST, a.get('href'))
		categories.append({'name': name, 'link': link})
	return categories


def fetch_products_for_category(session, category, cat_id):
	"""Собрать продукты для заданной категории.

	Возвращает список словарей {'title':..., 'coast':..., 'cat_id':...}.
	"""
	resp = session.get(category['link'], timeout=10)
	resp.raise_for_status()
	soup = BeautifulSoup(resp.text, 'html.parser')
	articles = soup.find_all('div', class_='style_card__4UCei')
	products = []
	for art in articles:
		title_tag = art.find('p', class_='style_title__1polx')
		price_tag = art.find('p', class_='style_original_price__7aXl7')
		if not title_tag:
			continue
		title = title_tag.get_text(strip=True)
		coast = price_tag.get_text(strip=True) if price_tag else ''
		products.append({'title': title, 'coast': coast, 'cat_id': cat_id})
	return products


def save_json(obj, path):
	with open(path, 'w', encoding='utf-8') as f:
		json.dump(obj, f, ensure_ascii=False, indent=2)


def main():
	session = make_session()
	categories = fetch_categories(session)
	save_json(categories, CATEGORY_FILE)

	products = []
	for idx, cat in enumerate(categories, start=1):
		try:
			prods = fetch_products_for_category(session, cat, idx)
			products.extend(prods)
		except Exception as e:
			# пропускаем ошибочную категорию, но продолжаем
			print(f'Ошибка при парсинге категории {cat.get("name")}:', e)
		time.sleep(1)

	save_json(products, PRODUCTS_FILE)



if __name__ == '__main__':
	main()
