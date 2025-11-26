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

@app.get("/search/<manifest>")
def search_get(manifest):
    term = request.args.get('q', '')
    res = r.ft('jvm').search(Query(f"@manifest:{{{manifest}}} @value:{{{term}}}"))
    docs = map(parseJSON, res.docs)
    items = []
    for doc in docs:
        items.append(doc.json)
    dict = {
        "items": items
    }        
    return jsonify(dict)