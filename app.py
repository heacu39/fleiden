from flask import Flask, request, render_template, jsonify
import json
import redis
from redis.commands.search.query import Query

app = Flask(__name__)
application = app

r = redis.Redis(host='178.62.124.120', port=6379)

def parseJSON(doc):
    doc.json = json.loads(doc.json)
    return doc
    
@app.route('/')
def hello_world():
    return 'Hello Fleiden!'
    
@app.get("/search")
def search_get():
    term = request.args.get('q', '')
    res = r.ft('jvm').search(Query(f"@value:{{{term}}}"))
    docs = map(parseJSON, res.docs)
    return docs
    #return render_template('results.html', docs=docs)