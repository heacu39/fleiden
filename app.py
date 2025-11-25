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