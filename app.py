from flask import Flask, request, render_template
import json
import redis
from redis.commands.search.query import Query

app = Flask(__name__)
application = app

pool = redis.ConnectionPool(host='178.62.124.120', port=6379, db=0)
#pool = redis.ConnectionPool(host='192.168.1.20', port=6379, db=0)
red = redis.Redis(connection_pool=pool)

@app.route('/')
def hello_world():
    return 'Hello Fleiden!'
    
@app.route("/search/<lepcha>")
def entries(prefix):
    q = Query(f"@value:{{{lepcha}}}").paging(0, 9999)
    res = red.ft('jvm').search(q)
    docs = map(parseJSON, res.docs)
    return render_template('results.html', total=res.total, lepcha=lepcha, docs=docs, repr=f"{res}")
