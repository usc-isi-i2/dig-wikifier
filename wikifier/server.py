from flask import Flask
from flask import request
from flask_cors import CORS
import json
import requests
from optparse import OptionParser
import codecs
from requests.auth import HTTPBasicAuth
from extractor import AnchorTextExtractor
from graph_builder import GraphBuilder
from flask import jsonify

app = Flask(__name__)
# Load configs from file. File path must be set using command `export APP_SETTINGS=path/to/config.cfg
app.config.from_envvar('APP_SETTINGS')
CORS(app)

config = {}
redis_host = app.config.get('REDIS_HOST')
redis_port = app.config.get('REDIS_PORT')

anchor_text_extractor = AnchorTextExtractor()
graph_builder = GraphBuilder(redis_host, redis_port)
print("Initialization complete")
@app.route('/')
def home():
    return 'Wikifier implementation'

@app.route('/annotate', methods=['POST'])
def create_bipartite_graph():
    request_data = json.loads(request.data)
    tokens = anchor_text_extractor.extract_tokens(request_data["text"])
    print(tokens)
    return app.response_class(
        response = json.dumps({'tokens': tokens}),
        status=200,
        mimetype='application/json'
    )
