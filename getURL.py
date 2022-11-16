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
        "http://130.194.72.10:7011",
        "http://130.194.72.10:7012",
        "http://130.194.72.10:7013",
        "http://130.194.72.10:7014",
        "http://130.194.72.10:7015",
        "http://130.194.72.10:7016",
        "http://130.194.72.10:7017",
        "http://130.194.72.10:7018",
        "http://130.194.72.10:7019",
        "http://130.194.72.10:7020",
        "http://130.194.72.10:7021",
        "http://130.194.72.10:7022",
        "http://130.194.72.10:7023",
##        "http://130.194.72.10:7024",
##        "http://130.194.72.10:7025",
##        "http://130.194.72.10:7026",
##        "http://130.194.72.10:7027",
##        "http://130.194.72.10:7028",
##        "http://130.194.72.10:7029",
##        "http://130.194.72.10:7030",
##        "http://130.194.72.10:7031",
##        "http://130.194.72.10:7032",
##        "http://130.194.72.10:7033",
##        "http://130.194.72.10:7034",
##        "http://130.194.72.10:7035",
##        "http://130.194.72.10:7066",
##        "http://130.194.72.10:7037",
##        "http://130.194.72.10:7038",
##        "http://130.194.72.10:7039",
##        "http://130.194.72.10:7040",
##        "http://130.194.72.10:7041",
        ]

    with counter.get_lock():
        counter.value += 1
        out = counter.value
        if out==len(URL):
            counter.value=0
            out=0

    print(URL[out])
    url=URL[out]
##    response = requests.post("http://172.17.0.2:8080", data = request.get_data(), headers=request.headers)
    
##    print("Called")
    return jsonify(url)

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=7000)
