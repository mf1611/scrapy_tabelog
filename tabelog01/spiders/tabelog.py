import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from bs4 import BeautifulSoup
from tabelog01.items import Restaurant


class TabelogSpider(CrawlSpider):
    name = 'tabelog'
    allowed_domains = ['tabelog.com']
    start_urls = [
        # 神奈川のランキングの1ページ目
        'https://tabelog.com/kanagawa/rstLst/?SrtT=rt&Srt=D&sort_mode=1'
        ]
    
    rules = [
        # 一覧ページ（2ページ目以降）
        Rule(LinkExtractor(allow=r'/\w+/rstLst/\d+/')),
        # 詳細ページのパース
        Rule(LinkExtractor(allow=r'/\w+/A\d+/A\d+/\d+/$'), 
                            callback='parse_restaurant')
    ]



    def parse_restaurant(self, response):
        """
        practice.pyで下記の情報を取れるか確認しながら記載
        """

        soup = BeautifulSoup(response.text, 'lxml')

        url = response.url

        name = soup.find('h2', class_='display-name').text.strip()
        address = soup.find('p', class_='rstinfo-table__address').text
        
        store_info = soup.find('div', class_='rdheader-subinfo') # 店舗情報のヘッダー枠データ取得
        store_info = store_info.find_all('dl')
        station = store_info[0].find('span').text

        genre = store_info[1].find_all('span')
        genre = [g.text for g in genre]

        score = soup.find('span', class_='rdheader-rating__score-val-dtl').text
        score = float(score)

        basic_info = soup.find_all('table', class_='c-table c-table--form rstinfo-table__table')
        basic_info = basic_info[0].find_all('td')
        transportation = [i.text.strip() for i in basic_info if station in i.text.strip()][0]
        
        item = Restaurant(
            url=url,
            name=name,
            address=address,
            station=station,
            transportation=transportation,
            genre=genre,
            score=score
        )

        yield item
