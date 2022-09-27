# Copyright (c) Alex Ellis 2017. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

from flask import Flask, request, jsonify
from waitress import serve
import requests
import os
from multiprocessing import Value
counter = Value('i', 0)

app = Flask(__name__)

# distutils.util.strtobool() can throw an exception
def is_true(val):
    return len(val) > 0 and val.lower() == "true" or val == "1"



@app.before_request
def fix_transfer_encoding():
    """
    Sets the "wsgi.input_terminated" environment flag, thus enabling
    Werkzeug to pass chunked requests as streams.  The gunicorn server
    should set this, but it's not yet been implemented.
    """

    transfer_encoding = request.headers.get("Transfer-Encoding", None)
    if transfer_encoding == u"chunked":
        request.environ["wsgi.input_terminated"] = True



@app.route("/", defaults={"path": ""}, methods=["POST", "GET"])
@app.route("/<path:path>", methods=["POST", "GET"])
def main_route(path):
    # raw_body = os.getenv("RAW_BODY", "false")

    # as_text = True

    # if is_true(raw_body):
    #     as_text = False
    # ret = handler.handle(request.get_data(as_text=as_text))

    #ret = handler.handle(request)
##    print("Hello")
##    print(request.get_data())
##    print(request.headers)
    URL=[
        "http://192.168.56.117:7011",
        "http://192.168.56.117:7012",
        "http://192.168.56.117:7013",
        "http://192.168.56.117:7014",
        "http://192.168.56.117:7015",
        "http://192.168.56.117:7016",
        "http://192.168.56.117:7017",
        "http://192.168.56.117:7018",
        "http://192.168.56.117:7019",
        "http://192.168.56.117:7020",
        ]

    with counter.get_lock():
        counter.value += 1
        out = counter.value
        if out==len(URL):
            counter.value=0
            out=0

    print(out)
    url=URL[out]
##    response = requests.post("http://172.17.0.2:8080", data = request.get_data(), headers=request.headers)
    
##    print("Called")
    return jsonify(url)

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=7000)
