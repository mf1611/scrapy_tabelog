from elasticsearch import Elasticsearch
from flask import Flask, render_template, request

app = Flask(__name__)

es = Elasticsearch(['localhost:9200'])

@app.route('/', methods=["GET", "POST"])
def index():
    """
    /へのリクエストを処理
    """
    if request.method == "GET":
        return render_template('search.html')
    else:
        # クエリ(?q=の値)を取得
        # query = request.args.get['q']
        query = request.form['q']
        pages = search_pages(query) if query else []
        return render_template('search.html', query=query, pages=pages)
        


def search_pages(query):
    """
    引数にとったqueryでの検索結果のリストを返す
    """

    result = es.search(
        index='pages', 
        doc_type='page', 
        body={
            "query": {
                "match": {"name": query},
                "match": {"genre": query},
                "match": {"station": query},
                "match": {"transportation": query}
            },
            }
        )

    return result['hits']['hits']



if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)
