import logging
import json
import random
from urllib.request import urlopen
from flask import Flask, render_template
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def index():
    """初期画面を表示します."""
    return render_template("index.html")

@app.route("/api/recommend_article")
def api_recommend_article():
    """はてブのホットエントリーから記事を入手して、ランダムに1件返却します."""

    # 1. はてブのホットエントリーページのHTMLを取得する
    with urlopen("http://feeds.feedburner.com/hatena/b/hotentry") as res:
        html = res.read().decode("utf-8")
    # 2. BeautifulSoupでHTMLを読み込む
    soup = BeautifulSoup(html, "html.parser")
    # 3. 記事一覧を取得する
    titles = soup.select("item")
    # 4. ランダムに1件取得し以下の形式で返却する.
    #     {
    #         "content" : "記事のタイトル",
    #         "link" : "記事のURL"
    #     }

    index = random.randrange(100)

    if index >= len(titles):
        logging.error('error!')
        return json.dumps( {
            "content" : "記事のタイトル",
            "link" : "記事のURL"
        })

    title = titles[index]
    return json.dumps({
        "content" : title.find("title").string,
        "link" : title.get('rdf:about')
    })

# @app.route("/api/xxxx")
# def api_xxxx():
#     """
#         **** ここを実装します（発展課題） ****
#         ・自分の好きなサイトをWebスクレイピングして情報をフロントに返却します
#         ・お天気APIなども良いかも
#         ・関数名は適宜変更してください
#     """
#     pass

if __name__ == "__main__":
    app.run(debug=True, port=5004)
