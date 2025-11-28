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
    
@app.get("/page/<manifest>")
def page_search(manifest):
    term = request.args.get('q', '')
    res = r.ft('jvm').search(Query(f"{term}").summarize().highlight())
    docs = map(parseJSON, res.docs)
    return render_template('results.html', docs=docs, repr=f"{res}")
    #items = []
    #for doc in res.docs:
    #    container = json.loads(doc.json)
    #    items.append(container)
    #return jsonify(items)
    
@app.get("/search/<manifest>")
def search_get(manifest):
    term = request.args.get('q', '')
    res = r.ft('jvm').search(Query(f"@manifest:{{{manifest}}} @value:{{{term}}}"))
    #docs = map(parseJSON, res.docs)
    #return render_template("results.html", docs = docs)
    items = []
    for doc in res.docs:
        container = json.loads(doc.json)
        items.append(container['annotation'])
    dict = {
        "@context": "http://iiif.io/api/search/2/context.json",
        "id": request.url,
        "type": "AnnotationPage",
        "items": items
    }        
    return jsonify(dict)
    
@app.get("/v1/search/<manifest>")
def v1search_get(manifest):
    term = request.args.get('q', '')
    res = r.ft('jvm').search(Query(f"@manifest:{{{manifest}}} @value:{{{term}}}").paging(0, 9999))
    resources = []
    for doc in res.docs:
        container = json.loads(doc.json)
        resource = {
            "@id": container['annotation']['id'],
            "@type": "oa:Annotation",
            "motivation": "sc:painting",
            "resource": {
                "@type": "cnt:ContentAsText",
                "chars": container['annotation']['body']['value']
            },
            "on": container['annotation']['target']
        }
        resources.append(resource)
    dict = {
        "@context": [
            "http://iiif.io/api/presentation/2/context.json",
            "http://iiif.io/api/search/1/context.json"
        ],
        "@id": request.url,
        "@type": "sc:AnnotationList",
        "resources": resources
    }        
    return jsonify(dict)