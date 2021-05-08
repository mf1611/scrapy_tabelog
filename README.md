## ScrapyによるスクレイピングとElasticsearchによるWeb検索ページ

- ここでは、食べログの神奈川県のランキングページにのるお店の情報をScrapyでスクレイピングし、そのデータをElasticsearchに入れ、Flaskを使ってweb検索ページを作成する

- scrapyを使うメリットの1つは、エラー処理等含めて体系的な設定ファイルでの管理が可能になっていること


- 参考: Pythonクローリング＆スクレイピング ―データ収集・解析のための実践開発ガイド, www.amazon.co.jp/dp/B01NGWKE0P



<br>

## 1. プロジェクトフォルダの作成
```
$ scrapy startproject tabelog01
```

- items.pyを記載（scraping対象となるクラスとそのfiled）
- settings.pyに下記を追記
    ```
    DOWNLOAD_DELAY=1  # 迷惑を掛けないために、間隔を平均1秒に設定
    FEED_EXPORT_ENCODING='utf-8'  # 文字化けをしないようにするために
    ```

<br>


## 2. spiderの作成(scrapyにおけるクローリングの設定や処理等)
```
$ cd tabelog01
$ scrapy genspider tabelog tabelog.com
```

- spiders/tabelog.pyを編集

    - クローリングのルールを記載
        ```python
        class TabelogSpider(CrawlSpider):
            name = 'tabelog'
            allowed_domains = ['tabelog.com']
            start_urls = []
            rules = []
        ```

    - 上記で作成されるtabelog.pyにスクレイピング詳細を記載するために、shellでどのように内容を取れるかを確認(scrapyの形式なら、scrapy shellでインタラクティブに確認すればいいが、beautifulsoupでやりたいので)
        ```python
        def parse_restaurant(self, response):
            ...
        ```

<br>

## 3. クローリング実施
```
$ mkdir output
$ scrapy crawl tabelog -o output/restaurants.jl  # jlは、jsonのline形式のファイル（1行ごとに処理可能なフォーマット）
```

<br>

## 4. Elasticsearchに投入
1. dockerでElasticsearchを起動（使用しているOS上でも良いが、docker使えばOSに依存せずにサーバーを起動出来る）

    ```
    $ cd docker_es
    $ docker-compose up
    ```

2. pythonを使って、3で得たjlデータをElasticsearchに投入

    ```
    $ python insert_into_es.py
    ```

## 5. FlaskでWebページ作成
1. dockerでElasticsearchを起動

    ```
    $ cd docker_es
    $ docker-compose up
    ```

2. Flaskを使って、検索フォームにクエリを入力（POST）すると、クエリに対してElasticsearchによる検索結果の一覧を表示させるようにする

    ```
    $ python app_server.py  # 実行後、http://localhost:8000にアクセス
    ```

<br>
<br>

## DBに保存する場合
### - PostgreSQLの場合
1. dockerでpostgresqlを起動
    
    ```
    $ docker pull postgres # イメージを持ってくる
    $ docker run -p 5432:5432 -v $PWD/data_psql:/data/db --name=postgres_tabelog --POSTGRES_PASSWORD=secret --POSTGES_USER=postgres -d postgres
    # もし作成済みなら、
    $ docker start postgres_tabelog

2. pipelines.pyにDBアクセスと、その際の処理を記載
    
    ```python
    class PostgresPipeline(object):
        def open_spider(self, spider):
            ...
        def close_spider(self, spider):
            ...
        def process_item(self, item, spider):
            ...
    ```
    
<br>

3. 下記をsettings.pyに追記
    ```
    ITEM_PIPELINES = {
        'tabelog01.pipelines.PostgresPipeline': 800,
    }
    ```
<br>

### - MongoDBの場合
1. dockerでmongodbを起動

    ```
    $ docker pull mongo # イメージを持ってくる
    $ docker run -p 27017:27017 -v $PWD/data_mongo:/data/db --name mongo_tabelog -d mongo
    # もし作成済みなら、
    $ docker start mongo_tabelog
    ```

2. pipelines.pyにDBアクセスと、その際の処理を記載

    ```python
    class MongoPipeline(object):
        def open_spider(self, spider):
            ...
        def close_spider(self, spider):
            ...
        def process_item(self, item, spider):
            ...
    ```

<br>

3. 下記をsettings.pyに追記:
    
    ```
    ITEM_PIPELINES = {
        'tabelog01.pipelines.MongoPipeline': 800,
    }
    ```

<br>
<br>

上記どちらか設定した状態で、

```
$ scrapy crawl tabelog
```

※ 保存しない場合は、settings.pyの該当部を消すこと
