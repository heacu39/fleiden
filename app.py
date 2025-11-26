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
    return render_template("results.html", docs = docs)
    #items = []
    #for doc in docs:
    #    items.append(doc.json.annotation)
    #dict = {
    #    "@context": "http://iiif.io/api/search/2/context.json",
    #    "id": "url",
    #    "type": "AnnotationPage",
    #    "items": items
    #}        
    #return jsonify(dict)
