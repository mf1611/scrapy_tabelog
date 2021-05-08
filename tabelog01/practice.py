import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

url_page = 'https://tabelog.com/kanagawa/A1404/A140402/14066990/'

response = requests.get(url_page)
soup = BeautifulSoup(response.text, 'lxml')

name = soup.find('h2', class_='display-name')
print(name.text.strip())


store_info = soup.find('div', class_='rdheader-subinfo') # 店舗情報のヘッダー枠データ取得
store_info = store_info.find_all('dl')

station = store_info[0].find('span')
print(station.text)


genre = store_info[1].find_all('span')
genre = [g.text for g in genre]
print(genre)

address = soup.find('p', class_='rstinfo-table__address')
print(address.text)

score = soup.find('span', class_='rdheader-rating__score-val-dtl')
print(float(score.text))


basic_info = soup.find_all('table', class_='c-table c-table--form rstinfo-table__table')
basic_info = basic_info[0].find_all('td')
print([i.text.strip() for i in basic_info if station.text in i.text.strip()])


print(response.url)