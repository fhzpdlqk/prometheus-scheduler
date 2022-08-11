import random

import prometheus_client
from flask import Flask, Response
from flask_cors import CORS
from prometheus_client import Counter, Gauge, CollectorRegistry, push_to_gateway
from apscheduler.schedulers.background import BackgroundScheduler
import requests

sched = BackgroundScheduler()
registry = CollectorRegistry()
g = Gauge('my_inprogress_requests', 'Description of gauge', registry=registry)

@sched.scheduled_job('interval', seconds=10, id="test1")
def get_api():
    API_HOST = "http://20.196.229.134:5000/matrics"
    headers = {'Content-Type': 'application/json'}
    response = requests.get(API_HOST, headers=headers)
    g.set(response.json()["data"])
    return

def create_app(test_config=None):
    app = Flask(__name__)
    requests_total = Counter("request_count", "Total request cout of the host", registry=registry)

    CORS(app)

    sched.start()

    @app.route("/metrics")
    def requests_gauge():
        return Response(prometheus_client.generate_latest(registry),
                        mimetype="text/plain")
    return app