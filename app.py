from flask import Flask, request, render_template
import json
import redis
from redis.commands.search.query import Query

app = Flask(__name__)
application = app

r = redis.Redis(host='178.62.124.120', port=6379)
r.ping()


@app.route('/')
def hello_world():
    return 'Hello Fleiden!'
    
@app.route("/search/<term>")
def search(term):
    res = r.ft('jvm').search(Query("@value:ᰓᰨᰠ"))
    docs = map(parseJSON, res.docs)
    return render_template('results.html', total=res.total, term=term, docs=docs)
