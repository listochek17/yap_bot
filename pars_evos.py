# import requests
# from bs4 import BeautifulSoup
# import json
#
# HOST = 'https://yaponamama.uz/'
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
# }
#
# html = requests.get(HOST, headers=headers).text
# soup = BeautifulSoup(html, 'html.parser')
#
# category_block = soup.find('div', class_='style_categories___eG8o')
# categories = category_block.find_all('div', class_='cursor-pointer')
#
# category_data = []
# for category in categories:
#     cat_name = category.find('p').get_text(strip=True)
#     cat_link = category.find('a').get('href')
#     category_data.append({
#         'name': cat_name,
#         'link': cat_link,
#     })
#
#
# with open('category.json', mode='w', encoding='utf-8') as f:
#     json.dump(category_data, f, indent=4, ensure_ascii=False)
#
#
# cat_id = 0
# products_data = []
# for item in category_data:
#     html2 = requests.get(item['link']).text
#     soup2 = BeautifulSoup(html2, 'html.parser')
#     articles = soup2.find_all('div', class_='style_card__4UCei')
#     cat_id += 1
#     for article in articles:
#         title = article.find('p', class_='style_title__1polx').get_text(strip=True)
#         coast = article.find('p', class_='style_original_price__7aXl7').get_text(strip=True)
#
#         products_data.append({
#             'title': title,
#             'coast': coast,
#             'cat_id': cat_id
#         })
#
#
# with open('products.json', mode='w', encoding='utf-8') as f:
#     json.dump(products_data, f, indent=4, ensure_ascii=False)
