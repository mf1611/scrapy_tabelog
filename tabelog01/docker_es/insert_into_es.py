import sys
import hashlib
import json
from elasticsearch import Elasticsearch

"""
usage:
elasticsearchが立ち上がっている状態で、下記を実行
$ python insert_into_es.py ../output/restaurants.jl
"""


es = Elasticsearch(['localhost:9200'])

result = es.indices.create(index='pages', ignore=400, body={
    # settingsという項目で、analyzerを定義
    'settings': {
        'analysis': {
            'analyzer': {
                'kuromoji_analyzer': {
                    'tokenizer': 'kuromoji_tokenizer'
                }
            }
        }
    }, 
    # mappingsという項目で、pageタイプを定義
    'mappings': {
        'page': {
            # _allは、全てのフィールドを結合して1つの文字列とした特殊なフィールド
            '_all': {'analyzer': 'kuromoji_analyzer'},
            'properties': {
                'url': {'type': 'string'},
                'name': {'type': 'string', 'analyzer': 'kuromoji_analyzer'},
                'address': {'type': 'string', 'analyzer': 'kuromoji_analyzer'},
                'station': {'type': 'string'},
                'transportation': {'type': 'string', 'analyzer': 'kuromoji_analyzer'},
                'genre': {'type': 'string'},
                'score': {'type': 'float'},
            }
        }
    }
})

print(result)  # elasticsearchからのレスポンスを表示


# コマンドライン引数で指定したパスのファイルを読み込む
with open(sys.argv[1]) as f:
    for line in f:  # json line形式のファイル(.jl)を1行ごとに読み込み
        page = json.loads(line)

        # urlのハッシュ値をドキュメントidとする
        doc_id = hashlib.sha1(page['url'].encode('utf-8')).hexdigest()

        # elasticsearchにインデックス化（保存）する
        result = es.index(index='pages', doc_type='page', id=doc_id, body=page)
        print(result)