#!/usr/bin/python

from flask import Flask, Response
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

metrics = PrometheusMetrics(app)

counter = 0


@app.route('/')
def visit():
    global counter
    counter = counter + 1
    result = "Visit number %d\n" % counter
    return Response(result, mimetype='text/plain')

@app.route('/metrics')
def metrics():
    global counter
    result = "# TYPE hello_world_counter counter\nhello_world_counter %d\n" % counter
    return Response(result, mimetype='text/plain')

app.run()
