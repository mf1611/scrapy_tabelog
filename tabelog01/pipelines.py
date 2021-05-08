# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import psycopg2


class PostgresPipeline(object):
    """
    ItemをPostgresDBに保存するPipeline
    """
    def open_spider(self, spider):
        """
        Spider開始時にPostgreに接続
        """
        host = 'localhost'
        port = 5432
        dbname = 'postgres'
        user = 'postgres'
        password = 'P@ssw0rd'
        self.connection = psycopg2.connect(f'host={host} port={port} dbname={dbname} user={user} password={password}')
        self.connection.autocommit = False
        self.cursor = self.connection.cursor()

        # 新規でテーブルを作成する場合
        self.table_name = 'store'
        query = f"""
                CREATE TABLE {self.table_name}(
                    url text not null,
                    name text not null, 
                    address text not null,
                    station text not null,
                    transportation text not null,
                    genre text not null,
                    score numeric not null
                    );
                """
        self.cursor.execute(query)
        self.connection.commit()  # 上記のクエリ結果を反映


    def close_spider(self, spider):
        """
        spiderの終了時にMongoDBに接続
        """
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
    
    def process_item(self, item, spider):
        """
        
        """
        values = (
            item['url'],
            item['name'],
            item['address'],
            item['station'],
            item['transportation'],
            item['genre'],
            item['score'],
        )
        query = f"""
                INSERT INTO {self.table_name}(
                    url.
                    name, 
                    address, 
                    station, 
                    transportation, 
                    genre, 
                    score
                    ) VALUES(
                        %s, %s, %s, %s, %s, %s, %s
                        );
                """
        self.cursor.execute(query, values)
        self.connection.commit()
        return item




class MongoPipeline(object):
    """
    ItemをMongoDBに保存するPipeline
    """
    def open_spider(self, spider):
        """
        Spider開始時にMongoDBに接続
        """
        self.client = MongoClient(host='localhost', 
                                  port=27017,
                                  username='root',
                                  password='P@ssw0rd'
        )
        self.db = self.client['scraping_tabelog']  # DBが存在しない場合でも新規作成される
        self.collection = self.db['items']  # itemsコレクションを取得, 存在しない場合でも新規作成される
    
    def close_spider(self, spider):
        """
        spiderの終了時にMongoDBに接続
        """
        self.client.close()
    
    def process_item(self, item, spider):
        """
        Itemをコレクションに追加する
        # insert_one()メソッドで、pythonのdictをコレクションに追加できる
        # insert_many()メソッドで、複数のdict(dictのリスト)をコレクションに追加できる
        """
        self.collection.insert_one(dict(item)) 
        return item