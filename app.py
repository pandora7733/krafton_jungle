from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbjungle  # 'dbjungle'라는 이름의 db를 만들거나 사용합니다.


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/save', methods=['POST'])
def post_article():
    # 1. 클라이언트로부터 데이터를 받기
    title_receive = request.form['title_give']  # 클라이언트로부터 title을 받는 부분
    content_receive = request.form['content_give']  # 클라이언트로부터 content를 받는 부분
    likeCount = 0 #초기 좋아요 수 0

    article = { 'title': title_receive, 'content': content_receive, 'likeCount': likeCount }

    # 3. mongoDB에 데이터를 넣기
    db.articles.insert_one(article)

    return jsonify({'result': 'success'})

@app.route('/contents', methods=['GET'])
def read_articles():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기 (Read)
    result = list(db.articles.find({}, {'_id': 0}))
    # 2. articles라는 키 값으로 article 정보 보내주기
    return jsonify({'result': 'success', 'articles': result})

@app.route('/delete', methods=['POST'])
def delete_article():
    title_receive = request.form['title_give']
    db.articles.delete_one({'title': title_receive})
    return jsonify({'result': 'success'})

@app.route('/update', methods=['POST'])
def update_article():
    title_receive = request.form['title_give']
    new_title_receive = request.form['new_title_give']
    content_receive = request.form['content_give']
    db.articles.update_one({'title': title_receive}, {'$set': { 'title': new_title_receive, 'content': content_receive}})
    return jsonify({'result': 'success'})

@app.route('/like', methods=['POST'])
def like_article():
    title_receive = request.form['title_give']
    db.articles.update_one({'title': title_receive}, {'$inc': {'likeCount': 1}})
    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)